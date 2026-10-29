#!/usr/bin/env python3
"""
Ace Werk — blog static generator.

Python 3 stdlib ONLY. No third-party markdown package.

Reads markdown source files from `content/posts/<slug>.md` and emits:

  - blog/index.html        — reverse-chronological card list + search + pagination
  - blog/<slug>/index.html — one rendered post page per source file
  - blog/search-index.json — static search index

Run from anywhere:  python scripts/build_blog.py
"""

import html
import json
import math
import re
import os
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"
BLOG_DIR = ROOT / "blog"
SEARCH_INDEX_FILE = BLOG_DIR / "search-index.json"

# Threshold at which the search index stops being inlined and is fetched
# lazily on first focus of the search field (~200KB per spec).
INLINE_INDEX_THRESHOLD_BYTES = 200 * 1024

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

SITE_URL = "https://acewerk.com"

# ACEWERK_ENV=prod builds indexable pages with production analytics and never
# includes fixtures. Any other value (or unset) is a dev/staging build.
PROD = (os.environ.get("ACEWERK_ENV") or "").strip().lower() == "prod"
PROD_ANALYTICS = (
    '  <script defer src="https://x.acewerk.com/tessera.js" '
    'data-website-id="15435e6c-c2e0-4995-bd8e-db662d4474f3"></script>\n'
)

# Required + optional front matter fields.
REQUIRED_FIELDS = ("title", "slug", "date", "author", "excerpt")

# ──────────────────────────────────────────────────────────────────────────
# Markdown parsing (bounded subset)
# ──────────────────────────────────────────────────────────────────────────

_INLINE_TOKEN = re.compile(
    r"`([^`]+)`"                                        # 1 inline code
    r"|\[([^\]]+)\]\((?:<([^>]+)>|([^)\s]+))\)"         # 2 label, 3 url<>, 4 url
    r"|\*\*([^*]+)\*\*"                                 # 5 strong **
    r"|__([^_]+)__"                                     # 6 strong __
    r"|(?<!\*)\*([^*\s][^*]*)\*(?!\*)"                  # 7 em *
    r"|(?<![\w])_([^_\s][^_]*)_(?!_)"                  # 8 em _
    r"|(?<!\]\()(https?://[^\s<>)\]]+)"          # 9 bare url
)


def render_inline(text):
    """Render the bounded inline subset to HTML (links, code, strong, em)."""
    out = []
    pos = 0
    for m in _INLINE_TOKEN.finditer(text):
        out.append(html.escape(text[pos:m.start()]))
        g = m.groups()
        if g[0] is not None:  # code
            out.append("<code>" + html.escape(g[0]) + "</code>")
        elif g[1] is not None:  # link
            url = g[2] if g[2] is not None else g[3]
            out.append(
                '<a href="%s">%s</a>'
                % (html.escape(url, quote=True), render_inline(g[1]))
            )
        elif g[4] is not None or g[5] is not None:
            inner = g[4] if g[4] is not None else g[5]
            out.append("<strong>" + render_inline(inner) + "</strong>")
        elif g[8] is not None:  # bare url
            url = g[8]
            out.append(
                '<a href="%s">%s</a>' % (html.escape(url, quote=True), html.escape(url))
            )
        else:  # em (g[6] or g[7])
            inner = g[6] if g[6] is not None else g[7]
            out.append("<em>" + render_inline(inner) + "</em>")
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)


_HEADING_RE = re.compile(r"^(#{2,4})\s+(.*)$")
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
_LIST_ITEM_RE = re.compile(r"^([ \t]*)([-*+]|\d+\.)\s+(.*)$")
_TABLE_ROW_RE = re.compile(r"^\|.*\|$")
_TABLE_SEP_CELL_RE = re.compile(r"^\s*:?-{1,}:?\s*$")


def _is_table_separator_row(line):
    """True if the line is a GFM header/body separator (|---|:---:|... )."""
    if not _TABLE_ROW_RE.match(line):
        return False
    cells = [c for c in line.strip().strip("|").split("|")]
    if not cells:
        return False
    return all(_TABLE_SEP_CELL_RE.match(c) for c in cells)


def render_table(header_cells, body_rows):
    """Render a GFM table to accessible HTML: real <table> with <thead>/<tbody>,
    <th scope="col"> headers, <th scope="row"> first column, wrapped in a
    horizontal-scroll container for narrow viewports. Cell text is preserved
    verbatim (unicode markers, em-dashes, condition text)."""
    out = [
        '<div class="table-wrap" style="overflow-x:auto;">\n',
        "<table>\n",
        "  <thead>\n    <tr>\n",
    ]
    for c in header_cells:
        out.append('      <th scope="col">%s</th>\n' % render_inline(c.strip()))
    out.append("    </tr>\n  </thead>\n")
    out.append("  <tbody>\n")
    for row in body_rows:
        out.append("    <tr>\n")
        for idx, c in enumerate(row):
            cell = render_inline(c.strip())
            if idx == 0:
                out.append('      <th scope="row">%s</th>\n' % cell)
            else:
                out.append("      <td>%s</td>\n" % cell)
        out.append("    </tr>\n")
    out.append("  </tbody>\n")
    out.append("</table>\n")
    out.append("</div>\n")
    return "".join(out)


def parse_blocks(md_text, raw_html=False):
    """Split markdown body into typed blocks.

    raw_html=True (set when the post's front matter has raw_html: true)
    enables the `<!-- html -->` ... `<!-- /html -->` passthrough fence;
    without it the fence markers are ordinary paragraph text (escaped).
    """
    lines = md_text.split("\n")
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue

        # Raw HTML block (opt-in via front matter flag)
        if raw_html and stripped == "<!-- html -->":
            raw_lines = []
            i += 1
            while i < n and lines[i].strip() != "<!-- /html -->":
                raw_lines.append(lines[i])
                i += 1
            if i < n:  # closing fence found
                i += 1
                blocks.append(("rawhtml", "\n".join(raw_lines)))
                continue
            # Unclosed fence: emit what we have (defensive; well-formed
            # posts always close the fence).

        # Fenced code block
        fence = _FENCE_RE.match(stripped)
        if fence:
            marker = fence.group(1)
            fence_char = marker[0]
            fence_len = len(marker)
            lang = stripped[fence_len:].strip()
            code_lines = []
            i += 1
            close_re = re.compile(r"^" + re.escape(fence_char) + "{" + str(fence_len) + r",}\s*$")
            while i < n and not close_re.match(lines[i].strip()):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            blocks.append(("code", lang, "\n".join(code_lines)))
            continue

        # ATX heading (h2/h3/h4 — h1 is the post title from front matter)
        h = _HEADING_RE.match(stripped)
        if h:
            blocks.append(("heading", len(h.group(1)), h.group(2).strip()))
            i += 1
            continue

        # Blockquote (consecutive `>` lines; bare `>` splits paragraphs)
        if stripped.startswith(">"):
            parts = []
            cur = []
            while i < n and lines[i].strip().startswith(">") and not _TABLE_ROW_RE.match(lines[i].strip()):
                q = re.sub(r"^>\s?", "", lines[i].strip())
                if q == "":
                    if cur:
                        parts.append(" ".join(cur))
                        cur = []
                else:
                    cur.append(q)
                i += 1
            if cur:
                parts.append(" ".join(cur))
            blocks.append(("blockquote", parts))
            continue

        # GFM table (header row + separator row)
        if (
            _TABLE_ROW_RE.match(stripped)
            and i + 1 < n
            and _is_table_separator_row(lines[i + 1])
        ):
            header_cells = [c for c in stripped.strip("|").split("|")]
            i += 2
            body_rows = []
            while i < n and _TABLE_ROW_RE.match(lines[i].strip()) and not _is_table_separator_row(lines[i]):
                body_rows.append([c for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append(("table", header_cells, body_rows))
            continue

        # List (consecutive list-item lines, nesting via indentation)
        if _LIST_ITEM_RE.match(stripped):
            list_lines = []
            while i < n and lines[i].strip() and _LIST_ITEM_RE.match(lines[i].strip()):
                list_lines.append(lines[i])
                i += 1
            blocks.append(("list", list_lines))
            continue

        # Paragraph (until blank line or a new block starter)
        para = []
        while i < n and lines[i].strip():
            s = lines[i].strip()
            if (
                _HEADING_RE.match(s)
                or s.startswith(">")
                or _LIST_ITEM_RE.match(s)
                or _FENCE_RE.match(s)
                or _TABLE_ROW_RE.match(s)
            ):
                break
            para.append(s)
            i += 1
        blocks.append(("para", " ".join(para)))

    return blocks


def render_list(lines):
    """Render (possibly nested) list lines to <ul>/<ol> HTML."""
    items = []
    for raw in lines:
        m = _LIST_ITEM_RE.match(raw)
        if not m:
            continue
        indent = len(m.group(1).expandtabs(4))
        ordered = bool(re.match(r"\d+\.", m.group(2)))
        items.append((indent, ordered, m.group(3)))

    out = []
    stack = []  # each: {"ordered": bool, "indent": int}
    for indent, ordered, content in items:
        while stack and indent < stack[-1]["indent"]:
            out.append("</li>")
            out.append("</ol>" if stack[-1]["ordered"] else "</ul>")
            stack.pop()
        if not stack or indent > stack[-1]["indent"]:
            out.append("<ol>" if ordered else "<ul>")
            stack.append({"ordered": ordered, "indent": indent})
        else:
            out.append("</li>")
        out.append("<li>" + render_inline(content))
    while stack:
        out.append("</li>")
        out.append("</ol>" if stack[-1]["ordered"] else "</ul>")
        stack.pop()
    return "".join(out)


def render_body(md_text, raw_html=False):
    """Render the markdown body (already front-matter-stripped) to HTML."""
    parts = []
    for block in parse_blocks(md_text, raw_html=raw_html):
        kind = block[0]
        if kind == "para":
            parts.append("<p>" + render_inline(block[1]) + "</p>")
        elif kind == "heading":
            level = block[1]
            parts.append("<h%d>%s</h%d>" % (level, render_inline(block[2]), level))
        elif kind == "list":
            parts.append(render_list(block[1]))
        elif kind == "table":
            parts.append(render_table(block[1], block[2]))
        elif kind == "blockquote":
            inner = "".join("<p>%s</p>" % render_inline(p) for p in block[1])
            parts.append("<blockquote>" + inner + "</blockquote>")
        elif kind == "code":
            lang, code = block[1], block[2]
            lang_attr = ' class="language-%s"' % html.escape(lang) if lang else ""
            parts.append(
                "<pre><code%s>%s</code></pre>" % (lang_attr, html.escape(code))
            )
        elif kind == "rawhtml":
            # Pass through verbatim (flagged posts only).
            parts.append(block[1])
    return "\n".join(parts)


def body_plain_text(md_text):
    """Markdown body stripped of markup, for the search index body field."""
    text = re.sub(r"```.*?```", " ", md_text, flags=re.DOTALL)
    # Raw-HTML posts: drop CSS/JS and comments, keep only the text between tags.
    text = re.sub(r"<(style|script)\b.*?</\1\s*>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"^#{2,4}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[ \t]*([-*+]|\d+\.)\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


# ──────────────────────────────────────────────────────────────────────────
# Front matter + post loading
# ──────────────────────────────────────────────────────────────────────────

def parse_frontmatter(text):
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]
            for line in parts[1].strip().split("\n"):
                line = line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                meta[key.strip()] = value
    return meta, body


# Page chrome that build_post_page() already emits. Pasting any of it into a
# raw-HTML fence closes the article early and leaves the rest of the post
# outside .page-wrapper with a second footer, so it fails the build instead.
_FENCE_FORBIDDEN_RE = re.compile(r"</article>|</main>|<footer|page-wrapper", re.I)


def _check_raw_html_fences(name, body):
    for block in parse_blocks(body, raw_html=True):
        if block[0] != "rawhtml":
            continue
        m = _FENCE_FORBIDDEN_RE.search(block[1])
        if m:
            sys.exit(
                "ERROR: %s has page chrome (%s) inside a raw-HTML fence; "
                "the builder adds the page template itself" % (name, m.group(0))
            )


def load_posts():
    posts = []
    if not POSTS_DIR.is_dir():
        return posts
    for path in sorted(POSTS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        missing = [f for f in REQUIRED_FIELDS if not meta.get(f)]
        if missing:
            print(
                "WARN: %s missing front matter fields %s — skipped"
                % (path.name, ", ".join(missing)),
                file=sys.stderr,
            )
            continue
        meta["body_md"] = body.strip()
        meta["tags"] = _parse_tags(meta.get("tags", ""))
        meta["fixture"] = str(meta.get("fixture", "")).lower() in ("true", "1", "yes")
        if meta["fixture"] and (PROD or not os.environ.get("ACEWERK_DEV")):
            print("SKIP: %s is a fixture (set ACEWERK_DEV=1 to include)" % path.name, file=sys.stderr)
            continue
        meta["raw_html"] = str(meta.get("raw_html", "")).lower() in ("true", "1", "yes")
        if meta["raw_html"]:
            _check_raw_html_fences(path.name, body)
        meta["updated"] = (meta.get("updated") or "").strip() or None
        meta["_source"] = path.name
        posts.append(meta)
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def _parse_tags(raw):
    tags = [t.strip() for t in raw.split(",") if t.strip()]
    return tags


# ──────────────────────────────────────────────────────────────────────────
# Derived fields
# ──────────────────────────────────────────────────────────────────────────

def format_date(iso):
    try:
        y, m, d = iso.split("-")
        return "%s %s, %s" % (MONTHS[int(m) - 1], int(d), y)
    except (ValueError, IndexError):
        return iso


# Reading time counts prose only. The `<!-- html -->` … `<!-- /html -->` fence
# carries table markup, CSS and JS (never prose), and the trailing sections below
# are reference material rather than article prose. Posts without these sections
# are unaffected.
READ_TIME_SKIPPED_SECTIONS = ("sources", "references", "notes", "faq")


def _prose_only(body_md):
    """Body markdown minus the parts that are not prose (reading-time input).

    Uses the same fence markers as parse_blocks: everything between
    `<!-- html -->` and `<!-- /html -->` is dropped, and so is every heading
    section named in READ_TIME_SKIPPED_SECTIONS, up to the next `## ` heading.
    """
    kept = []
    in_html = False
    skipping = False
    for line in body_md.split("\n"):
        stripped = line.strip()
        if in_html:
            if stripped == "<!-- /html -->":
                in_html = False
            continue
        if stripped == "<!-- html -->":
            in_html = True
            continue
        if skipping:
            if re.match(r"^##\s", line):
                skipping = False
            else:
                continue
        if re.match(r"^##\s+", line):
            heading = stripped.lstrip("#").strip().rstrip(":").strip().lower()
            if heading in READ_TIME_SKIPPED_SECTIONS:
                skipping = True
                continue
        kept.append(line)
    return "\n".join(kept)


def read_time_minutes(body_md):
    words = len(re.findall(r"\S+", _prose_only(body_md)))
    return max(1, math.ceil(words / 200))


def truncate_excerpt(excerpt, limit=200):
    excerpt = excerpt.strip()
    if len(excerpt) <= limit:
        return excerpt
    return excerpt[: limit - 1].rstrip() + "…"


# ──────────────────────────────────────────────────────────────────────────
# Shared templates (CSS / head / nav / footer / JS)
# ──────────────────────────────────────────────────────────────────────────

CSS = r"""
    :root {
      /* canonical tokens (reused) */
      --canvas: #060912;
      --surface: #0c1122;
      --surface-plus: #11182b;
      --accent: #d49a2e;
      --accent-soft: #f4d39e;
      --ink: #e5e7f0;
      --ink-muted: rgba(190,200,220,0.88);
      --border: rgba(255,255,255,0.08);
      --glass-border: rgba(255,255,255,0.11);
      --rule: rgba(255,255,255,0.09);
      --rule-soft: rgba(255,255,255,0.055);
      --radius-sm: 6px;
      --radius-md: 9px;
      --radius-lg: 14px;
      --transition-fast: 0.18s ease-out;
      --transition-med: 0.3s ease-out;
      --max-width: 1100px;
      --fs-min: 11px;
      --fs-footnote: 10px;

      /* type scale */
      --fs-label:         clamp(11px, 0.6vw + 8px, 12px);
      --fs-body:          clamp(16px, 0.35vw + 14px, 18px);
      --fs-item-title:    clamp(19px, 0.5vw + 16px, 22px);
      --fs-lead:          clamp(22px, 1.2vw + 14px, 30px);
      --fs-section-title: clamp(26px, 1.6vw + 15px, 38px);

      /* blog additions */
      --breakpoint-nav: 768px;
      --nav-height: 52px;
      --nav-height-mobile: 44px;
      --measure-prose: 720px;
      --fs-post-title: clamp(26px, 2.6vw + 14px, 40px);
      --accent-tint: rgba(212,154,46,0.16);
      --accent-border: rgba(212,154,46,0.42);
      --code-bg: rgba(4,6,12,0.55);
      --code-inline-bg: rgba(255,255,255,0.07);

      /* static backdrop */
      --backdrop-base: radial-gradient(140% 160% at 50% 46%, #0a111f 0%, #060a14 55%, #04060c 100%);
      --backdrop-glow-warm-1: rgba(212,154,46,0.10);
      --backdrop-glow-warm-2: rgba(212,154,46,0.07);
      --backdrop-glow-cool: rgba(56,74,120,0.14);
      --backdrop-dots: rgba(255,255,255,0.05);
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { font-size: 15px; scroll-behavior: smooth; }
    body {
      background: var(--canvas);
      color: var(--ink);
      font-family: 'Space Grotesk', system-ui, sans-serif;
      font-weight: 300;
      line-height: 1.6;
    }
    a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 3px;
    }
    .visually-hidden {
      position: absolute; width: 1px; height: 1px;
      margin: -1px; padding: 0; overflow: hidden;
      clip: rect(0 0 0 0); clip-path: inset(50%);
      white-space: nowrap; border: 0;
    }

    /* ══════ STATIC BACKDROP (no canvas, no WebGL) ══════ */
    .blog-backdrop {
      position: fixed; inset: 0;
      z-index: 0;
      overflow: hidden;
      pointer-events: none;
      background: var(--backdrop-base);
    }
    .blog-backdrop::before {
      content: ""; position: absolute; inset: 0;
      background:
        radial-gradient(60% 45% at 78% 8%,  var(--backdrop-glow-warm-1) 0%, rgba(212,154,46,0) 60%),
        radial-gradient(55% 40% at 15% 92%, var(--backdrop-glow-warm-2) 0%, rgba(212,154,46,0) 55%),
        radial-gradient(42% 34% at 50% 50%, var(--backdrop-glow-cool) 0%, rgba(56,74,120,0) 72%);
    }
    .blog-backdrop::after {
      content: ""; position: absolute; inset: 0;
      background-image: radial-gradient(var(--backdrop-dots) 1px, transparent 1px);
      background-size: 32px 32px;
      -webkit-mask-image: radial-gradient(120% 120% at 50% 46%, #000 40%, transparent 95%);
              mask-image: radial-gradient(120% 120% at 50% 46%, #000 40%, transparent 95%);
      pointer-events: none;
    }

    /* ══════ TOP NAVIGATION ══════ */
    .nav-bar {
      display: flex; align-items: center;
      position: fixed; top: 0; left: 0; right: 0; z-index: 50;
      background: linear-gradient(to bottom, rgba(10,15,30,0.72), rgba(6,9,18,0.58));
      backdrop-filter: blur(14px) saturate(1.15);
      -webkit-backdrop-filter: blur(14px) saturate(1.15);
      border-bottom: 1px solid var(--glass-border);
      padding: 0 clamp(20px, 3vw, 40px);
      height: var(--nav-height);
    }
    .nav-logo {
      font-family: 'Orbitron', sans-serif;
      font-weight: 500; font-size: 24px;
      letter-spacing: 0.14em;
      color: var(--accent);
      text-transform: uppercase; text-decoration: none;
      display: flex; align-items: center; gap: 4px;
    }
    .nav-links { display: flex; align-items: center; gap: 24px; }
    .nav-links a {
      position: relative;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 300; font-size: 13px;
      letter-spacing: 0.12em; text-transform: uppercase;
      color: var(--ink-muted); text-decoration: none;
      padding: 2px 0 4px 0;
      transition: color var(--transition-fast);
    }
    .nav-links a::after {
      content: "";
      position: absolute; left: 0; right: 0;
      bottom: -1px;
      height: 1px;
      background: var(--accent);
      transform: scaleX(0);
      transform-origin: center;
      opacity: 0;
      transition: transform var(--transition-fast), opacity var(--transition-fast);
    }
    .nav-links a:hover,
    .nav-links a.active { color: var(--ink); }
    .nav-links a:hover::after,
    .nav-links a.active::after { transform: scaleX(1); opacity: 1; }

    /* Blog nav item — subtle accent dot (not a CTA/badge) */
    .nav-links a.nav-blog::before {
      content: "";
      display: inline-block;
      width: 4px; height: 4px;
      border-radius: 50%;
      background: var(--accent);
      opacity: 0.7;
      margin-right: 7px;
      vertical-align: middle;
      transition: opacity var(--transition-fast);
    }
    .nav-links a.nav-blog:hover::before,
    .nav-links a.nav-blog.active::before {
      opacity: 1;
      box-shadow: 0 0 8px rgba(212,154,46,0.6);
    }

    /* Hamburger trigger */
    .nav-toggle {
      display: none;
      flex-direction: column;
      align-items: center; justify-content: center;
      gap: 3px;
      width: 44px; height: 44px;
      margin-left: auto;
      background: transparent; border: none;
      cursor: pointer; padding: 0;
    }
    .nav-toggle-bar {
      width: 20px; height: 2px;
      background: var(--ink-muted);
      transition: transform var(--transition-med), opacity var(--transition-med), background var(--transition-med);
    }
    .nav-toggle:hover .nav-toggle-bar { background: var(--ink); }
    .nav-toggle.open .nav-toggle-bar { background: var(--accent); }
    .nav-toggle.open .nav-toggle-bar:nth-child(1) { transform: translateY(5px) rotate(45deg); }
    .nav-toggle.open .nav-toggle-bar:nth-child(2) { opacity: 0; }
    .nav-toggle.open .nav-toggle-bar:nth-child(3) { transform: translateY(-5px) rotate(-45deg); }

    body.nav-open { overflow: hidden; }

    .page-wrapper {
      position: relative; z-index: 1;
      padding-top: var(--nav-height);
    }

    .site-container {
      width: 100%; max-width: var(--max-width);
      padding: 0 clamp(20px, 4vw, 48px);
      margin: 0 auto;
    }
    .header-inner-wrapper {
      display: flex; align-items: center; justify-content: space-between;
    }

    /* ══════ HERO ══════ */
    .hero-shell {
      margin-top: clamp(24px, 4vh, 44px);
      margin-bottom: clamp(18px, 3vh, 30px);
    }
    .hero-label {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 400; font-size: var(--fs-label);
      letter-spacing: 0.24em; text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 12px;
    }
    .hero-title {
      font-family: 'Orbitron', sans-serif;
      font-weight: 500;
      font-size: clamp(28px, 4.6vw, 52px);
      line-height: 1.12; letter-spacing: 0.08em;
      color: #ffffff; text-transform: uppercase;
      max-width: 780px;
    }
    .hero-note {
      margin-top: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 400; font-size: var(--fs-label);
      letter-spacing: 0.06em;
      color: var(--ink-muted);
    }

    /* ══════ GLASS SHELL ══════ */
    .content-wrap {
      max-width: var(--max-width);
      margin: 0 auto;
      padding: 0 clamp(20px, 4vw, 48px);
    }
    .content-shell {
      background: linear-gradient(165deg, rgba(12,18,35,0.58), rgba(7,10,20,0.50));
      backdrop-filter: blur(14px) saturate(1.15);
      -webkit-backdrop-filter: blur(14px) saturate(1.15);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-lg);
      box-shadow: 0 8px 32px rgba(0,0,0,0.45),
                  inset 0 1px 0 rgba(255,255,255,0.08);
      padding: clamp(26px, 4vw, 56px) clamp(22px, 4vw, 56px);
    }
    @supports not (backdrop-filter: blur(1px)) {
      .content-shell, .nav-bar, .footer-bar, .post-card {
        background: linear-gradient(165deg, rgba(11,16,32,0.94), rgba(7,10,20,0.92));
      }
    }

    /* ══════ BLOG TOOLBAR (search + page size) ══════ */
    .blog-toolbar {
      display: flex; align-items: center; justify-content: space-between;
      gap: 16px; flex-wrap: wrap; margin-bottom: 24px;
    }
    .blog-search { position: relative; display: flex; align-items: center; flex: 1 1 260px; min-width: 0; }
    .blog-search-icon {
      position: absolute; left: 14px; width: 16px; height: 16px;
      color: var(--ink-muted); pointer-events: none;
    }
    .blog-search-input {
      width: 100%; height: 48px;
      padding: 0 44px;
      background: rgba(12,18,35,0.4);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      color: var(--ink);
      font-family: 'Space Grotesk', sans-serif; font-weight: 300;
      font-size: var(--fs-body);
      transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
    }
    .blog-search-input::-webkit-search-cancel-button { -webkit-appearance: none; appearance: none; }
    .blog-search-input::placeholder { color: var(--ink-muted); }
    .blog-search-input:focus {
      border-color: var(--accent-border);
      box-shadow: 0 0 0 3px var(--accent-tint);
      outline: none;
    }
    .blog-search-clear {
      position: absolute; right: 8px;
      width: 32px; height: 32px;
      display: flex; align-items: center; justify-content: center;
      background: none; border: none; border-radius: var(--radius-sm);
      color: var(--ink-muted); font-size: 20px; line-height: 1;
      cursor: pointer;
      transition: color var(--transition-fast), background var(--transition-fast);
    }
    .blog-search-clear:hover { color: var(--ink); background: rgba(255,255,255,0.06); }

    .page-size-wrap { display: flex; align-items: center; gap: 10px; }
    .page-size-label {
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.06em;
      color: var(--ink-muted);
    }
    .page-size-select {
      height: 40px; padding: 0 12px;
      background: rgba(12,18,35,0.4);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      color: var(--ink);
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: 13px;
    }

    /* ══════ STATUS ══════ */
    .blog-status {
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.06em;
      color: var(--ink-muted); margin-bottom: 20px;
    }
    .status-clear {
      background: none; border: none; padding: 0; margin-left: 8px;
      color: var(--accent); cursor: pointer;
      font-family: inherit; font-size: inherit; letter-spacing: inherit;
      text-decoration: underline; text-underline-offset: 3px;
    }
    .status-clear:hover { color: var(--accent-soft); }
    .blog-empty { color: var(--ink-muted); }

    /* ══════ POST GRID + CARD ══════ */
    .post-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 24px;
    }
    .post-card {
      position: relative;
      display: flex; flex-direction: column;
      gap: 14px;
      padding: 24px;
      background: linear-gradient(165deg, rgba(12,18,35,0.58), rgba(7,10,20,0.50));
      backdrop-filter: blur(14px) saturate(1.15);
      -webkit-backdrop-filter: blur(14px) saturate(1.15);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-lg);
      box-shadow: 0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.08);
      transition: transform var(--transition-med), border-color var(--transition-med), box-shadow var(--transition-med);
    }
    .post-card:hover {
      transform: translateY(-3px);
      border-color: var(--accent-border);
      box-shadow: 0 14px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(212,154,46,0.18), inset 0 1px 0 rgba(255,255,255,0.10);
    }
    .post-card:hover .post-card-title { color: var(--accent-soft); }
    .post-card:active {
      transform: translateY(0);
      box-shadow: 0 2px 4px rgba(0,0,0,0.35), inset 0 2px 4px rgba(0,0,0,0.3);
    }
    .post-card-title {
      font-family: 'Rajdhani', sans-serif; font-weight: 500;
      font-size: var(--fs-item-title);
      line-height: 1.25;
      color: #ffffff;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
      min-height: calc(1.25em * 2);
    }
    .post-card-link { color: inherit; text-decoration: none; }
    .post-card-link::after {
      content: ""; position: absolute; inset: 0;
      border-radius: inherit;
    }
    .post-card-excerpt {
      font-family: 'Space Grotesk', sans-serif; font-weight: 300;
      font-size: var(--fs-body);
      color: var(--ink-muted);
      line-height: 1.7;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 3;
      overflow: hidden;
    }
    .post-card-meta {
      display: flex; align-items: baseline; justify-content: space-between; flex-wrap: nowrap; gap: 14px;
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.06em;
    }
    .post-card-date { color: var(--accent); }
    .post-card-read { color: var(--ink-muted); white-space: nowrap; }
    .post-card-author {
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.06em;
      color: var(--ink-muted);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      max-width: 100%;
    }
    .post-card-tags { display: flex; flex-wrap: wrap; gap: 6px; }
    .post-card-tag {
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label);
      text-transform: uppercase; letter-spacing: 0.08em;
      color: var(--ink-muted);
      padding: 3px 8px;
      border: 1px solid var(--rule);
      border-radius: var(--radius-sm);
    }
    .post-card-tag.post-card-fixture {
      color: var(--accent-soft);
      border-color: var(--accent-border);
    }

    /* ══════ PAGINATION ══════ */
    .pagination {
      display: flex; justify-content: center; align-items: center;
      gap: 8px; margin-top: 28px;
    }
    .pagination-btn {
      min-width: 36px; height: 36px; padding: 0 10px;
      display: inline-flex; align-items: center; justify-content: center;
      background: rgba(12,18,35,0.4);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      color: var(--ink-muted);
      font-family: 'JetBrains Mono', monospace; font-weight: 400; font-size: 13px;
      cursor: pointer;
      transition: color var(--transition-fast), border-color var(--transition-fast), background var(--transition-fast);
    }
    .pagination-btn:hover:not(:disabled):not(.is-current) {
      color: var(--ink); border-color: var(--accent-border);
    }
    .pagination-btn.is-current {
      background: var(--accent-tint);
      border-color: var(--accent-border);
      color: var(--accent-soft);
      cursor: default;
    }
    .pagination-btn:disabled { opacity: 0.38; cursor: default; pointer-events: none; }
    .pagination-ellipsis { color: var(--ink-muted); padding: 0 2px; }

    /* ══════ POST PAGE ══════ */
    .post-header { margin-bottom: 2em; }
    .post-header-top {
      display: flex; align-items: center; justify-content: space-between;
      flex-wrap: nowrap; gap: 12px; margin-bottom: 0.5em; min-width: 0;
    }
    .post-back {
      display: inline-block; flex: 0 0 auto;
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.1em; text-transform: uppercase;
      color: var(--accent); text-decoration: none; white-space: nowrap;
    }
    .post-back:hover { color: var(--accent-soft); }
    .post-date {
      flex: 0 0 auto;
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.06em;
      color: var(--accent); white-space: nowrap;
    }
    .post-title {
      font-family: 'Rajdhani', sans-serif; font-weight: 500;
      font-size: var(--fs-post-title);
      line-height: 1.12; letter-spacing: 0.02em;
      color: #ffffff;
      margin: 0 0 0.5em;
    }
    .post-byline {
      display: flex; align-items: baseline; justify-content: space-between;
      flex-wrap: nowrap; gap: 12px;
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.06em;
      color: var(--ink-muted);
    }
    .post-read { white-space: nowrap; }

    .fixture-note {
      margin: 0 0 2em;
      padding: 12px 16px;
      border: 1px solid var(--accent-border);
      border-radius: var(--radius-md);
      background: var(--accent-tint);
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: var(--fs-label); letter-spacing: 0.06em;
      color: var(--accent-soft);
    }

    /* ══════ LONG-FORM PROSE ══════ */
    .post-body {
      color: var(--ink);
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 300;
      font-size: var(--fs-body);
      line-height: 1.75;
    }
    .post-body h2 {
      font-family: 'Rajdhani', sans-serif; font-weight: 500;
      font-size: var(--fs-section-title);
      line-height: 1.15; letter-spacing: 0.04em;
      color: #ffffff;
      margin: 2.5em 0 0.6em;
    }
    .post-body h3 {
      font-family: 'Rajdhani', sans-serif; font-weight: 500;
      font-size: var(--fs-lead);
      line-height: 1.2; letter-spacing: 0.03em;
      color: #ffffff;
      margin: 2em 0 0.55em;
    }
    .post-body h4 {
      font-family: 'Space Grotesk', sans-serif; font-weight: 500;
      font-size: var(--fs-item-title);
      line-height: 1.3; letter-spacing: 0.01em;
      color: var(--accent-soft);
      margin: 1.75em 0 0.5em;
    }
    .post-body p { margin: 0 0 1.25em; }
    .post-body p:last-child { margin-bottom: 0; }
    .post-body ul, .post-body ol { margin: 0 0 1.25em; padding-left: 1.5em; }
    .post-body li { margin: 0.35em 0; }
    .post-body li::marker { color: var(--accent); font-family: 'JetBrains Mono', monospace; }
    .post-body ul { list-style: disc; }
    .post-body ol { list-style: decimal; }
    .post-body blockquote {
      margin: 1.75em 0;
      padding: 0.25em 0 0.25em 1.5em;
      border-left: 2px solid var(--accent);
      color: var(--ink);
      background: rgba(255,255,255,0.02);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    }
    .post-body blockquote p { margin: 0; }
    .post-body a {
      color: var(--accent);
      text-decoration: underline;
      text-decoration-color: rgba(212,154,46,0.45);
      text-underline-offset: 3px;
      text-decoration-thickness: 1px;
      transition: color var(--transition-fast);
    }
    .post-body a:hover { color: var(--accent-soft); }
    .post-body code {
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: 0.85em;
      color: var(--accent-soft);
      background: var(--code-inline-bg);
      padding: 0.15em 0.45em;
      border-radius: var(--radius-sm);
      border: 1px solid var(--rule);
    }
    .post-body pre {
      margin: 1.5em 0;
      padding: 1.25em 1.5em;
      background: var(--code-bg);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      overflow-x: auto;
      tab-size: 2;
    }
    .post-body pre code {
      display: block;
      font-family: 'JetBrains Mono', monospace; font-weight: 400;
      font-size: 0.9em; line-height: 1.6;
      color: var(--ink);
      background: none; border: none; padding: 0;
    }
    .post-body figure { margin: 2em 0; }
    .post-body figure img {
      display: block; width: 100%; height: auto;
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
    }
    .post-body figcaption {
      margin-top: 0.6em;
      font-family: 'Space Grotesk', sans-serif; font-weight: 300;
      font-size: var(--fs-label); line-height: 1.5;
      color: var(--ink-muted);
      text-align: center; letter-spacing: 0.04em;
    }
    .post-body hr { border: none; border-top: 1px solid var(--rule); margin: 2.5em 0; }
    /* ══════ COVERAGE TABLES (GFM) ══════ */
    .table-wrap {
      margin: 1.75em 0;
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      background: rgba(255,255,255,0.02);
      -webkit-overflow-scrolling: touch;
    }
    .table-wrap table {
      border-collapse: collapse;
      width: max-content;
      min-width: 100%;
      font-family: 'Space Grotesk', system-ui, sans-serif;
      font-weight: 300;
      font-size: 0.92em;
      line-height: 1.5;
      color: var(--ink);
    }
    .table-wrap th, .table-wrap td {
      padding: 8px 12px;
      border-bottom: 1px solid var(--rule-soft);
      text-align: left;
      vertical-align: top;
      white-space: nowrap;
    }
    .table-wrap thead th {
      font-family: 'Rajdhani', sans-serif;
      font-weight: 500;
      font-size: 0.95em;
      letter-spacing: 0.03em;
      color: #ffffff;
      background: var(--surface-plus);
      border-bottom: 1px solid var(--accent-border);
    }
    .table-wrap th[scope="row"] {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 400;
      font-size: 0.85em;
      letter-spacing: 0.02em;
      color: var(--accent-soft);
      background: var(--surface);
      white-space: normal;
      min-width: 180px;
    }
    .table-wrap tbody tr:last-child th,
    .table-wrap tbody tr:last-child td { border-bottom: none; }
    .table-wrap tbody tr:hover td, .table-wrap tbody tr:hover th { background: rgba(255,255,255,0.025); }

    /* ══════ FOOTER ══════ */
    .site-footer {
      max-width: var(--max-width);
      margin: 0 auto;
      padding: clamp(14px, 2vw, 22px) clamp(20px, 4vw, 48px) clamp(18px, 3vw, 28px);
    }
    .footer-bar {
      background: linear-gradient(165deg, rgba(12,18,35,0.58), rgba(7,10,20,0.50));
      backdrop-filter: blur(14px) saturate(1.15);
      -webkit-backdrop-filter: blur(14px) saturate(1.15);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      box-shadow: 0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.08);
      padding: 13px 20px;
      text-align: center;
    }
    .footer-text {
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 300; font-size: 11px;
      letter-spacing: 0.14em; text-transform: uppercase;
      color: rgba(200,210,228,0.8);
    }

    @keyframes fade-up {
      from { opacity: 0; transform: translateY(8px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .reveal { animation: fade-up 0.3s ease-out both; }

    /* ══════ RESPONSIVE ══════ */
    @media (max-width: 768px) {
      .nav-bar { height: var(--nav-height-mobile); }
      .nav-logo { font-size: 14px; }
      .nav-toggle { display: inline-flex; }
      .nav-links {
        position: fixed; top: var(--nav-height-mobile); left: 0; right: 0; z-index: 49;
        display: none;
        flex-direction: column; align-items: stretch; gap: 0;
        background: #060912;
        backdrop-filter: blur(14px) saturate(1.15);
        -webkit-backdrop-filter: blur(14px) saturate(1.15);
        border-bottom: 1px solid var(--glass-border);
        padding: 12px 20px 20px;
      }
      .nav-links.open { display: flex; }
      .nav-links a {
        display: flex; align-items: center;
        min-height: 48px;
        font-weight: 400; font-size: 16px;
        border-top: 1px solid var(--rule-soft);
        padding: 0;
      }
      .nav-links a:first-child { border-top: 0; }
      .nav-links a.active { color: var(--accent-soft); }
      .nav-links a::after { display: none; }
      .page-wrapper { padding-top: var(--nav-height-mobile); }
    }
    @media (min-width: 769px) {
      .nav-toggle { display: none; }
    }

    /* ══════ REDUCED MOTION ══════ */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
      .post-card:hover { transform: none; }
      .nav-toggle-bar { transition: none; }
      .nav-links { transition: none; }
    }

    /* ══════ THE BACKDROP — nebula field, full page, fixed ══════
       Same DNA as /services/ and /contact/: identical tile pitch,
       crystal-facet shader and colour grade. Only the baked art and
       the motion recipe differ — quiet, edge-weighted, dark centre. */
    .mosaic-backdrop {
      position: fixed; inset: 0; z-index: 0;
      background: radial-gradient(120% 120% at 50% 50%, #08101f 0%, #060a16 55%, #04060c 100%);
      pointer-events: none;   /* pointer is read at window level */
    }
    .mosaic-backdrop canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
    /* reading scrim: the centre lane stays calm under the copy */
    .mosaic-backdrop::after {
      content: ""; position: absolute; inset: 0;
      background: radial-gradient(60% 70% at 50% 50%, rgba(6,9,18,0.34) 0%, rgba(6,9,18,0.10) 55%, rgba(6,9,18,0) 100%);
    }
    @media print { .mosaic-backdrop { display: none; } }
"""


def render_head(title, canonical=None, description=None, jsonld=""):
    parts = [
        "<!doctype html>\n",
        '<html lang="en">\n',
        "<head>\n",
        '  <meta charset="utf-8">\n',
        '  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n',
        PROD_ANALYTICS if PROD else '  <meta name="robots" content="noindex, nofollow">\n',
        "  <title>" + html.escape(title) + "</title>\n",
        '  <link rel="icon" href="/favicon.ico" sizes="any">\n',
        '  <link rel="icon" href="/assets/icons/acewerk-logo.svg" type="image/svg+xml">\n',
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">\n',
    ]
    if description:
        parts.append(
            '  <meta name="description" content="' + html.escape(description, quote=True) + '">\n'
        )
        parts.append(
            '  <meta property="og:type" content="article">\n'
            '  <meta property="og:title" content="' + html.escape(title, quote=True) + '">\n'
            '  <meta property="og:description" content="' + html.escape(description, quote=True) + '">\n'
        )
    if canonical:
        parts.append('  <link rel="canonical" href="' + canonical + '">\n')
    parts += [
        '  <link rel="preload" href="/assets/fonts/orbitron-500-latin.woff2" as="font" type="font/woff2" crossorigin>\n',
        '  <link rel="preload" href="/assets/fonts/space-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>\n',
        '  <link rel="preload" href="/assets/fonts/rajdhani-500-latin.woff2" as="font" type="font/woff2" crossorigin>\n',
        '  <link rel="preload" href="/assets/fonts/jetbrains-mono-latin.woff2" as="font" type="font/woff2" crossorigin>\n',
        '  <link rel="stylesheet" href="/assets/fonts/fonts.css">\n',
        "  <style>\n",
        CSS,
        "  </style>\n",
        jsonld,
        "</head>\n",
    ]
    return "".join(parts)


def render_nav(active="blog"):
    """Render the shared nav; `active` is the slug key ('services', 'our-team',
    'contact', 'blog', or None)."""
    items = [
        ("services", "/services/", "Services", ""),
        ("our-team", "/our-team/", "Our Team", ""),
        ("contact", "/contact/", "Contact", ""),
        ("blog", "/blog/", "Blog", " nav-blog"),
    ]
    links = []
    for key, href, label, extra in items:
        cls = extra.strip()
        is_active = key == active
        if is_active:
            cls = (cls + " active").strip()
        attrs = ' href="%s"' % href
        if cls:
            attrs += ' class="%s"' % cls
        if is_active:
            attrs += ' aria-current="page"'
        links.append("      <a" + attrs + ">%s</a>" % label)
    return (
        '  <header class="nav-bar" role="banner">\n'
        '    <div class="header-inner-wrapper site-container">\n'
        '      <a href="/" class="nav-logo" aria-label="Ace Werk home">Ace Werk</a>\n'
        '      <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"\n'
        '              aria-label="Open menu" type="button">\n'
        '        <span class="nav-toggle-bar" aria-hidden="true"></span>\n'
        '        <span class="nav-toggle-bar" aria-hidden="true"></span>\n'
        '        <span class="nav-toggle-bar" aria-hidden="true"></span>\n'
        '      </button>\n'
        '      <nav class="nav-links" id="site-nav" role="navigation" aria-label="Main navigation">\n'
        + "\n".join(links)
        + "\n"
        "      </nav>\n"
        "    </div>\n"
        "  </header>\n"
    )


FOOTER = (
    '    <footer class="site-footer" role="contentinfo">\n'
    '      <div class="footer-bar">\n'
    '        <p class="footer-text">&copy; Ace Werk 2026. All rights reserved.</p>\n'
    "      </div>\n"
    "    </footer>\n"
)


NAV_JS = r"""
<script>
(function(){
  "use strict";
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!toggle || !nav) return;
  var links = nav.querySelectorAll('a');
  var first = links[0];
  var last = links[links.length - 1];
  var logo = document.querySelector('.nav-logo');

  function isOpen(){ return toggle.classList.contains('open'); }
  function openMenu(){
    toggle.classList.add('open');
    nav.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close menu');
    document.body.classList.add('nav-open');
    if (logo) logo.setAttribute('tabindex', '-1');
    if (first) first.focus();
  }
  function closeMenu(){
    toggle.classList.remove('open');
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    document.body.classList.remove('nav-open');
    if (logo) logo.removeAttribute('tabindex');
    toggle.focus();
  }

  toggle.addEventListener('click', function(){ isOpen() ? closeMenu() : openMenu(); });

  document.addEventListener('keydown', function(e){
    if (!isOpen()) return;
    if (e.key === 'Escape') { e.preventDefault(); closeMenu(); return; }
    if (e.key === 'Tab') {
      if (e.shiftKey && (document.activeElement === toggle || document.activeElement === first)) {
        e.preventDefault(); if (last) last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); toggle.focus();
      }
    }
  });

  document.addEventListener('click', function(e){
    if (!isOpen()) return;
    if (nav.contains(e.target) || toggle.contains(e.target)) return;
    closeMenu();
  });

  nav.addEventListener('click', function(e){
    if (e.target.closest && e.target.closest('a')) closeMenu();
  });
})();
</script>
"""


SEARCH_ICON = (
    '<svg viewBox="0 0 16 16" width="16" height="16" fill="none" '
    'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
    'aria-hidden="true"><circle cx="7" cy="7" r="5"></circle>'
    '<line x1="11" y1="11" x2="14" y2="14"></line></svg>'
)


def render_card(post):
    tags = post["tags"]
    tag_spans = []
    for t in tags[:3]:
        tag_spans.append('<span class="post-card-tag">%s</span>' % html.escape(t))
    if len(tags) > 3:
        tag_spans.append('<span class="post-card-tag">+%d</span>' % (len(tags) - 3))
    if post.get("fixture"):
        tag_spans.append('<span class="post-card-tag post-card-fixture">Fixture</span>')
    tags_html = ""
    if tag_spans:
        tags_html = '\n    <div class="post-card-tags">%s</div>' % " ".join(tag_spans)

    date_iso = post["date"]
    slug = post["slug"]
    title = html.escape(post["title"])
    excerpt = html.escape(truncate_excerpt(post["excerpt"]))
    author = html.escape(post["author"])
    read_time = post["read_time"]
    dt = html.escape(date_iso)
    dstr = html.escape(format_date(date_iso))

    parts = [
        '<article class="post-card">\n',
        '  <div class="post-card-meta">\n',
        '    <span class="post-card-date"><time datetime="' + dt + '">' + dstr + "</time></span>\n",
        '    <span class="post-card-read">' + str(read_time) + " min read</span>\n",
        "  </div>\n",
        '  <h3 class="post-card-title">\n',
        '    <a class="post-card-link" href="/blog/' + slug + '/">' + title + "</a>\n",
        "  </h3>\n",
        '  <p class="post-card-excerpt">' + excerpt + "</p>\n",
        '  <div class="post-card-author">By ' + author + "</div>\n",
        (tags_html + "\n") if tags_html else "",
        "</article>",
    ]
    return "".join(parts)


# ──────────────────────────────────────────────────────────────────────────
# Page builders
# ──────────────────────────────────────────────────────────────────────────

def build_index_page(posts, index_json, inline_index):
    title = "Blog — Journal | Ace Werk"
    cards = "\n".join(render_card(p) for p in posts)

    if posts:
        initial_status = "%d %s" % (len(posts), "posts" if len(posts) != 1 else "post")
        grid_html = (
            '    <div class="post-grid" id="post-grid">\n'
            + "\n".join("    " + c for c in cards.split("\n"))
            + "\n    </div>"
        )
        empty_html = ""
    else:
        initial_status = "No posts yet."
        grid_html = '    <p class="blog-empty">No posts yet.</p>'
        empty_html = ""

    hero_note = (
        '        <p class="hero-note">Developer fixtures — sample posts for staging QA. Not published content.</p>\n'
        if any(p.get("fixture") for p in posts)
        else ""
    )

    if inline_index:
        inline_script = (
            '  <script type="application/json" id="search-index">'
            + index_json.replace("</", "<\\/")   # never close the script early
            + "</script>\n"
        )
    else:
        inline_script = ""

    toolbar = "".join([
        '    <div class="blog-toolbar" hidden>\n',
        '      <form class="blog-search" role="search" aria-label="Search posts">\n',
        '        <label class="visually-hidden" for="blog-search-input">Search posts</label>\n',
        '        <span class="blog-search-icon" aria-hidden="true">' + SEARCH_ICON + "</span>\n",
        '        <input id="blog-search-input" class="blog-search-input" type="search"\n',
        '               autocomplete="off" spellcheck="false" placeholder="Search posts&hellip;"\n',
        '               aria-label="Search posts" />\n',
        '        <button class="blog-search-clear" type="button" aria-label="Clear search" hidden>&times;</button>\n',
        "      </form>\n",
        '      <div class="page-size-wrap">\n',
        '        <label class="page-size-label" for="page-size">Posts per page</label>\n',
        '        <select id="page-size" class="page-size-select">\n',
        '          <option value="5" selected>5</option>\n',
        '          <option value="10">10</option>\n',
        '          <option value="20">20</option>\n',
        "        </select>\n",
        "      </div>\n",
        "    </div>\n",
    ])

    page = (
        render_head(title, canonical="https://acewerk.com/blog/")
        + "<body>\n"
        '  <div class="mosaic-backdrop" aria-hidden="true"><canvas id="mosaic-blog"></canvas></div>\n'
        + render_nav("blog")
        + '  <div class="page-wrapper">\n'
        "    <main>\n"
        '      <div class="content-wrap site-container">\n'
        '        <div class="content-shell hero-shell reveal">\n'
        '          <div class="hero-label">Journal</div>\n'
        '          <h1 class="hero-title">Blog</h1>\n'
        + hero_note
        + "        </div>\n"
        "      </div>\n"
        '      <div class="content-wrap site-container">\n'
        '        <div class="content-shell reveal">\n'
        + toolbar
        + '          <div class="blog-status" role="status" aria-live="polite">'
        + html.escape(initial_status)
        + "</div>\n"
        + grid_html
        + "\n"
        '          <nav class="pagination" aria-label="Pagination" hidden></nav>\n'
        "        </div>\n"
        "      </div>\n"
        "    </main>\n"
        + FOOTER
        + "  </div>\n"
        + inline_script
        + INDEX_JS
        + NAV_JS
        + '<script src="/blog/assets/tessera-blog.js"></script>\n'
        + "</body>\n</html>\n"
    )
    return page


def _post_jsonld(post):
    """Post-scoped JSON-LD (Article + Person + BreadcrumbList) for posts that opt in
    via the optional 'description' front-matter field. Other pages stay byte-identical."""
    if not (post.get("description") or "").strip():
        return ""
    base = "https://acewerk.com/blog/" + post["slug"] + "/"
    article = {
        "@type": "Article",
        "headline": post["title"],
        "description": post["description"],
        "mainEntityOfPage": base,
        "datePublished": post["date"],
    }
    if post.get("updated"):
        article["dateModified"] = post["updated"]
    article["author"] = {"@type": "Person", "name": post["author"]}
    data = {
        "@context": "https://schema.org",
        "@graph": [
            article,
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acewerk.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://acewerk.com/blog/"},
                    {"@type": "ListItem", "position": 3, "name": post["title"], "item": base},
                ],
            },
        ],
    }
    return (
        '  <script type="application/ld+json">\n'
        "  " + json.dumps(data, ensure_ascii=False)
        + "\n  </script>\n"
    )


def build_post_page(post):
    title = "%s — Blog | Ace Werk" % post["title"]
    body_html = render_body(post["body_md"], raw_html=post.get("raw_html", False))
    description = (post.get("description") or "").strip() or None
    jsonld = _post_jsonld(post)
    title_esc = html.escape(post["title"])
    author_esc = html.escape(post["author"])
    date_esc = html.escape(post["date"])
    dstr = html.escape(format_date(post["date"]))
    # Header shows the publish date only; the update date opens the post body.
    if post.get("updated"):
        updated_html = (
            '              <p class="post-updated">Last updated <time datetime="'
            + html.escape(post["updated"])
            + '">'
            + html.escape(format_date(post["updated"]))
            + "</time></p>\n"
        )
    else:
        updated_html = ""
    read_time = post["read_time"]
    fixture_note = (
        '    <div class="fixture-note">Fixture &mdash; sample post for staging QA. Not published content.</div>\n'
        if post.get("fixture")
        else ""
    )
    parts = [
        render_head(title, canonical="https://acewerk.com/blog/" + post["slug"] + "/", description=description, jsonld=jsonld),
        "<body>\n",
        '  <div class="mosaic-backdrop" aria-hidden="true"><canvas id="mosaic-blog"></canvas></div>\n',
        render_nav("blog"),
        '  <div class="page-wrapper">\n',
        "    <main>\n",
        '      <div class="content-wrap site-container">\n',
        '        <div class="content-shell hero-shell reveal">\n',
        "          <article>\n",
        '            <header class="post-header">\n',
        '              <div class="post-header-top">\n',
        '                <a class="post-back" href="/blog/">&larr; Blog</a>\n',
        '                <time class="post-date" datetime="' + date_esc + '">' + dstr + "</time>\n",
        "              </div>\n",
        "              <h1 class=\"post-title\">" + title_esc + "</h1>\n",
        '              <div class="post-byline">\n',
        "                <span>By " + author_esc + "</span>\n",
        "                <span class=\"post-read\">" + str(read_time) + " min read</span>\n",
        "              </div>\n",
        "            </header>\n",
        fixture_note,
        '            <div class="post-body">\n',
        updated_html,
        body_html,
        "\n",
        "            </div>\n",
        "          </article>\n",
        "        </div>\n",
        "      </div>\n",
        "    </main>\n",
        FOOTER,
        "  </div>\n",
        NAV_JS,
        '<script src="/blog/assets/tessera-blog.js"></script>\n',
        "</body>\n</html>\n",
    ]
    return "".join(parts)


def build_search_index(posts):
    entries = []
    for p in posts:
        entries.append(
            {
                "title": p["title"],
                "excerpt": truncate_excerpt(p["excerpt"]),
                "author": p["author"],
                "date": p["date"],
                "slug": p["slug"],
                "body": body_plain_text(p["body_md"]),
            }
        )
    return entries


# ──────────────────────────────────────────────────────────────────────────
# Client-side search + pagination JS
# ──────────────────────────────────────────────────────────────────────────

INDEX_JS = r"""
<script>
(function(){
  "use strict";
  var toolbar = document.querySelector('.blog-toolbar');
  var pagination = document.querySelector('.pagination');
  var pageSizeWrap = document.querySelector('.page-size-wrap');
  var searchForm = document.querySelector('.blog-search');
  var searchInput = document.getElementById('blog-search-input');
  var searchClear = document.querySelector('.blog-search-clear');
  var pageSize = document.getElementById('page-size');
  var statusEl = document.querySelector('.blog-status');
  var grid = document.getElementById('post-grid');
  var cards = grid ? Array.prototype.slice.call(grid.querySelectorAll('.post-card')) : [];

  if (toolbar) toolbar.hidden = false;          // toolbar stays visible (search lives here)
  var showControls = cards.length > 5;
  if (pageSizeWrap) { pageSizeWrap.hidden = !showControls; pageSizeWrap.style.display = showControls ? '' : 'none'; }
  if (pagination) { pagination.hidden = !showControls; pagination.style.display = showControls ? '' : 'none'; }

  // ---- search index: inline when small, lazy on first focus when large ----
  var INDEX = [];
  var NORM = null;
  var inlineEl = document.getElementById('search-index');
  function normalize(list) {
    return list.map(function(p){
      return [p.title, p.excerpt, p.author, String(p.date), p.slug, p.body]
        .map(function(s){ return String(s == null ? '' : s).toLowerCase(); });
    });
  }
  function loadIndex() {
    fetch('/blog/search-index.json', { credentials: 'same-origin' })
      .then(function(r){ return r.ok ? r.json() : []; })
      .then(function(data){ INDEX = data; NORM = normalize(data); applyState(); })
      .catch(function(){ INDEX = []; NORM = []; applyState(); });
  }
  if (inlineEl) {
    try { INDEX = JSON.parse(inlineEl.textContent); } catch(e) { INDEX = []; }
    NORM = normalize(INDEX);
  } else if (searchInput) {
    searchInput.addEventListener('focus', loadIndex, { once: true });
  }

  // ---- URL state ----
  function readState() {
    var p = new URLSearchParams(location.search);
    var q = (p.get('q') || '').trim();
    var size = parseInt(p.get('size') || '5', 10);
    if ([5, 10, 20].indexOf(size) < 0) size = 5;
    var page = parseInt(p.get('page') || '1', 10);
    if (!(page >= 1)) page = 1;
    return { q: q, size: size, page: page };
  }
  function writeState(s) {
    var p = new URLSearchParams();
    if (s.q) p.set('q', s.q);
    if (s.size !== 5) p.set('size', String(s.size));
    if (s.page > 1) p.set('page', String(s.page));
    var qs = p.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
  }

  // ---- matching: every token (>=2 chars) is a substring of some field ----
  function tokenize(q) {
    return q.toLowerCase().split(/\s+/).filter(function(t){ return t.length >= 2; });
  }
  function matchesPost(idx, tokens) {
    if (!tokens.length) return true;
    var fields = NORM[idx];
    for (var i = 0; i < tokens.length; i++) {
      var found = false;
      for (var j = 0; j < fields.length; j++) {
        if (fields[j].indexOf(tokens[i]) !== -1) { found = true; break; }
      }
      if (!found) return false;
    }
    return true;
  }

  // ---- render ----
  function applyState() {
    var s = readState();
    var tokens = tokenize(s.q);
    var filtered = [];
    for (var i = 0; i < cards.length; i++) {
      var show = NORM === null ? true : matchesPost(i, tokens);
      if (show) filtered.push(cards[i]);
    }
    var total = filtered.length;
    var pageCount = Math.max(1, Math.ceil(total / s.size));
    if (s.page > pageCount) s.page = pageCount;
    var start = (s.page - 1) * s.size;
    var end = start + s.size;
    for (var i = 0; i < cards.length; i++) {
      var visible = false;
      for (var k = start; k < end && k < filtered.length; k++) {
        if (filtered[k] === cards[i]) { visible = true; break; }
      }
      cards[i].style.display = visible ? '' : 'none';
    }
    if (searchInput && searchInput.value !== s.q) searchInput.value = s.q;
    if (searchClear) searchClear.hidden = !s.q;
    if (pageSize) pageSize.value = String(s.size);
    writeState(s);
    renderStatus(total, s.q);
    renderPagination(pageCount, s.page);
  }

  function renderStatus(total, q) {
    if (cards.length === 0) { statusEl.textContent = 'No posts yet.'; return; }
    if (total === 0) {
      statusEl.textContent = '';
      statusEl.appendChild(document.createTextNode('No posts match \u201c' + q + '\u201d. '));
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'status-clear';
      btn.textContent = 'Clear search';
      btn.addEventListener('click', clearSearch);
      statusEl.appendChild(btn);
      return;
    }
    statusEl.textContent = total + (total === 1 ? ' post' : ' posts');
  }

  function renderPagination(count, current) {
    if (!pagination) return;
    pagination.innerHTML = '';
    if (count <= 1) return;
    function btn(label, page, opts) {
      opts = opts || {};
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pagination-btn' + (opts.current ? ' is-current' : '');
      b.textContent = label;
      if (opts.current) b.setAttribute('aria-current', 'page');
      if (opts.disabled) b.disabled = true;
      if (opts.ariaLabel) b.setAttribute('aria-label', opts.ariaLabel);
      if (!opts.disabled && !opts.current) b.addEventListener('click', function(){ setPage(page); });
      return b;
    }
    function ellipsis() {
      var s = document.createElement('span');
      s.className = 'pagination-ellipsis';
      s.setAttribute('aria-hidden', 'true');
      s.textContent = '\u2026';
      return s;
    }
    pagination.appendChild(btn('\u2190', current - 1, { disabled: current === 1, ariaLabel: 'Previous page' }));
    pageList(count, current).forEach(function(p){
      if (p === '...') pagination.appendChild(ellipsis());
      else pagination.appendChild(btn(String(p), p, { current: p === current }));
    });
    pagination.appendChild(btn('\u2192', current + 1, { disabled: current === count, ariaLabel: 'Next page' }));
  }

  function pageList(count, current) {
    if (count <= 7) {
      var a = []; for (var i = 1; i <= count; i++) a.push(i); return a;
    }
    var pages = [1];
    var lo = Math.max(2, current - 1);
    var hi = Math.min(count - 1, current + 1);
    if (lo > 2) pages.push('...');
    for (var i = lo; i <= hi; i++) pages.push(i);
    if (hi < count - 1) pages.push('...');
    pages.push(count);
    return pages;
  }

  // ---- events ----
  function setPage(p) { var s = readState(); s.page = p; writeState(s); applyState(); }
  function setSize(v) { var s = readState(); s.size = v; s.page = 1; writeState(s); applyState(); }
  function clearSearch() {
    if (searchInput) searchInput.value = '';
    var s = readState(); s.q = ''; s.page = 1; writeState(s); applyState();
    if (searchInput) searchInput.focus();
  }

  var debounceTimer = null;
  if (searchInput) {
    searchInput.addEventListener('input', function(){
      searchClear.hidden = !searchInput.value;
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function(){
        var s = readState(); s.q = searchInput.value.trim(); s.page = 1; writeState(s); applyState();
      }, 200);
    });
    searchInput.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && searchInput.value) { e.preventDefault(); clearSearch(); }
    });
  }
  if (searchClear) searchClear.addEventListener('click', clearSearch);
  if (pageSize) pageSize.addEventListener('change', function(){ setSize(parseInt(pageSize.value, 10)); });
  if (searchForm) searchForm.addEventListener('submit', function(e){ e.preventDefault(); });

  window.addEventListener('popstate', function(){ applyState(); });

  applyState();
})();
</script>
"""


# ──────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────

def main():
    # Optional verification flag: --inline-threshold N overrides the byte
    # threshold below which the index is inlined (used to exercise the
    # lazy-fetch path with a real build; default is ~200KB).
    threshold = INLINE_INDEX_THRESHOLD_BYTES
    args = sys.argv[1:]
    if "--inline-threshold" in args:
        try:
            threshold = int(args[args.index("--inline-threshold") + 1])
        except (ValueError, IndexError):
            threshold = INLINE_INDEX_THRESHOLD_BYTES

    posts = load_posts()

    # enrich with derived fields
    for p in posts:
        p["excerpt"] = truncate_excerpt(p["excerpt"])
        p["read_time"] = read_time_minutes(p["body_md"])

    index_entries = build_search_index(posts)
    index_json = json.dumps(index_entries, ensure_ascii=False, indent=2)

    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    # search index file (always written)
    SEARCH_INDEX_FILE.write_text(index_json + "\n", encoding="utf-8")

    # decide inline vs lazy
    inline_index = len(index_json.encode("utf-8")) <= threshold

    # blog index page
    index_page = build_index_page(posts, index_json, inline_index)
    (BLOG_DIR / "index.html").write_text(index_page, encoding="utf-8")

    # post pages
    for p in posts:
        slug_dir = BLOG_DIR / p["slug"]
        slug_dir.mkdir(parents=True, exist_ok=True)
        (slug_dir / "index.html").write_text(build_post_page(p), encoding="utf-8")

    print("Built %d post(s)." % len(posts))
    print("  blog/index.html")
    print("  blog/search-index.json (%d bytes, %s)"
          % (len(index_json.encode("utf-8")),
             "inlined" if inline_index else "lazy-fetch"))
    for p in posts:
        print("  blog/%s/index.html" % p["slug"])


if __name__ == "__main__":
    main()

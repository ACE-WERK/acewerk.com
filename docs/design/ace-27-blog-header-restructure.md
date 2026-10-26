# ACE-27 — Blog post header restructure spec

- Change ID: ACE-27
- Layer: Design-system (blog post header layout)
- Upstream: BA task t_44e07100
- Source of truth: repo ACE-WERK/acewerk-dev main, scripts/build_blog.py + generated post pages

Status: FROZEN

Scope:
- Change the post-page header layout so the publish date appears on the same top row as the back-link, right-aligned, with the title beneath and a compact byline under that.
- Rule applies to all blog post pages (build_blog.py template + existing generated pages).
- No changes to blog index page, cards, nav, prose styles, footer, or fixture-note semantics.

---

## 1. New header layout (authoritative)

New HTML structure inside build_post_page (article header):

Before (current):

  <article>
    <header class="post-header">
      <a class="post-back" href="/blog/">&larr; Blog</a>
      <h1 class="post-title">Title</h1>
      <div class="post-byline">
        <span>By Author</span>
        <time datetime="...">Date</time>
        <span>N min read</span>
      </div>
    </header>

After (required):

  <article>
    <header class="post-header">
      <div class="post-header-top">
        <a class="post-back" href="/blog/">&larr; Blog</a>
        <time class="post-date" datetime="...">Date</time>
      </div>
      <h1 class="post-title">Title</h1>
      <div class="post-byline">
        <span>By Author</span>
        <span class="post-read">N min read</span>
      </div>
    </header>

Semantics:
- .post-header-top:
  - Flex row: back-link left, date right-aligned.
  - Must never wrap at 1440 / 768 / 390.
  - Date's right edge must equal the row's right edge (i.e., aligns with shell/container right).
- .post-title:
  - Remains full-width, left-aligned.
- .post-byline:
  - Flex row: author left, read-time right-aligned (margin-left: auto).
  - Right edge must equal the shell/container's right edge.
  - Date is removed from here.

---

## 2. CSS rules (must match exactly)

All tokens reference blog-design.md / ACE-23. No new color or font tokens.

.post-header {
  margin-bottom: 2em;
}

.post-header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: nowrap;
  gap: 12px;
  margin-bottom: 0.5em;
  min-width: 0;
}

.post-back {
  display: inline-block;
  flex: 0 0 auto;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: var(--fs-label);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
  text-decoration: none;
  white-space: nowrap;
}
.post-back:hover { color: var(--accent-soft); }

.post-date {
  flex: 0 0 auto;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: var(--fs-label);
  letter-spacing: 0.06em;
  color: var(--accent);
  white-space: nowrap;
}

.post-title {
  font-family: 'Rajdhani', sans-serif;
  font-weight: 500;
  font-size: var(--fs-post-title);
  line-height: 1.12;
  letter-spacing: 0.02em;
  color: #ffffff;
  margin: 0 0 0.5em;
}

.post-byline {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: nowrap;
  gap: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: var(--fs-label);
  letter-spacing: 0.06em;
  color: var(--ink-muted);
}

.post-read {
  white-space: nowrap;
}

Notes:
- No special media-query behavior required; the existing shell/container padding
  and ACE-23 clamp already ensure safe space. Back-link + date are short strings
  and flex-wrap: nowrap guarantees they stay on one line.

---

## 3. Template changes (build_blog.py)

In build_post_page():

- Current (approx, lines around 1261-1269):

  '            <header class="post-header">\n',
  '              <a class="post-back" href="/blog/">&larr; Blog</a>\n',
  "              <h1 class=\"post-title\">" + title_esc + "</h1>\n",
  '              <div class="post-byline">\n',
  "                <span>By " + author_esc + "</span>\n",
  '                <time datetime="' + date_esc + '">' + dstr + "</time>\n",
  "                <span>" + str(read_time) + " min read</span>\n",
  "              </div>\n",
  "            </header>\n",

- Replace with:

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

Constraints:
- Use existing variables (date_esc, dstr, author_esc, read_time, title_esc).
- Do not alter canonical URL, meta, or other head elements.
- Do not alter fixture-note markup; it remains after </header>.

---

## 4. CSS block changes (build_blog.py)

Update the embedded CSS in the build_blog.py CSS string (around lines 742-764):

- Remove the old .post-byline time accent rule:
  - Delete: ".post-byline time { color: var(--accent); }"
- Replace/extend .post-header and .post-byline with rules from §2.

No changes to:
- .post-card-* rules (blog index)
- .fixture-note
- Prose styles (.post-body)
- Nav / shell / container geometry

---

## 5. Generated pages

After modifying build_blog.py:

- Re-run build_blog.py (as per existing workflow) to regenerate all post pages.
- Ensure generated post pages exactly match this spec:
  - Top row: back-link + date, flex, no-wrap.
  - Title under it.
  - Byline: author left, read-time right; no date.
- Existing fixture posts (dev-fixture-short, dev-fixture-long, dev-fixture-truncation)
  are updated via regeneration; do not hand-edit them separately.

---

## 6. Acceptance criteria (testable)

A1: Header top row
- Every blog post page contains a .post-header-top flex row with:
  - left: <a class="post-back"> ("← Blog")
  - right: <time class="post-date"> (accent color, JetBrains Mono, no-wrap).
- The date's right edge equals the row's right edge (space-between + flex row).

A2: No wrap at 1440 / 768 / 390
- At viewports 1440×900, 768×1024, and 390×844:
  - .post-header-top does not wrap (only one line).
  - .post-byline does not wrap (only one line).
- Checked visually or via box-model: element box heights equal line-height;
  no second-line boxes for header-top/byline.

A3: Byline alignment
- .post-byline uses:
  - left: "By Author"
  - right: "N min read" with margin-left: auto
- Byline right edge matches the content-shell's right edge.

A4: Typography preserved
- Date:
  - color: var(--accent) (gold)
  - font-family: 'JetBrains Mono', monospace
  - font-size: var(--fs-label)
- Back-link:
  - same font/token set as before (JetBrains Mono, var(--fs-label), accent).
- Byline:
  - same token set; read-time in var(--ink-muted).

A5: Fixture note untouched
- The .fixture-note block (if present) is:
  - still positioned directly below </header>
  - identical class and text: "Fixture — sample post for staging QA..."

A6: No horizontal overflow
- At 1440 / 768 / 390:
  - scrollWidth equals innerWidth on main; no horizontal scrollbars.
  - Header-top and byline contents fully contained inside the content-shell.

A7: Consistency
- All blog post pages (including fixtures) use the same header layout:
  - Confirm via:
    - running build_blog.py
    - spot-checking at least two generated post files (e.g., dev-fixture-short, dev-fixture-long).

---

## 7. Edge cases

E1: Very long author name
- Author name must not push "N min read" onto a new line.
- .post-byline must use flex-wrap: nowrap and rely on the shell's padding;
  if necessary, allow the author text to ellipsize via:
    - max-width: 55% or similar;
    - overflow: hidden; text-overflow: ellipsis;
  but do not break wrap.

E2: Long title above header-top
- .post-title uses existing clamp token (--fs-post-title) and is full-width;
  no new constraints required.

E3: Existing page regeneration
- Changing build_blog.py must not alter:
  - blog index page layout (toolbar, post-grid, pagination).
  - nav structure or scripts.
- Only the post-page header section is modified.

E4: Accessibility
- <time> retains datetime attribute with ISO date.
- Semantic roles unchanged; no removal of aria attributes.

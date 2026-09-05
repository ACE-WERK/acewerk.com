# AceWerk Blog — Design Specification

Status: **Authoritative for ACE-14 (dev-agent).**
Branch: `feature/blog` · Scope: `/blog/` (index) and `/blog/<slug>/` (post).
Replaces the WebGL mosaic on blog routes only; does not modify the mosaic on any other page.

This document is the design system extension for the blog. Every value below is a
concrete token reference or literal — there are no placeholders. Where a token is
*new*, it is listed in §1.2 and added using the existing naming convention. Where a
value is *existing*, it is referenced verbatim from the canonical set in
`services/index.html` `:root` (lines 141–167).

---

## 1. Design tokens

### 1.1 Reused tokens (canonical — do not re-declare)

Color
- `--canvas: #060912`
- `--surface: #0c1122`
- `--surface-plus: #11182b`
- `--accent: #d49a2e`
- `--accent-soft: #f4d39e`
- `--ink: #e5e7f0`
- `--ink-muted: rgba(190,200,220,0.88)`
- `--border: rgba(255,255,255,0.08)`
- `--glass-border: rgba(255,255,255,0.11)`
- `--rule: rgba(255,255,255,0.09)`
- `--rule-soft: rgba(255,255,255,0.055)`

Shape / motion
- `--radius-sm: 6px`
- `--radius-md: 9px`
- `--radius-lg: 14px`
- `--transition-fast: 0.18s ease-out`
- `--transition-med: 0.3s ease-out`
- `--max-width: 1100px`

Type scale
- `--fs-label: clamp(11px, 0.6vw + 8px, 12px)` — eyebrows, tags, stat labels
- `--fs-body: clamp(16px, 0.35vw + 14px, 18px)` — running copy
- `--fs-item-title: clamp(19px, 0.5vw + 16px, 22px)` — names
- `--fs-lead: clamp(22px, 1.2vw + 14px, 30px)` — lead / CTA
- `--fs-section-title: clamp(26px, 1.6vw + 15px, 38px)`
- `--fs-stat: clamp(34px, 3.5vw + 10px, 56px)`

Fonts (`assets/fonts/fonts.css`) — Space Grotesk 300/400/500 (body), Orbitron 500
(brand), Inter 400/500, JetBrains Mono 400/500 (code/labels), Rajdhani 400/500.

**Cross-page container spec (ACE-23):** the gutter, shell, and hero top-margin
rules for `site-container` / `content-wrap` / `content-shell` / `hero-shell`
apply to **all** pages (blog and non-blog), not just blog. Their canonical form
and the unified values live in `docs/design/ace-23-container-spacing.md` §1.3 —
this document's container values match it and are not re-decided locally.

### 1.2 New tokens (deliverable 7)

Add these to the blog pages' `:root`. Names follow the existing `--breakpoint-*`,
`--fs-*`, `--accent-*`, `--measure-*` conventions.

```css
:root {
  /* structural / layout */
  --breakpoint-nav: 768px;            /* nav collapses to hamburger below this */
  --nav-height: 52px;                 /* desktop nav bar (was hardcoded) */
  --nav-height-mobile: 44px;          /* mobile nav bar (was hardcoded) */
  --measure-prose: 720px;             /* prose reading column measure */

  /* type */
  --fs-post-title: clamp(26px, 2.6vw + 14px, 40px);  /* post page h1 */

  /* accent derivatives (same hue as --accent #d49a2e) */
  --accent-tint: rgba(212,154,46,0.16);   /* accent wash: focus ring, current page, hover fill */
  --accent-border: rgba(212,154,46,0.42); /* accent-tinted border for hover/current states */

  /* code surfaces */
  --code-bg: rgba(4,6,12,0.55);           /* block code surface */
  --code-inline-bg: rgba(255,255,255,0.07); /* inline code surface */

  /* static-backdrop variant (blog routes) — every backdrop colour lives here */
  --backdrop-base: radial-gradient(140% 160% at 50% 46%, #0a111f 0%, #060a14 55%, #04060c 100%);
  --backdrop-glow-warm-1: rgba(212,154,46,0.10);  /* = --accent at 10% alpha */
  --backdrop-glow-warm-2: rgba(212,154,46,0.07);  /* = --accent at 7% alpha */
  --backdrop-glow-cool: rgba(56,74,120,0.14);     /* cool counter-glow */
  --backdrop-dots: rgba(255,255,255,0.05);        /* dot grid, --ink family */
}
```

Everything else reuses §1.1 or one of the values listed above — there are no other
magic literals in this spec.

---

## 2. Static backdrop (deliverable 6)

Blog routes do **not** instantiate the mosaic. Instead a page-level static backdrop
variant is used: pure CSS, fixed, behind all content, `z-index: 0`. It is built from
the existing token hues (the accent gold and the canvas/surface navy family), with the
few literal values collected as `--backdrop-*` tokens in §1.2. No canvas, no WebGL.

Markup (replaces `<div class="mosaic-bg">…</div>` on blog pages):

```html
<div class="blog-backdrop" aria-hidden="true"></div>
```

CSS:

```css
.blog-backdrop {
  position: fixed; inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  /* same base radial field as the mosaic-bg, so the page feels continuous */
  background: var(--backdrop-base);
}

/* two soft gold glows (--accent at low alpha) + a cool counter-glow:
   a "still nebula" that echoes the mosaic's mood without motion */
.blog-backdrop::before {
  content: ""; position: absolute; inset: 0;
  background:
    radial-gradient(60% 45% at 78% 8%,  var(--backdrop-glow-warm-1) 0%, rgba(212,154,46,0) 60%),
    radial-gradient(55% 40% at 15% 92%, var(--backdrop-glow-warm-2) 0%, rgba(212,154,46,0) 55%),
    radial-gradient(42% 34% at 50% 50%, var(--backdrop-glow-cool) 0%, rgba(56,74,120,0) 72%);
}

/* faint dot grid masked to the centre, mirroring the mosaic's ::after falloff */
.blog-backdrop::after {
  content: ""; position: absolute; inset: 0;
  background-image: radial-gradient(var(--backdrop-dots) 1px, transparent 1px);
  background-size: 32px 32px;
  -webkit-mask-image: radial-gradient(120% 120% at 50% 46%, #000 40%, transparent 95%);
          mask-image: radial-gradient(120% 120% at 50% 46%, #000 40%, transparent 95%);
  pointer-events: none;
}
```

Notes for dev:
- The `.mosaic-bg` container, its `<canvas>`, and the entire inline `makeBand`
  script block are **omitted** from blog pages. There must be no `webgl2` context,
  no Three.js import, no shader compilation on `/blog/` or `/blog/<slug>/`.
- All page content sits in `.page-wrapper { position: relative; z-index: 1; padding-top: var(--nav-height); }`
  exactly as on the inner pages.
- The brightest region of this backdrop is the radial centre `#0a111f`. Contrast for
  all prose/token text is verified against that value in §12.

---

## 3. Navigation (deliverable 3)

The shared nav is:

```html
<header class="nav-bar" role="banner">
  <div class="header-inner-wrapper site-container">
    <a href="/" class="nav-logo" aria-label="Ace Werk home">Ace Werk</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"
            aria-label="Open menu" type="button">
      <span class="nav-toggle-bar" aria-hidden="true"></span>
      <span class="nav-toggle-bar" aria-hidden="true"></span>
      <span class="nav-toggle-bar" aria-hidden="true"></span>
    </button>
    <nav class="nav-links" id="site-nav" role="navigation" aria-label="Main navigation">
      <a href="/services/">Services</a>
      <a href="/our-team/">Our Team</a>
      <a href="/contact/">Contact</a>
      <a href="/blog/" class="nav-blog">Blog</a>
    </nav>
  </div>
</header>
```

Order is fixed: Services → Our Team → Contact → **Blog (last)**. The logo hyperlink
stays on the left, unchanged.

**Scope note:** this nav (with the Blog item and hamburger) must be adopted on the
blog templates, and should be back-ported to `services`, `our-team`, `contact`, and
`index` so the header is consistent site-wide. This is a nav-only change; it does not
touch the mosaic markup on those pages.

### 3.1 Blog nav item — subtle distinction

The Blog item must read as "a live feed lives here", never as a CTA or promotional
badge. It uses the exact same type treatment as the other items (Space Grotesk 300,
13px, letter-spacing 0.12em, uppercase) and is distinguished only by a **small accent
dot** rendered before the label.

```css
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
  box-shadow: 0 0 8px rgba(212,154,46,0.6); /* soft glow only on hover/active */
}
```

- Default dot opacity `0.7` — present but quiet; it is **not** a filled button, has
  no background, no padding box, no uppercase "NEW" tag, no outline ring.
- On hover/active the dot brightens to full opacity and gains a soft glow; the label
  follows the standard `.nav-links a:hover/active` rule (color → `--ink` + accent
  underline scaleX).
- Active state on `/blog/` and `/blog/<slug>/` uses `class="active"` +
  `aria-current="page"`, identical to the other items.

### 3.2 Mobile hamburger

Breakpoint: `--breakpoint-nav: 768px`. Below 768px the `.nav-links` collapse into a
dropdown panel and the `.nav-toggle` button appears; at ≥768px the toggle is hidden
and `.nav-links` render inline (desktop behaviour unchanged). This single value is
recorded here as `--breakpoint-nav` and is the one place the breakpoint lives.

Trigger (`.nav-toggle`)
- 44px × 44px tap target, right-aligned in the bar, transparent background, no border.
- Three bars: `width 20px; height 2px; background var(--ink-muted); margin 3px 0;`
  gap 6px total. Default bars are `--ink-muted`; hover → `--ink`.
- `:focus-visible`: global accent outline (2px `--accent`, offset 3px) — no override.
- Expanded (`.open`): bars morph to an "×" — top bar `transform: translateY(5px) rotate(45deg)`,
  middle bar `opacity: 0`, bottom bar `transform: translateY(-5px) rotate(-45deg)`;
  all bars become `--accent`. Transition `var(--transition-med)`.

Panel (`#site-nav` at <768px)
- `position: fixed; top: var(--nav-height-mobile); left: 0; right: 0; z-index: 49;`
- `display: none` by default; `.open { display: block; }`.
- Surface: `background: rgba(6,9,18,0.94)` + `backdrop-filter: blur(14px) saturate(1.15)`
  (+ `-webkit-` prefix), `border-bottom: 1px solid var(--glass-border)`.
- `padding: 12px 20px 20px;`
- Links stacked full-width: Space Grotesk 400, 16px, letter-spacing 0.12em, uppercase,
  `color: var(--ink)`, `min-height: 48px`, `display: flex; align-items: center`,
  separated by `border-top: 1px solid var(--rule-soft)` (first child no border).
  Active link: `color: var(--accent-soft)` + the accent-dot treatment for Blog.
- The Blog item in the panel keeps its 4px accent dot.

Behaviour (required, implemented by dev — spec here, not improvised)
- Trigger toggles `aria-expanded` (`false` ↔ `true`) and the `.open` class on both
  trigger and `#site-nav`.
- On open: move focus to the first link in `#site-nav`.
- Focus trap: while open, Tab from the last focusable element wraps to the first
  (the trigger), Shift+Tab from the trigger wraps to the last link. Only the trigger
  and panel links are focusable while open.
- Esc closes the panel and returns focus to the trigger.
- Background scroll lock while open: add `overflow: hidden` to `body` (a `.nav-open`
  class on `<body>`); restore on close.
- Clicking a link closes the panel (normal navigation proceeds). Clicking outside the
  panel closes it. Clicking the trigger toggles.
- Return focus to the trigger on close.

### 3.3 Responsive nav values

```css
@media (max-width: 768px) {   /* --breakpoint-nav */
  .nav-bar { height: var(--nav-height-mobile); }
  .nav-logo { font-size: 14px; }          /* was 24px desktop */
  .nav-toggle { display: inline-flex; }
  .nav-links { display: none; /* .open overrides to the fixed panel */ }
  .page-wrapper { padding-top: var(--nav-height-mobile); }
}
@media (min-width: 769px) {
  .nav-toggle { display: none; }
  .nav-links { display: flex; }
}
```

The existing `max-width: 700px` content-collapse block on the other pages is
unrelated and stays as-is; it does not govern the hamburger.

---

## 4. Blog index layout (`/blog/`)

Top-to-bottom, inside `.page-wrapper > main`:

1. `.blog-backdrop` (fixed, behind everything)
2. Header (nav) — §3
3. `.content-wrap.site-container` containing a `.content-shell` (reuse existing
   glass shell, §1 tokens + the `.content-shell` rules from `services/index.html`
   lines 285–299).
   Inside the shell, top to bottom:
   - Hero block: `.hero-label` ("Journal" — JetBrains Mono `--fs-label`, accent) +
     `h1.hero-title` "Blog" (Orbitron 500, same rules as existing `.hero-title`).
   - `.blog-toolbar` — search input (left) + page-size selector (right). §7, §8.
   - `.blog-status` — live result count / no-results / empty message (aria-live). §9.
   - `.post-grid` — the card grid. §5.
   - `.pagination` — §8.
4. Footer — reuse existing `.site-footer` / `.footer-bar` unchanged.

Wireframe:

```
┌─ nav-bar (logo ···· [hamburger | Services · Our Team · Contact · Blog]) ─┐
│
│  ┌─ content-shell ────────────────────────────────────────────────┐
│  │  JOURNAL                                                     │
│  │  Blog                                                        │
│  │  [ search …………………  × ]                 Posts per page [5 ▾] │
│  │  12 posts                                                    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                     │
│  │  │  card    │ │  card    │ │  card    │                     │
│  │  └──────────┘ └──────────┘ └──────────┘                     │
│  │  ← Prev   [1] [2] [3]  Next →                               │
│  └───────────────────────────────────────────────────────────────┘
```

---

## 5. Blog post card (deliverable 1)

### 5.1 Anatomy

Each post is an `<article class="post-card">`. The whole card is clickable via a
stretched-link overlay on the title anchor (semantic link + full-card hit area).

```html
<article class="post-card">
  <span class="post-card-glyph" aria-hidden="true">◆</span>
  <h3 class="post-card-title">
    <a class="post-card-link" href="/blog/<slug>/">Post title</a>
  </h3>
  <p class="post-card-excerpt">Excerpt…</p>
  <div class="post-card-meta">
    <span class="post-card-date"><time datetime="2026-09-05">Sep 05, 2026</time></span>
    <span class="post-card-read">3 min read</span>
    <span class="post-card-author">Author Name</span>
  </div>
  <div class="post-card-tags">
    <span class="post-card-tag">Design</span>
    <span class="post-card-tag">Systems</span>
  </div>
</article>
```

- **Glyph** (top-left): JetBrains Mono `◆` (U+25C6), `font-size 14px`,
  `color: var(--accent)`, `text-shadow: 0 0 12px rgba(233,168,60,0.45)`,
  `display: block; margin-bottom: 14px;`. Mirrors the `.svc-card-glyph` language.
- **Title**: Rajdhani 500, `font-size: var(--fs-item-title)`, `line-height: 1.25`,
  `color: #ffffff`. Truncated to **2 lines** (§5.3). No thumbnail image — the content
  model has no image field; the glyph is the visual anchor.
- **Excerpt**: Space Grotesk 300, `font-size: var(--fs-body)`,
  `color: var(--ink-muted)`, `line-height: 1.7`. Truncated to **3 lines** (§5.3).
- **Meta row**: single flex row, JetBrains Mono 400 `var(--fs-label)`, `letter-spacing 0.06em`:
  - date — `color: var(--accent)`, format `Mon DD, YYYY` (e.g. `Sep 05, 2026`), in a
    semantic `<time datetime="YYYY-MM-DD">`.
  - read-time — `color: var(--ink-muted)`, format `N min read` where
    `N = max(1, ceil(wordCount / 200))`, computed at build time.
  - author — `color: var(--ink-muted)`, pushed right via `margin-left: auto`,
    `max-width: 140px`, single-line ellipsis (§5.3).
- **Tags row** (optional): muted pills, JetBrains Mono 400 `var(--fs-label)`,
  `text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-muted)`,
  `padding: 3px 8px; border: 1px solid var(--rule); border-radius: var(--radius-sm)`.
  Show at most 3 tags; if more, show the first 3 plus a `+N` counter. If no tags,
  omit the row entirely (no reserved space).

### 5.2 Card visual language (glass tile)

Matches the `.content-shell` glass treatment, tuned for a hover lift:

```css
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
  transition: transform var(--transition-med), border-color var(--transition-med),
              box-shadow var(--transition-med);
}
```

Stretched link:

```css
.post-card-link { color: inherit; text-decoration: none; }
.post-card-link::after {
  content: ""; position: absolute; inset: 0;   /* full-card hit area */
  border-radius: inherit;
}
```

States:

- **Default** — as above.
- **Hover** — `transform: translateY(-3px)`; `border-color: var(--accent-border)`;
  `box-shadow: 0 14px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(212,154,46,0.18),
  inset 0 1px 0 rgba(255,255,255,0.10)`; title `color: var(--accent-soft)`.
- **Focus-visible** — the link's global focus ring applies (2px `--accent`, offset 3px),
  rendered around the whole card because the `::after` overlay fills it. No additional
  shadow needed.
- **Active (pressed)** — `transform: translateY(0)`; `box-shadow: 0 2px 4px rgba(0,0,0,0.35),
  inset 0 2px 4px rgba(0,0,0,0.3)` (pressed, like `.btn-primary:active`).

`@supports not (backdrop-filter: blur(1px))` fallback (Safari-old / any non-supporting
browser): `.post-card { background: linear-gradient(165deg, rgba(11,16,32,0.94), rgba(7,10,20,0.92)); }`
— same pattern as the existing `.content-shell` fallback.

### 5.3 Truncation rules (long titles / authors / excerpts)

- **Title** — clamp to 2 lines, ellipsis, and reserve 2 lines of height so cards in a
  row stay equal-height:
  ```css
  .post-card-title {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    min-height: calc(1.25em * 2);  /* line-height 1.25 × 2 */
  }
  ```
- **Excerpt** — clamp to 3 lines, ellipsis:
  ```css
  .post-card-excerpt {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
  }
  ```
  Additionally the build step should pre-truncate excerpts to **200 characters**
  (append `…`) so the search index and DOM stay lean; the 3-line clamp is the
  display-side guarantee.
- **Author** — single line, ellipsis:
  ```css
  .post-card-author {
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    max-width: 140px;
  }
  ```
- **Tags** — see §5.1 (max 3 + `+N`).

### 5.4 Grid

```css
.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}
```

Result at `--max-width: 1100px`: 3 columns desktop; 2 columns ~700–1024px; 1 column
below ~700px. Cards stretch to equal height per row.

---

## 6. Long-form prose style set (deliverable 2)

Applied to the post body container `.post-body` (and the excerpt/lead if reused).
All values concrete; this is the largest deliverable — dev must not improvise.

### 6.1 Container

```css
.post-body {
  max-width: var(--measure-prose);      /* 720px */
  margin: 0 auto;
  color: var(--ink);                    /* full contrast for reading */
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 300;
  font-size: var(--fs-body);
  line-height: 1.75;
}
```

### 6.2 Headings

Headings use Rajdhani (matches the section-title voice); colour white; anchored with
generous top margin so scanning is clear.

```css
.post-body h2 {
  font-family: 'Rajdhani', sans-serif; font-weight: 500;
  font-size: var(--fs-section-title);          /* clamp 26–38px */
  line-height: 1.15; letter-spacing: 0.04em;
  color: #ffffff;
  margin: 2.5em 0 0.6em;
}
.post-body h3 {
  font-family: 'Rajdhani', sans-serif; font-weight: 500;
  font-size: var(--fs-lead);                   /* clamp 22–30px */
  line-height: 1.2; letter-spacing: 0.03em;
  color: #ffffff;
  margin: 2em 0 0.55em;
}
.post-body h4 {
  font-family: 'Space Grotesk', sans-serif; font-weight: 500;
  font-size: var(--fs-item-title);             /* clamp 19–22px */
  line-height: 1.3; letter-spacing: 0.01em;
  color: var(--accent-soft);
  margin: 1.75em 0 0.5em;
}
```

### 6.3 Paragraph rhythm

```css
.post-body p { margin: 0 0 1.25em; }
.post-body p:last-child { margin-bottom: 0; }
```

Consecutive paragraphs: no extra gap — the single `1.25em` bottom margin is the
rhythm. Vertical rhythm is anchored to `line-height: 1.75`.

### 6.4 Lists

```css
.post-body ul, .post-body ol { margin: 0 0 1.25em; padding-left: 1.5em; }
.post-body li { margin: 0.35em 0; }
.post-body li::marker { color: var(--accent); font-family: 'JetBrains Mono', monospace; }
.post-body ul { list-style: disc; }   /* accent disc via ::marker */
.post-body ol { list-style: decimal; }/* tabular accent numerals via ::marker */
```

Nested lists: indent one level, same marker rules, `font-size` unchanged.

### 6.5 Blockquote

```css
.post-body blockquote {
  margin: 1.75em 0;
  padding: 0.25em 0 0.25em 1.5em;
  border-left: 2px solid var(--accent);
  color: var(--ink);
  background: rgba(255,255,255,0.02);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
.post-body blockquote p { margin: 0; }
.post-body blockquote cite {
  display: block; margin-top: 0.75em;
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  font-size: var(--fs-label); letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--ink-muted); font-style: normal;
}
```

No italics in the quote body (the Space Grotesk subset shipped has no italic face).

### 6.6 Inline links

```css
.post-body a {
  color: var(--accent);                 /* 7.6:1 on brightest backdrop — AA */
  text-decoration: underline;
  text-decoration-color: rgba(212,154,46,0.45);
  text-underline-offset: 3px;
  text-decoration-thickness: 1px;
  transition: color var(--transition-fast);
}
.post-body a:hover { color: var(--accent-soft); }
```

`:focus-visible` uses the global accent outline (no override).

### 6.7 Code

Inline:

```css
.post-body code {
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  font-size: 0.85em;
  color: var(--accent-soft);
  background: var(--code-inline-bg);
  padding: 0.15em 0.45em;
  border-radius: var(--radius-sm);
  border: 1px solid var(--rule);
}
```

Block:

```css
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
```

### 6.8 Images with captions

```css
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
```

### 6.9 Horizontal rule

```css
.post-body hr {
  border: none;
  border-top: 1px solid var(--rule);
  margin: 2.5em 0;
}
```

### 6.10 Post page header (above `.post-body`)

```css
.post-header { margin-bottom: 2em; }
.post-header .post-title {          /* h1 */
  font-family: 'Rajdhani', sans-serif; font-weight: 500;
  font-size: var(--fs-post-title);   /* clamp 26–40px */
  line-height: 1.12; letter-spacing: 0.02em;
  color: #ffffff;
  margin: 0 0 0.5em;
}
.post-header .post-byline {
  display: flex; flex-wrap: wrap; gap: 8px 20px; align-items: baseline;
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  font-size: var(--fs-label); letter-spacing: 0.06em;
  color: var(--ink-muted);
}
.post-header .post-byline time { color: var(--accent); }
```

In-page back control (above the title, inside the header):

```html
<a class="post-back" href="/blog/">← Blog</a>
```

```css
.post-back {
  display: inline-block; margin-bottom: 1.25em;
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  font-size: var(--fs-label); letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--accent); text-decoration: none;
}
.post-back:hover { color: var(--accent-soft); }
```

A real `<a href="/blog/">` — never `history.back()`.

---

## 7. Search input component (deliverable 4)

```html
<form class="blog-search" role="search" aria-label="Search posts">
  <label class="visually-hidden" for="blog-search-input">Search posts</label>
  <span class="blog-search-icon" aria-hidden="true"><!-- inline 16×16 magnifier SVG, stroke currentColor --></span>
  <input id="blog-search-input" class="blog-search-input" type="search"
         autocomplete="off" spellcheck="false" placeholder="Search posts…"
         aria-label="Search posts" />
  <button class="blog-search-clear" type="button" aria-label="Clear search" hidden>×</button>
</form>
```

Behaviour (from the frozen spec): 200ms debounce, minimum 2 characters, query
reflected in `?q=`, filtering resets pagination to page 1. Clear control one-click
clears. If the generated index exceeds ~200KB, fetch lazily on first focus. With JS
disabled, the list renders fully and the search form is `hidden`.

Input (`type="search"`; suppress the native WebKit cancel button so the custom × is
the single clear affordance):

```css
.blog-search { position: relative; display: flex; align-items: center; }
.blog-search-icon {
  position: absolute; left: 14px; width: 16px; height: 16px;
  color: var(--ink-muted); pointer-events: none;
}
.blog-search-input {
  width: 100%; height: 48px;
  padding: 0 44px 0 44px;             /* icon left, clear right */
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
```

States:
- **Idle** — as above; placeholder `--ink-muted`.
- **Focused** — `border-color: var(--accent-border)`;
  `box-shadow: 0 0 0 3px var(--accent-tint)`.
- **Typing (value non-empty)** — the clear button is shown (`hidden` removed).
- **No-results / empty** — the input itself is unchanged; the message lives in the
  `.blog-status` region (§9). No inline error styling on the input.

Clear control:

```css
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
.blog-search-clear:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
```

On click: clear value, remove `?q=`, refocus the input, restore full list.
`:focus-visible` on the input uses the same accent outline (offset 3px) as the rest
of the site; the ring in the focused state is additive.

Accessibility: `role="search"` landmark; visually-hidden label; the live region in
§9 announces result counts / no-results to screen readers via `aria-live="polite"`.

---

## 8. Pagination + page-size selector (deliverable 5)

### 8.1 Page-size selector

Native `<select>` (robust, accessible, no-JS safe), styled as glass:

```html
<label class="page-size-label" for="page-size">Posts per page</label>
<select id="page-size" class="page-size-select">
  <option value="5" selected>5</option>
  <option value="10">10</option>
  <option value="20">20</option>
</select>
```

```css
.page-size-select {
  height: 40px; padding: 0 12px;
  background: rgba(12,18,35,0.4);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  color: var(--ink);
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  font-size: 13px;
}
.page-size-select:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
.page-size-label {
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  font-size: var(--fs-label); letter-spacing: 0.06em;
  color: var(--ink-muted);
}
```

Default `5`. Changing the size returns to page 1 and persists across searches
(state in URL: `?q=&size=&page=`). Placed right-aligned in `.blog-toolbar`:

```css
.blog-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; flex-wrap: wrap; margin-bottom: 24px;
}
```

### 8.2 Pagination nav

```html
<nav class="pagination" aria-label="Pagination">
  <button class="pagination-btn pagination-prev" type="button" aria-label="Previous page">←</button>
  <button class="pagination-btn is-current" type="button" aria-current="page">1</button>
  <button class="pagination-btn" type="button">2</button>
  <span class="pagination-ellipsis" aria-hidden="true">…</span>
  <button class="pagination-btn" type="button">7</button>
  <button class="pagination-btn pagination-next" type="button" aria-label="Next page">→</button>
</nav>
```

```css
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
  transition: color var(--transition-fast), border-color var(--transition-fast),
              background var(--transition-fast);
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
.pagination-btn:disabled {
  opacity: 0.38; cursor: default; pointer-events: none;
}
.pagination-ellipsis { color: var(--ink-muted); padding: 0 2px; }
```

States:
- **Default** — glass button, `--ink-muted`.
- **Current** — `aria-current="page"`, accent-tinted fill + accent border +
  `--accent-soft` text (a wash, not a solid gold block — avoids CTA loudness).
- **Disabled (prev on page 1 / next on last page)** — `disabled` attribute +
  `opacity 0.38`, no pointer events.
- **Focus-visible** — global accent outline.

Numbering rule for long ranges: if there are > 7 pages, render first page, last page,
current page, current ±1, and collapse the rest to ellipses (`…`). For ≤ 7 pages,
render every page number. Reverse-chronological order is preserved across pages.
Pagination is client-side over the fully rendered list (JS-disabled visitors see all
posts).

---

## 9. Empty & no-results states

A single live region reports state; three variants:

```html
<div class="blog-status" role="status" aria-live="polite"></div>
```

```css
.blog-status {
  font-family: 'JetBrains Mono', monospace; font-weight: 400;
  font-size: var(--fs-label); letter-spacing: 0.06em;
  color: var(--ink-muted); margin-bottom: 20px;
}
```

- **Results** — `N posts` (count of the currently filtered set).
- **No results (search)** — `No posts match “<query>”.` followed by a clear button:
  ```html
  <button class="status-clear" type="button">Clear search</button>
  ```
  one-click clear (same action as the × control).
- **Empty index (zero posts, no search)** — `No posts yet.` with no clear button.

```css
.status-clear {
  background: none; border: none; padding: 0; margin-left: 8px;
  color: var(--accent); cursor: pointer;
  font-family: inherit; font-size: inherit; letter-spacing: inherit;
  text-decoration: underline; text-underline-offset: 3px;
}
.status-clear:hover { color: var(--accent-soft); }
```

---

## 10. Motion & reduced motion

- Card hover lift: `transform translateY(-3px)` + shadow over `--transition-med`.
- Panel open/close: slide + fade (`opacity` + `translateY(-6px)`) over
  `--transition-med`; trigger bar→× morph over `--transition-med`.
- Search results re-render: no animation (instant reflow; avoids flicker during
  debounced typing).
- `prefers-reduced-motion: reduce` — the global site rule already forces
  `animation-duration`/`transition-duration` to `0.01ms`. For the blog additionally:
  disable the hover lift (`transform: none`), render the panel open/close and the
  trigger morph as an instant opacity/visibility swap (no transform), and skip the
  dot-glow pulse. The static backdrop has no motion by construction.

```css
@media (prefers-reduced-motion: reduce) {
  .post-card:hover { transform: none; }
  .nav-toggle-bar { transition: none; }
  .nav-links { transition: none; }
}
```

---

## 11. Responsive behaviour

| Viewport | Nav | Grid | Prose | Toolbar |
|---|---|---|---|---|
| 375px | hamburger (panel) | 1 col | measure ≤ viewport − padding | toolbar wraps, search full-width |
| 700px | hamburger | 1 col | full measure | search full-width |
| 768px | hamburger (breakpoint) | 1–2 cols | full measure | inline |
| 1024px | inline links | 2–3 cols | full measure | inline |
| 1440px | inline links | 3 cols | 720px centred | inline |

- `--measure-prose: 720px` with `margin: 0 auto` centres the prose column; at narrow
  widths the shell's `padding` (from `.content-shell`) provides the gutter.
- The card grid uses `auto-fill minmax(300px, 1fr)` so it degrades fluidly with no
  media queries for column count.
- At 375px, confirm no horizontal scroll: `pre` scrolls (`overflow-x: auto`), long
  author names ellipsize, titles clamp to 2 lines.

---

## 12. Contrast & accessibility (WCAG AA)

Contrast of prose/body text against the static backdrop at its **brightest**
(`#0a111f`, the radial centre). Computed per WCAG 2.1 relative-luminance formula:

| Foreground | Background | Ratio | AA (≥4.5) |
|---|---|---|---|
| `--ink` `#e5e7f0` | `#0a111f` | 15.29 | PASS |
| `--ink-muted` (composited `#a8b2c5`) | `#0a111f` | 8.84 | PASS |
| `--accent` `#d49a2e` (inline links) | `#0a111f` | 7.60 | PASS |
| `--accent-soft` `#f4d39e` | `#0a111f` | 13.17 | PASS |
| `#ffffff` (headings) | `#0a111f` | 18.87 | PASS |

All prose and token text clears AA at the brightest backdrop point; content inside
the glass shells sits on a darker composite and therefore exceeds these ratios.

Other accessibility requirements (from the frozen spec), all met by this spec:
- Semantic landmarks: `header/nav/main/article/time/figure/footer`.
- Visible focus states everywhere (global `:focus-visible` accent outline + the
  component focus rings in §7/§8).
- Hamburger: `aria-expanded` + `aria-controls`, focus trap, Esc-close, scroll lock,
  return-focus-to-trigger (§3.2).
- Search: `role="search"`, labelled input, `aria-live` status (§7/§9).
- `prefers-reduced-motion` (§10).
- Blog nav item is subtly distinct, not a CTA/badge (§3.1).

---

## 13. Safari / glass rendering notes

- The static backdrop uses no WebGL, so the glass/backdrop-filter behaviour on Safari
  has no canvas to contend with. Use both `backdrop-filter` and
  `-webkit-backdrop-filter` on every glass surface (`.content-shell`, `.post-card`,
  `.nav-bar`, `.nav-links` panel, `.blog-search-input`), matching the existing pages.
- Keep the `@supports not (backdrop-filter: blur(1px))` fallback for `.post-card` and
  the nav panel (older Safari falls back to a near-opaque gradient, not transparent).
- The dot grid in `.blog-backdrop::after` uses `-webkit-mask-image` + `mask-image`
  (both present); on browsers without `mask-image` support, drop the dot grid
  entirely (the glow layers still render) rather than showing a full-page dot field.

---

## 14. Dev handoff checklist (ACE-14)

1. Add §1.2 tokens to the blog pages' `:root`; reuse §1.1 tokens everywhere else.
2. Replace the mosaic container/script with `.blog-backdrop` on `/blog/` and post
   pages only; verify **no WebGL context** is created on those routes.
3. Implement §3 nav (Blog item + hamburger) with the `--breakpoint-nav: 768px`
   value; back-port to the other pages' navs (nav-only, no mosaic changes).
4. Build the card (§5) and grid (§4) with the truncation rules in §5.3.
5. Build the prose style set (§6) verbatim.
6. Build search (§7) and pagination (§8) per spec; wire the empty/no-results states
   (§9) into the `aria-live` status region.
7. Respect §10 (reduced motion) and §13 (Safari).
8. Confirm §12 contrast values hold at 375/768/1024/1440px (QA verifies with
   screenshots + Lighthouse).

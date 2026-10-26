# ACE-26 — Design: spacing/geometry delta spec for blog post-card glyph removal

- Change ID: ACE-26
- Layer: Design (design-agent) — **CONFIRMED + LOCKED**. Pure-CSS deletion delta; **no new design**.
- Authoritative upstream: BA spec `docs/design/ace-26-blog-card-glyph-removal.md` @ `6b9cdde` (D1–D5, A1–A7, E1–E7). This doc **matches D2 and corrects one D2/E7 numeric estimate with measured proof** (§4).
- Source of truth: repo `ACE-WERK/acewerk-dev` `main`. Measured against two real renders: **PRE** = `6684697` (glyph present) and **POST** = `87d9004` (glyph removed — the Dev implementation commit, already pushed). Both rendered via local static server, Chromium headless, real woff2 fonts loaded (`document.fonts.ready`), at the 3 QA viewports.
- Downstream: **QA (t_1eb92faf)** validates A1–A7 on live `dev.acewerk.com/blog/` using **DOM-only** measurement at 3 viewports. **Dev (t_ebf21f32)** has already committed `87d9004` (byte-identical to the POST render measured here). No visual redesign — this is a geometry lock, not a design pass.

---

## 0. One-line intent

Remove the decorative gold diamond (`<span class="post-card-glyph">`) from the blog post card. The card is a flex column (`gap:14px; padding:24px`). Deleting the first flex item makes `.post-card-meta` (the date/read-time row) the first child, which now sits at the card's **top padding edge (24px)** — visually consistent with left/right/bottom. **No spacing property changes.** This doc locks the exact numbers QA must measure, so "it looks tighter" is replaced by "these values are byte-identical / at these exact px."

## 1. The `.post-card` container — byte-identical before and after (verified)

These computed values are **frozen** and measured **identical** in PRE and POST at all 3 viewports. QA: any one of these changing = FAIL (A5).

| Property | Locked computed value (all viewports) |
|---|---|
| `display` / `flex-direction` | `flex` / `column` |
| `padding` (T/R/B/L) | `24px` / `24px` / `24px` / `24px` |
| `gap` | `14px` |
| `border` (width, all sides) | `1px` |
| `border-color` | `rgba(255, 255, 255, 0.11)` (`--glass-border`) |
| `border-radius` | `14px` (`--radius-lg`) |
| `background-image` | `linear-gradient(165deg, rgba(12, 18, 35, 0.58), rgba(7, 10, 20, 0.5))` |
| `backdrop-filter` | `blur(14px) saturate(1.15)` |
| `box-shadow` (rest) | `rgba(0,0,0,0.45) 0px 8px 32px 0px, rgba(255,255,255,0.08) 0px 1px 0px 0px inset` |
| hover transform | `translateY(-3px)` (unchanged) |
| active transform | `translateY(0)` (unchanged) |
| `.post-grid` `gap` | `24px` (unchanged) |
| `.post-grid` `grid-template-columns` | `repeat(auto-fill, minmax(300px, 1fr))` (unchanged) |

**Card width and first-row card position are also invariant** (width-driven grid, no reflow — E7):

| Viewport | card width (invariant) | card0 absolute top @scrollY=0 (invariant) |
|---|---|---|
| 1440×900 | 433.000px | 521.797px |
| 768×1024 | 309.562px | 427.234px |
| 390×844 | 304.000px | 405.797px |

## 2. The only things that change

Removing the first flex item (`post-card-glyph`) changes exactly two classes of numbers, and nothing else:

1. **Card height** shrinks by the glyph's reclaimed space (§4: **50.391px**, identical at all 3 viewports).
2. **Cards below the first row** in the grid shift up by the same 50.391px (they stack in the same column; E7).

Every other computed value in §1 is byte-identical to PRE. No `margin-top` is added to `.post-card-meta`; no other rule in the `CSS` template or any page changes.

## 3. LOCKED post-removal geometry — QA measurement table (DOM-only)

After removal, each `.post-card`'s first child is `.post-card-meta`. **QA must verify these exact values** (A3). Offsets are measured from the **card's border-box top** via `getBoundingClientRect()` (subtract the card's `rect.top` from each child's `rect.top`).

**Primary lock (viewport-independent, the design truth):**

| Check | Locked value | Note |
|---|---|---|
| `getComputedStyle(card).paddingTop` | `24px` | all sides 24px |
| `getComputedStyle(card).gap` | `14px` | |
| first child is `.post-card-meta` | yes | `card.firstElementChild.className === 'post-card-meta'` |
| first-child top offset (border-box) | **25.00px** | = 24px padding + 1px border. (The task's "24px from card top" is the *padding* value; the *getBoundingClientRect* reading is 25.00px because it starts at the border edge. Both are correct — QA: do not "fail" a 24px spec on a 25px rect reading.) |
| content-edge to first child | **24px** | measured padding-edge → content, equals `padding-top` |
| inter-element gaps (all 4) | **14.00px** each | meta→title, title→excerpt, excerpt→author, author→tags |
| `.post-card-glyph` count in DOM | **0** | `document.querySelectorAll('.post-card-glyph').length === 0` |
| orphan `.post-card-glyph` CSS rule | **none** | no rule in any stylesheet matches the selector |

**Per-viewport child offsets (locked).** Offsets from card border-box top; `h` = measured child height (varies with font clamps/wrapping, but the **tops** are the lock):

### 1440×900 (card width 433.000px, card height 368.734 → 318.344)
| # | child | top offset (lock) | height (observed) |
|---|---|---|---|
| 0 | post-card-meta | **25.00** | 19.19 |
| 1 | post-card-title | **58.19** | 55.00 |
| 2 | post-card-excerpt | **127.19** | 91.78 |
| 3 | post-card-author | **232.97** | 19.19 |
| 4 | post-card-tags | **266.16** | 27.19 |

### 768×1024 (card width 309.562px, card height 389.812 → 339.422)
| # | child | top offset (lock) | height (observed) |
|---|---|---|---|
| 0 | post-card-meta | **25.00** | 19.19 |
| 1 | post-card-title | **58.19** | 49.59 |
| 2 | post-card-excerpt | **121.78** | 85.08 |
| 3 | post-card-author | **220.86** | 19.19 |
| 4 | post-card-tags | **254.05** | 60.38 (tags wrap to 2 rows) |

### 390×844 (card width 304.000px, card height 377.828 → 327.438)
| # | child | top offset (lock) | height (observed) |
|---|---|---|---|
| 0 | post-card-meta | **25.00** | 17.59 |
| 1 | post-card-title | **56.59** | 47.50 |
| 2 | post-card-excerpt | **118.09** | 81.56 |
| 3 | post-card-author | **213.66** | 17.59 |
| 4 | post-card-tags | **245.25** | 57.19 (tags wrap to 2 rows) |

**Date-row absolute Y (reference, @scrollY=0, current page layout):**

| Viewport | card top | + first-child offset | date-row absolute Y |
|---|---|---|---|
| 1440×900 | 521.797 | +25.00 | **546.80px** |
| 768×1024 | 427.234 | +25.00 | **452.23px** |
| 390×844 | 405.797 | +25.00 | **430.80px** |

(The absolute Y is **reference only** — it depends on the page header/layout above the grid, which is out of ACE-26 scope. The **primary** locked value is the 25.00px/24px relative offset above, which is stable.)

**Card height delta (locked):**

| Viewport | pre height | post height | Δ reclaimed |
|---|---|---|---|
| 1440×900 | 368.734 | 318.344 | **50.391px** |
| 768×1024 | 389.812 | 339.422 | **50.391px** |
| 390×844 | 377.828 | 327.438 | **50.391px** |

## 4. Reclaimed vertical space — measured 50.391px (correction to BA D2/E7)

BA D2/E7 estimated the reclaim at **~22.4 + 14 ≈ 36.4px**, on the assumption that the glyph's `margin-bottom:14px` was **redundant/inert** under the flex `gap`. Measurement shows that was **not** the case:

- PRE glyph box: `top 25.00`, `height 22.39` (14px font × ~1.6 body line-height = 22.4px line box).
- PRE measured space between glyph bottom and meta top = **28.00px** = **14px flex-gap + 14px margin-bottom**. Flexbox `gap` does **not** collapse with margins — the `margin-bottom` added a further 14px on top of the gap.
- **Reclaimed on removal = glyph box (22.39) + inter-gap (28.00) = 50.391px**, identical at all 3 viewports.

**Design consequence:** none to the design decision (still `gap:14px; padding:24px`, no compensation, meta at the 24px top-padding edge — exactly D2). **Numeric consequence for QA:** if any check asserts the card height drops by a specific amount, lock it to **50.391px**, not 36.4px. The +14px is the glyph's dead `margin-bottom` that dies with its rule (A5 confirms no other rule compensates for it). E1's "no residual phantom space" is **satisfied**: date row top is 24px from the content edge (25.00px border-box), measured.

## 5. QA measurement checklist (DOM-only, 3 viewports, no screenshot pass)

Run on live `dev.acewerk.com/blog/?t=<ts>` at **1440×900, 768×1024, 390×844** (Chromium headless):

1. **A1** — `git grep -n "post-card-glyph\|9670"` over tracked files → **0 hits**; no `◆` in any `blog/**` file or `scripts/build_blog.py`. *(verified here on `87d9004`: 0 hits.)*
2. **A3** — for each of the 3 `.post-card` articles: first child is `.post-card-meta`; computed `padding` = `24px` (all sides), `gap` = `14px`; `document.querySelectorAll('.post-card-glyph').length === 0`.
3. **§3 primary lock** — first-child border-box top offset = **25.00px** (24px content); all 4 inter-element gaps = **14.00px**.
4. **§3 per-viewport** — child top offsets match the §3 tables (within ±0.5px; font clamp rounding).
5. **§1 invariants** — every value in §1 byte-identical to PRE (border/radius/bg/backdrop/box-shadow/hover/grid gap/card width).
6. **§4** — card height delta = **50.391px** at all 3 viewports.
7. **A6** — **no console errors** on all 4 blog pages; HTML tag balance intact; `services/index.html` byte-identical to HEAD. *(verified here on POST render: 0 console errors, tag balance article 3/3 · span 21/21 · div 22/22 · a 8/8; services byte-identical.)*

## 6. Explicit DO-NOT list (must not change)

`.post-card` gap, padding, border, radius, background, backdrop/glass, box-shadow, hover, active; `.post-card-*` typography (font/size/line-height/color/letter-spacing); inter-element spacing; `.post-grid` gap + column formula; page header; search bar; post count; single-post template (`.post-title` / `.post-byline`); `.svc-card-glyph` (services). **No `margin-top` added to `.post-card-meta`.** No new token, no new rule.

## 7. Edge-case reconciliation

- **E1 (redundant margin):** RESOLVED by measurement — the `margin-bottom:14px` was **additive** (28px glyph→meta gap in PRE), not inert. It dies with the rule; no compensation. Date row lands at 24px content edge. See §4.
- **E7 (grid reflow):** CONFIRMED no column reflow — card width and first-row position invariant at all 3 viewports; only card height (−50.391px) and below-row card Y shift. Uniform card heights per row preserved.
- **A4/A5 (post pages pinned / diff-scope):** Dev commit `87d9004` diff = 6 files, +1/−44, matching D1 exactly; `blog/dev-fixture-*/index.html` differ by the 7-line CSS-rule deletion only (no card markup on those pages). *(verified here: `git diff 6684697 87d9004` = the 6 D1 files, shape +1/−44; the three fixture pages each show only the `.post-card-glyph` rule hunk.)*

## 8. Design sign-off

Geometry locked and verified against real renders (PRE `6684697`, POST `87d9004`). The removal is a clean pure-CSS deletion with **zero** container-spacing changes; the date row becomes the first child at the 24px top-padding edge, consistent with L/R/B, at all 3 QA viewports. The one correction to the BA estimate (§4, 50.391px vs 36.4px) is measurement-proven and does not alter any design decision. **Approve for QA on live `dev.acewerk.com/blog/`.**

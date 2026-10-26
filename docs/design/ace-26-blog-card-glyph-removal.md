# ACE-26 — Remove decorative diamond glyph from blog post cards

- Change ID: ACE-26
- Layer: Business-Analysis (ba-agent) — **FROZEN**. Decisions D1–D5, acceptance A1–A7, edge cases E1–E7.
- Source of truth: repo `ACE-WERK/acewerk-dev` `main` @ `6684697` (local `~/projects/acewerk.com`, remote `dev-origin`, deploys `https://dev.acewerk.com/`), re-verified by grep/diff on 2026-09-06.
- Downstream: Design (t_76d2d0ce, running) locks geometry → Dev (t_ebf21f32) implements + commits + pushes → QA (t_1eb92faf) validates A1–A7 on live dev → Release (t_7e23b99d) **PARKED** on the Illya gate (dev→prod merge). No visual redesign — pure deletion delta.

---

## 0. User Story

As a **visitor** reading the blog index on `dev.acewerk.com/blog/`, I want the post cards to present date, title, excerpt and author directly — without the decorative gold diamond above the metadata row — so that the card is tighter, the content hierarchy starts with the most relevant information (the date row), and the card stays visually consistent on desktop, tablet and mobile.

## 1. Verified state (2026-09-06, dev-origin main @ `6684697`)

Glyph markup (confirmed identical at HEAD): `<span class="post-card-glyph" aria-hidden="true">&#9670;</span>` (U+25C6).

| File | HEAD references | Location |
|---|---|---|
| `scripts/build_blog.py` | 2 | CSS rule `.post-card-glyph` lines 659–665 in the shared `CSS` template; glyph markup line in `render_card()` parts list, line 1136 |
| `blog/index.html` | 4 | CSS rule lines 356–362; glyph spans in all 3 post cards, lines 716 / 730 / 744 |
| `blog/dev-fixture-short/index.html` | 1 | CSS rule only (lines 356–362) — this is a post page, it renders no cards |
| `blog/dev-fixture-long/index.html` | 1 | CSS rule only (lines 356–362) |
| `blog/dev-fixture-truncation/index.html` | 1 | CSS rule only (lines 356–362) |
| `docs/design/blog-design.md` | 2 | glyph line in the §sample markup (line 327); the "Glyph (top-left) … Mirrors the `.svc-card-glyph` language" bullet (lines 344–346) plus the trailing "the glyph is the visual anchor" clause (line 348) |

Working-tree note (context for Dev): the repo working tree already carries an **uncommitted** glyph-removal diff (6 files, +1/−44). BA verified it is glyph-scope-only and that regenerating from the modified generator (`python3 scripts/build_blog.py`, run out-of-tree with `content/` + `scripts/`) yields output **byte-identical** to that working tree. Dev still owns the commit + push (D5).

Verified non-facts (do not re-hunt): no other file in the repo references `post-card-glyph`, `&#9670;`, `◆`, "rhombus" or "diamond" — the only remaining diamond glyphs in the site are `.svc-card-glyph` (services), which is a **different** component (E4).

## 2. Decisions (FROZEN)

### D1 — Exact removal list. Six files, nothing else.

Generator — `scripts/build_blog.py` (lines per HEAD `6684697`):

1. Delete the CSS rule (7 lines) from the shared `CSS` template, lines 659–665:

   ```css
   .post-card-glyph {
     font-family: 'JetBrains Mono', monospace;
     font-size: 14px;
     color: var(--accent);
     text-shadow: 0 0 12px rgba(233,168,60,0.45);
     display: block; margin-bottom: 14px;
   }
   ```

2. Delete the markup line from `render_card()`'s parts list, line 1136:

   ```python
   '  <span class="post-card-glyph" aria-hidden="true">&#9670;</span>\n',
   ```

Generated pages — `blog/index.html`, `blog/dev-fixture-short/index.html`, `blog/dev-fixture-long/index.html`, `blog/dev-fixture-truncation/index.html`:
- Delete the identical `.post-card-glyph` CSS rule (lines 356–362 in each).
- Delete the 3 glyph span lines in `blog/index.html` (lines 716 / 730 / 744).
- **Mechanism: edit the generator, then regenerate** (`python3 scripts/build_blog.py`). Hand-editing the generated HTML is only acceptable if regeneration produces a non-glyph diff; a clean regeneration is the acceptance path (A2).

Design doc — `docs/design/blog-design.md`:
- Delete the glyph line from the sample `<article class="post-card">` block.
- Delete the "Glyph (top-left)" bullet.
- Remove the now-stale trailing clause "the glyph is the visual anchor" from the Title bullet (the sentence becomes "…No thumbnail image — the content model has no image field.").

### D2 — Vertical geometry: delete the flex item, change no spacing property.

`.post-card` is `display:flex; flex-direction:column; gap:14px; padding:24px`. The glyph was the first flex item, so removing it:

- reclaims the glyph's own line box (14px font × inherited body `line-height:1.6` ≈ **22.4px** — do not use a guessed figure, measure in QA) **plus one 14px gap**;
- makes `.post-card-meta` (the date/read-time row) the first child, which then sits at exactly `padding-top: 24px` from the card border — consistent with left/right/bottom (D2 is the design answer to t_76d2d0ce; its spec must match these numbers, not invent new ones);
- the glyph's own `margin-bottom: 14px` was **redundant** under the flex gap (flex gaps apply between every item pair regardless of margins) — it dies with the rule and nothing must compensate for it.

Frozen: `.post-card { gap: 14px; padding: 24px; }` stays byte-identical. No `margin-top` added to `.post-card-meta`. No other rule in the `CSS` template or any page may change (A5 enforces this mechanically).

### D3 — Single-post template untouched.

`render_post_page()` uses `.post-title` / `.post-byline` and does **not** call the card markup; no related-posts module exists anywhere. The three fixture post pages therefore change **only** the CSS-rule deletion (A4 pins them byte-wise).

### D4 — Scope: blog only; services glyph untouched.

`.svc-card-glyph` (service cards) lives in `src/index.html`, `src/services.html`, `services/index.html` — different markup, different files, not emitted by `build_blog.py`. It stays. The only diamond removed in this change is the blog post-card one (E4).

### D5 — Commit and push ownership (settlement of a contradiction between the Dev and Release cards).

- **Dev (t_ebf21f32) owns the implementation commit**: message exactly `Remove decorative diamond from blog post cards`, containing exactly the 6 files of D1 (no untracked files — `AGENTS-blog-spec.md`, `data/`, `js/`, `tests/`, `scripts/__pycache__/` are NOT part of ACE-26). Push to `dev-origin` `main` via `git -c credential.helper="/usr/bin/gh auth git-credential" push dev-origin main`. The dev card's own "no commit/push" wording is superseded: **Release (t_7e23b99d) then owns only the dev→prod merge + live curl verification**, per the Illya gate. (Matches the ACE-24 precedent: BA spec commit and dev implementation commit are distinct; Release parks on human approval.)
- Pushing deploys `dev.acewerk.com` — the precondition for unblocking QA.

## 3. Acceptance criteria (testable)

- **A1 — Zero references.** In the post-change repo: `git grep -n "post-card-glyph\|9670"` over all tracked files returns **zero** hits; no `◆` character remains in any `blog/**` file or in `scripts/build_blog.py`.
- **A2 — No regeneration drift.** After Dev regenerates, each of the 4 generated pages is **byte-identical** to a fresh `python3 scripts/build_blog.py` run performed out-of-tree with the committed `content/` + `scripts/` (diff -r clean).
- **A3 — Card structure.** On live `dev.acewerk.com/blog/?t=<ts>`: all 3 `.post-card` articles exist; the first child element inside each is `.post-card-meta`; `getComputedStyle` on each card: `padding: 24px` (all sides), `gap: 14px`; `document.querySelectorAll('.post-card-glyph').length === 0`. Viewports: 1440×900, 768×1024, 390×844 (Chromium only, headless=new, per QA card).
- **A4 — Post pages pinned.** The three `blog/dev-fixture-*/index.html` files differ from HEAD **only** by the 7-line CSS-rule deletion: `.post-title` / `.post-byline` markup byte-identical, exactly one diff hunk each.
- **A5 — Diff-scope pin.** The whole diff (6 files, expected shape +1/−44) contains **no** change to `.post-card` gap/padding, card border/radius/background/backdrop, hover/active rules, inter-element spacing, typography, `.post-grid` gap, page header, search bar, or post count — verifiable by reading the diff hunk by hunk.
- **A6 — Hygiene.** No console errors on the 4 blog pages; HTML tag balance intact (article/span/div/a counts match); `services/index.html` byte-identical to HEAD.
- **A7 — Single commit.** Exactly one commit, message exactly `Remove decorative diamond from blog post cards`, on `dev-origin` `main`, containing exactly the 6 files of D1, and pushed (live page reflects the change after deploy).

## 4. Edge cases

- **E1 — Redundant margin.** The glyph's `margin-bottom:14px` was inert under the flex gap; QA must confirm no residual 14px phantom space above the date row (i.e., date row top = 24px from card edge, measured, not assumed).
- **E2 — JS/search independence.** The glyph span was `aria-hidden` and class-addressed by no JS; `search-index.json`, the inlined `#search-index` script, and `blog.js` behavior are unchanged (A2 + A6 cover it).
- **E3 — A11y neutral.** Removing a decorative `aria-hidden` span changes no accessible name, landmark, or focus order.
- **E4 — Diamond instances elsewhere.** `.svc-card-glyph` in services pages is a different component (A6 pins `services/index.html` byte-identical); `content/posts/*.md` contain no glyph.
- **E5 — Fixture pages carry the rule with no card.** Their inlined `CSS` template is shared, so the CSS rule must be deleted there too (D1); a "no glyph markup" check alone would miss it (A1 catches it).
- **E6 — Regen drift / stale untracked files.** The pre-existing uncommitted working-tree diff must not be committed as-is on top of later ACE-25 changes; Dev's commit must be generated from the current tree state (D5), and untracked files excluded (A7).
- **E7 — Grid reflow.** Card height drops ~22.4+14px; `repeat(auto-fill, minmax(300px,1fr))` column count is width-driven only — no reflow at any of the 3 viewports; A3 measurements confirm uniform card heights per row.

## 5. Files touched (for the Dev card t_ebf21f32)

1. `scripts/build_blog.py` — delete CSS rule (659–665) + markup line (1136).
2. `blog/index.html` — regenerate (removes CSS rule 356–362 + 3 spans).
3. `blog/dev-fixture-short/index.html` — regenerate (CSS rule only).
4. `blog/dev-fixture-long/index.html` — regenerate (CSS rule only).
5. `blog/dev-fixture-truncation/index.html` — regenerate (CSS rule only).
6. `docs/design/blog-design.md` — markup sample + bullet + stale clause.

## 6. Pipeline note

Design (t_76d2d0ce) is running — its geometry spec must equal D2 (24px/14px, no compensation; measure, don't guess). Dev's uncommitted working-tree state matches this spec exactly (BA-verified byte-identical to a clean regeneration), so Dev's remaining work is commit + push + A7. QA unblocks on the push. Release remains PARKED on the Illya gate.

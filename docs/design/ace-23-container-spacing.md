# ACE-23 — Container spacing token spec (gutter parity + post top margin)

- Change ID: ACE-23
- Layer: **Design (design-agent)** — CSS form + design-system update + trade-off rationale. No site code is edited here.
- Upstream (authoritative): BA spec, task `t_e3c51f99` — `docs/design/ace-23-container-margin-parity.md`, FROZEN (D1–D5, A1–A13, E1–E9).
- Source of truth: repo `ACE-WERK/acewerk-dev` `main` @ `b718d7d` (`~/projects/acewerk.com`, remote `dev-origin`) + **live** `dev.acewerk.com`, re-measured independently by Design with Playwright headless Chromium at 1440/768/390 on 2026-09-05 (raw data: `ace23_measure.json` in the design workspace).
- Downstream: Dev (`t_ac437bbd`) implements → QA (`t_0a77c351`) validates → Release.

Status: **CONFIRMED** — Design concurs with BA D1–D5, locks the exact CSS form, answers BA's two flagged questions (§2.4, §3.3), and adds **one correction** to a BA acceptance target: A4's 768px post-page shell-top (92.95 → **84.95**; §3.4). Nothing else is re-decided.

---

## 1. Verdict — the unified container rule (ISSUE 1)

### 1.1 Canonical gutter (confirming BA D1)

The canonical content gutter for **every** page is:

```css
padding: 0 clamp(20px, 4vw, 48px);
```

Resolves to: 20px @390 · 30.72px @768 · 48px @≥1200 (48px @1440). This is the value
the user referenced, the value the generated blog pages already ship, and the value
both `.content-wrap` and the blog `.site-container` rules already use.

### 1.2 The canonical container stack (what this spec freezes)

Every content page shares this exact stack; all four layers are pinned here with
their **complete** rules so future pages and `build_blog.py` have one reference:

```
.page-wrapper            — nav clearance (NOT a gutter)
.nav-bar                 — fixed bar, height 52 / 44px (NOT a gutter)
  .header-inner-wrapper.site-container   — nav row, SAME container geometry
main
  .content-wrap.site-container           — THE gutter (the rule that matters)
    .content-shell                        — glass card; inner text padding (NOT a gutter)
      [.hero-shell on the FIRST content shell only]  — top/bottom breathing
```

### 1.3 Exact CSS (canonical forms)

```css
/* 1) Gutter — the winning rule for .content-wrap.site-container AND the nav row.
       This is the rule that must be IDENTICAL on every page. */
.site-container {
  width: 100%;
  max-width: 1100px;          /* = --max-width */
  padding: 0 clamp(20px, 4vw, 48px);
  margin: 0 auto;
}

/* 2) Content wrap — belt-and-suspenders, already identical on every page
       (both blog and non-blog pages ship this). NOT changed by ACE-23. */
.content-wrap {
  max-width: 1100px;          /* = --max-width */
  margin: 0 auto;
  padding: 0 clamp(20px, 4vw, 48px);
}

/* 3) Glass shell — inner text padding; UNCHANGED by ACE-23. */
.content-shell {
  /* …existing background/border/shadow… */
  padding: clamp(26px, 4vw, 56px) clamp(22px, 4vw, 56px);
}

/* 4) Hero top/bottom breathing — applied to the FIRST content shell of a page.
       UNCHANGED by ACE-23; consumed by post pages via the D3 class. */
.hero-shell {
  margin-top: clamp(24px, 4vh, 44px);
  margin-bottom: clamp(18px, 3vh, 30px);
}
```

### 1.4 The exact change (confirming BA D2 — one line × 3 files)

On `services/index.html`, `our-team/index.html`, `contact/index.html`, change the
**end-of-sheet** `.site-container` rule (the one that currently wins the cascade)
from

```css
.site-container {
  width: 100%;
  max-width: 1100px;
  padding: 0 48px;             /* ← FIXED */
  margin: 0 auto;
}
```

to

```css
.site-container {
  width: 100%;
  max-width: 1100px;
  padding: 0 clamp(20px, 4vw, 48px);   /* ← D1 clamp; identical to blog */
  margin: 0 auto;
}
```

- `width`, `max-width`, `margin: 0 auto` untouched. No other rule, media query,
  or declaration changes.
- **`.content-wrap` on these pages is NOT touched** — it already carries the D1
  clamp and is not the winning rule (equal specificity, earlier in the sheet).
  Leaving it is deliberate: both declarations then resolve to the same value, so
  the cascade is redundant-but-harmless and the diff stays 1 line per file.
- No blog-side gutter edit is needed (blog already ships the D1 clamp).

### 1.5 Header alignment question (BA §6 Q1 → ANSWER)

**No matching change to the `@media (max-width: 700px)` nav rule is required.**
Confirming BA:

- The D2 rule change resolves to **48px ≥1200px** → the ≥701px nav row is
  byte-identical at 1440 (logo x=218) and shifts only in the 701–1199px band,
  where it **converges to the blog nav's position** (see §1.6).
- The ≤700px override on the 3 non-blog pages
  `.nav-bar .header-inner-wrapper.site-container { max-width: none; padding: 0 clamp(16px, 4vw, 32px); }`
  has **higher specificity** (0,2,1 + element) than the base `.site-container`
  rule, so it wins regardless of the base padding — the mobile nav stays
  `max-width: none` with its own 16→32px gutter. At 390px the logo stays at x=16
  (verified pre- and post-change, since the override governs). **Do not edit it.**
- Blog pages have no such override and keep the shared 20→48 clamp on the nav row
  — already parity with the D2 target. Both pre-existing states are untouched.

Design ruling: the nav's own tighter 16→32px mobile gutter (full-bleed bar) is a
**separate, intentional** decision from the content gutter and stays as-is. The
two scales coexisting (nav 16→32 full-bleed vs content 20→48) is the existing
design language and is not part of this defect.

### 1.6 Verified parity after the change (Design's live measurements)

Measured live pre-fix; post-fix values derived from the cascade (clamp resolves
deterministically) — QA re-measures per A1–A3:

| Viewport | nav row (services/our-team/contact) | logo x | content shell |
|---|---|---|---|
| 1440×900 | x=170, w=1100, padL=48 (unchanged) | **218.0** (unchanged) | x=218, w=1004 (unchanged) |
| 768×1024 | x=23.03, w=**706.56**, padL=**30.72** (was w=721.94, padL=48) | **53.75** (was 71.03) — now **== blog nav** (53.75) | x=**30.72**, w=**706.56** (was x=48, w=672) — now == blog |
| 390×844 | x=0, w=390, padL=16 (override wins, unchanged) | **16.0** (unchanged) | x=**20**, w=**350** (was x=48, w=294) — now == blog |

At 1440px the nav row and the content wrap are pixel-aligned (x=170/w=1100,
logo x=218 == shell x=218); after the fix that alignment **extends down to
701px** (nav and content share one rule end-to-end) and below 700px the
higher-specificity override keeps the full-bleed nav bar. The 768px logo shift
(71.03 → 53.75) is an **intended parity gain**, not a regression — it removes the
existing nav/content x-mismatch on non-blog pages. QA should visually confirm it
reads as alignment, not a jump (A6/E6).

Overflow: `scrollWidth == innerWidth` on all five measured pages at all three
viewports pre-fix; the fix only narrows outer padding, so A9 holds by construction.

### 1.7 Follow-up (NOT part of ACE-23)

After ACE-23, `.content-wrap`'s padding on the 3 non-blog pages is redundant
(equally-specified, later `.site-container` wins, same value). A later cleanup
may consolidate container geometry onto `.site-container` alone and delete the
`.content-wrap` padding — **do not bundle it here** (A11 scope guardrail: the
diff must stay 1 line × 3 files).

---

## 2. Post-page top spacing (ISSUE 2)

### 2.1 Verdict (confirming BA D3 — markup only, no new CSS)

Add the existing `hero-shell` class to the post article shell:

```html
<!-- before -->
<div class="content-wrap site-container">
  <div class="content-shell reveal">

<!-- after -->
<div class="content-wrap site-container">
  <div class="content-shell hero-shell reveal">
```

- No new CSS rule. The already-present `.hero-shell { margin-top: clamp(24px, 4vh, 44px); margin-bottom: clamp(18px, 3vh, 30px); }` (identical on every page, §1.3) now applies to the post shell.
- Rejected alternative (dedicated `.post-page`/`.post-hero` wrapper or a
  `.post-shell { margin-top: … }` rule): it would duplicate an existing token and
  add CSS to maintain for zero rendering difference. The article header **is**
  the page hero, so `hero-shell` is semantically honest, not a name stretch.
- Rejected alternative (padding-top on the post shell): padding would inflate the
  glass card (visible inside the border) instead of lifting it — wrong visual.
- `margin-top` on `.content-shell` directly (no class) is rejected: `.content-shell`
  is shared by all shells site-wide; the class keeps the intent explicit.

### 2.2 Exact change (confirming BA D3/D4 — one line × 4 files)

- `scripts/build_blog.py`, `build_post_page`, **line 1245**:
  `'        <div class="content-shell reveal">\n',`
  → `'        <div class="content-shell hero-shell reveal">\n',`
  (line 1196 = blog-index hero shell, line 1203 = blog-index grid shell — both
  already correct; do not touch.)
- `blog/dev-fixture-short/index.html` **line 669**, `blog/dev-fixture-long/index.html` **line 669**, `blog/dev-fixture-truncation/index.html` **line 669**: same single-line class addition.
- Source of truth = `build_blog.py`; regenerate and hand-patch must be identical (BA D4/A8/E5).

### 2.3 Expected shell-top numbers (locked for Dev + QA)

Post pages run the **blog nav** (44px at ≤768, 52px ≥769 — see §3.4), so post
shell-top == blog-index shell-top at every viewport. `margin-top` resolves:
24px floor @≤600vh · 4vh @600–1100vh · 44px cap @≥1100vh.

| Viewport | post shell y (after) | margin-top | == blog index y | == non-blog hero y |
|---|---|---|---|---|
| 1440×900 | **88.0** | 36px | 88.0 ✓ | 88.0 ✓ (52+36) |
| 768×1024 | **84.95** | 40.96px | 84.95 ✓ | **92.95** ✗ (52+40.96) — see §3.4 |
| 390×844 | **77.75** | 33.76px | 77.75 ✓ | 77.75 ✓ (44+33.76) |

Pre-fix post shell y: 52 / 44 / 44 (flush under the nav) → the fix lifts it to
the canonical hero position at every viewport.

### 2.4 Naming question (BA §6 Q2 → ANSWER)

`hero-shell` on the post article shell is **confirmed, not vetoed**. The article
header (back-link + title + byline) functions as the page's hero; reusing the
existing class is the minimal, maintainable form. Dev: use `hero-shell`, do not
introduce `.post-hero`.

### 2.5 `margin-bottom` consequence (BA E8, confirmed expected)

The class also applies `margin-bottom: clamp(18px, 3vh, 30px)` (18/27/21px at
390/768/1440). The post shell is the last block before the footer, so this adds
breathing room above the footer — parity-consistent with every hero shell on the
site. **Expected, not a regression.** QA notes it (A4/E8).

---

## 3. Design-system update (BA D5 — this doc is the new canonical reference)

Checked `docs/design/` @ `b718d7d`:

- `blog-design.md` — specifies the blog shell **locally** (`.site-container`
  clamp, `.hero-shell` margins, `.content-shell` padding as blog values) but its
  scope is `/blog/` only. It never states that these are the **cross-page** rules.
- `ace-21-blog-card-metadata.md`, `ace-22-post-body-width.md` — reference
  `.site-container` / `.content-shell` as context; neither defines container
  geometry.
- No other container/spacing token doc exists.

**Conclusion: the design system does not currently specify the cross-page
container rules.** This document **is** the correction and becomes the canonical
spec: §1.3 is the single reference for `site-container` + `content-wrap` +
`content-shell` + `hero-shell`/post-top for all pages and for `build_blog.py`.
A pointer line is added to `blog-design.md` (§3.2).

### 3.1 Canonical token table (for the design system)

| Token / value | Meaning | Where |
|---|---|---|
| `--max-width: 1100px` | container cap | all pages `:root` |
| `clamp(20px, 4vw, 48px)` | **content gutter** (`.site-container` padding; canonical) | all pages |
| `clamp(16px, 4vw, 32px)` + `max-width: none` | **nav-bar-only** mobile gutter, ≤700px, non-blog pages | 3 pages' `@media (max-width: 700px)` |
| `clamp(26px, 4vw, 56px) clamp(22px, 4vw, 56px)` | shell inner text padding | all pages `.content-shell` |
| `clamp(24px, 4vh, 44px)` | hero/page top breathing (vh-scaled) | all pages `.hero-shell` |
| `clamp(18px, 3vh, 30px)` | hero/page bottom breathing | all pages `.hero-shell` |
| `52px` / `44px` (`--nav-height` / `--nav-height-mobile`) | fixed nav height | all pages |

### 3.2 Pointer added to `blog-design.md`

§1 (tokens) gains one line under the reused-tokens block, cross-referencing this
doc as the cross-page canonical container spec (added alongside this commit; see
`docs/design/blog-design.md` @ the ACE-23 design commit).

---

## 4. Corrections to the BA acceptance list (Design's verification)

**A4 (post top spacing) — 768px target corrected: 92.95 → 84.95.**

BA A4 states post shell `y` must equal the non-blog hero shells "at the same
viewports", listing y=92.95 @768. Design's live measurement shows this is
**impossible on post pages**: post pages run the **blog nav**, whose height is
**44px at ≤768px** (`@media (max-width: 768px) { .nav-bar { height: var(--nav-height-mobile); } }` — blog pages have no 700px-height override, unlike the non-blog pages). So:

- 768×1024: post shell y = 44 + 40.96 = **84.95** (== blog index 84.95). The
  92.95 figure belongs to non-blog pages only (52 + 40.96).
- 1440 and 390 BA targets are correct (88 / 77.75) and hold.
- The 40.96px margin-top itself matches BA exactly at 768 — only the absolute
  shell-top target was off by the 8px nav-height delta.

**Corrected A4 (Design-signed):** post shell `margin-top` ==
`clamp(24px,4vh,44px)` (36/40.96/33.76px @1440/768/390) **and** post shell y
== **blog index** shell y at the same viewport (88 / **84.95** / 77.75). QA
should assert the margin-top value and the blog-index parity, not equality with
the non-blog absolute y (which is structurally 8px higher at 768).

**Observation (out of ACE-23 scope, follow-up candidate):** at 768px the
**nav bar height itself differs** between page families — blog 44px vs
non-blog 52px (non-blog carries no ≤768 nav-height override; its 44px rule is
≤700px). That 8px seam difference predates ACE-23 and is untouched by it. If the
team wants one nav height at 701–768px, that is a separate change.

---

## 5. Trade-off rationale (short)

**Gutter scaling (why `clamp(20px, 4vw, 48px)`):**
1. It is the user's stated reference and the value the generated blog pages ship
   — unifying the 3 hand-maintained pages to it is the minimal, forward-safe
   direction (new blog posts inherit it automatically).
2. The 4vw slope scales proportionally with screen size (20→48px across
   500→1200px); at ≥1200px it hits the 48px ceiling, so desktop (1440) is a
   byte-identical no-op — zero risk to the working desktop layout.
3. At 390px the shell gains 56px of content width (294 → 350px) and the
   nav/content x-mismatch disappears at 701–768px (logo 71.03 → 53.75, == blog).
   Rejected alternatives: fixed 48px everywhere (kills the mobile scaling the
   user asked for), a new bespoke clamp (a magic number with no precedent),
   or scaling the blog down (inverts the reference).

**Post top spacing (why `hero-shell` reuse, same `clamp(24px, 4vh, 44px)`):**
1. The defect is *absence of breathing room* — every page's first shell is
   lifted by exactly this margin; the only page family without it is the
   generated posts. Reusing the token restores one site-wide rule ("the first
   content shell floats below the nav") instead of introducing a second,
   near-identical one.
2. The 4vh component scales the gap with **screen height**, so it reads
   proportional on phones (33.76px @390) and tall desktops (36px @900, 40.96px
   @1024) — a fixed px margin would feel cramped on tall screens.
3. Markup-only (1 line × 4 files): no new CSS to maintain, no selector-specificity
   questions, and the `build_blog.py` template + generated pages stay in lockstep
   (A8). Rejected: new `.post-hero` (naming-only difference, +1 class to maintain),
   shell padding-top (inflates the glass card visibly — wrong visual),
   bare `.content-shell { margin-top }` (shared selector, implicit intent).

---

## 6. What QA should visually verify (design sign-off view)

- **1440px, all pages:** byte-identical to baseline — no shift anywhere (A1/A10).
- **768px, services/our-team/contact:** content shell x=30.72/w=706.56 == blog;
  nav logo sits at 53.75 (== blog) — reads as *alignment*, not a jump (A2/A6).
- **390px:** all six pages share shell x=20/w=350; nav logo unchanged at 16; no
  horizontal scrollbar (A3/A9).
- **701–768px band (spot-check ~730px):** nav logo converges toward blog position
  smoothly with width; no abrupt jump (E1 + §1.6).
- **3 post pages:** shell floats below the nav with the same gap as the blog
  index at each viewport (88/84.95/77.75); new bottom breathing above the footer
  is expected (A4 corrected, E8).
- **Nav panel (hamburger) at ≤768px:** opens/closes identically to pre-fix;
  panel top unaffected (A6).

Evidence (this workspace): `ace23_measure.json` — live pre-fix measurements,
5 pages × 3 viewports (shell/wrap/nav/navInner boxes, logo x, margins, overflow).

---
End of design spec (ACE-23, design-agent).

# DESIGN SPEC — ACE-22: .post-body width parity (header / fixture-note)

Change ID: ACE-22
Layer: Design (design-agent) — confirms CSS form + trade-off rationale; no code.
Upstream (authoritative): BA SPEC, task t_f258ac6f, frozen (D1–D6, A1–A4).
Source of truth for current state: repo ACE-WERK/acewerk-dev main @ d1d47b4
(~/projects/acewerk.com, remote dev-origin) + live dev.acewerk.com, measured
Playwright headless Chromium 1440/1920/768/390px, 2026-09-05.
Downstream: Dev (t_fdafbfd4) implements; QA (t_2cbaff0f) validates A1–A4.

Status: CONFIRMED — design concurs with BA's D1–D4 and the two-line deletion.
This doc adds the trade-off rationale Dev/QA/BA asked for and locks the
expected alignment numbers. It does NOT re-decide any BA-owned decision.

---

## 1. Verdict (the CSS form)

CONFIRMED: In the `.post-body` base rule, DELETE exactly these two declarations
and nothing else:

      max-width: var(--measure-prose);
      margin: 0 auto;

Resulting rule (identical in template + all 3 pages):

      .post-body {
        color: var(--ink);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 300;
        font-size: var(--fs-body);
        line-height: 1.75;
      }

Why pure deletion (and not an equivalent):
  • `.post-body` is a block-level child of `.content-shell`. With no width
    constraint it fills the shell's content box by default — the exact behavior
    `.post-header` and `.fixture-note` already have. No `width: 100%` needed.
  • `max-width: none` is a RENDER-EQUIVALENT but it is a substitution (modifies
    one line + deletes one), not a pure deletion. BA acceptance A4 requires the
    diff to contain ONLY the two deleted lines ×4 files. Pure deletion is the
    only form that satisfies A4 and keeps the diff minimal. → Prefer deletion.
  • Do NOT add a `width`, do NOT add `max-width: none`, do NOT re-center.

Token: keep `--measure-prose: 720px;` in :root (unchanged, now unreferenced),
per BA D2. Flagging its removal as an OPTIONAL follow-up only (§6) — not part
of this change.

Typography: FROZEN per D3. font-size var(--fs-body), line-height 1.75,
font-weight 300, color var(--ink), and every descendant rule under .post-body
stay byte-identical. Design confirms no typographic re-tuning is needed or
wanted for this change.

---

## 2. Trade-off: prose measure (720px) vs width parity (890px)

This is the design decision the task asked Design to own. Both options are
defensible; parity wins here. Rationale, with measured numbers:

THE OLD 720px MEASURE (the "typographic ideal"):
  • Classic long-form reading guidance is ~65–75 chars/line. At 720px with
    Space Grotesk 300 @ 18px (≈9.27px/char measured), the 720px column gives
    ≈77 chars/line — essentially at the ideal. That is the only real argument
    the old measure had.

THE NEW 890px PARITY (the fix):
  • At 890px the same type gives ≈91 chars/line. That is ABOVE the 65–75
    classic band. So the fix does make lines somewhat longer — this is the
    cost, stated honestly.
  • Why the cost is acceptable (why parity still wins):
    1. LINE-HEIGHT OFFSETS IT. Body leading is 1.75 (31.5px on 18px type) —
       generous. Long lines paired with tall, relaxed leading is the standard
       mitigation for wide columns; reflow is comfortable, not strained.
    2. BOUNDED, NOT UNBOUNDED. The column is capped at 890px content width at
       every viewport ≥ ~980px, because `.site-container` max-width:1100px
       clamps the shell. At 1920px the column is STILL 890px (verified), so
       ultra-wide monitors do not produce ever-longer lines. The worst case is
       a fixed ~91 cpl — not a runaway width.
    3. ALIGNMENT > COLUMN WIDTH for this page. The page's visual identity is a
       single left-aligned editorial stack (breadcrumb, title, byline,
       fixture-note banner, body) inside one glass card. The old measure broke
       that: a 720px column centered inside an 890px shell left an 85px inset
       on each side, so the prose visibly "floated" away from the title, byline
       and the amber banner. That misalignment is the reported defect and is a
       STRONGER visual blemish than a modestly longer line. Parity restores one
       clean left edge across the whole article — a more intentional, editorial
       look.
    4. THE PROSE IS STAGING FIXTURES, NOT LONG ESSAYS. The three pages are
       short markdown-demo fixtures ("Field Guide to the Markdown We Support").
       Long-form measure matters most for dense multi-thousand-word essays; here
       the reading burden of +14 cpl is negligible, while the alignment gain is
       fully visible on every post page.

DECISION: parity (full shell content-box width, matching `.post-header` /
`.fixture-note`) — consistent with BA D1. The ~77→91 cpl change is accepted as
the price of a single, clean, aligned article block; leading + container cap
keep it comfortable and bounded.

Rejected alternatives (for the record):
  • Keep 720px measure → perpetuates the 85px inset misalignment (the bug).
  • Widen to an explicit `max-width: 890px` centered → same parity at 1440 but
    re-introduces a magic number, breaks parity at viewports where the shell
    content box is not exactly 890px, and is a substitution (fails A4's
    delete-only diff). Parity via natural block fill is cleaner and self-
    adjusting.
  • Center a new wider measure → same re-centering cost; no benefit.

---

## 3. Expected alignment (locked numbers for Dev + QA)

Measured live (Playwright, Chromium) BEFORE fix, and re-measured with the two-
line deletion injected as a style override (the fix) — results below.

Desktop 1440x900 (all 3 fixture pages, identical):
  .content-shell  1004px
  .post-header     890px   left x = 275
  .fixture-note    890px   left x = 275
  .post-body       890px   left x = 275   (was 720px / x=360, 85px inset)
  → width parity ±1px AND equal left edge x=275. (Matches BA D6, A1.)

Ultra-wide 1920x1080 (container cap keeps parity):
  .post-header / .fixture-note / .post-body  all 890px, x = 515.
  → parity holds at any wide viewport; line length capped (see §2.2 cost #2).

Mid 768x1024:
  .post-header / .fixture-note / .post-body  all 643px, x ≈ 62.4.
  → already parity pre-fix (content box 643px < 720px max, measure never
    engaged). Fix is a no-op here — no regression possible.

Mobile 390x844 (the <=768px requirement):
  .content-shell  350px
  .post-header     304px   left x = 43
  .fixture-note    304px   left x = 43
  .post-body       304px   left x = 43   (unchanged)
  → .post-body ALREADY matches the other elements' width on mobile (304px ==
    siblings). The max-width:720px never engaged at 304px, so deleting it
    changes nothing there. REQUIREMENT SATISFIED BY CONSTRUCTION: mobile
    .post-body width is invariant at 304px / x=43, no horizontal overflow,
    no layout shift in header/fixture-note/byline. (Matches BA A2, E3.)

Where the fix actually takes effect: only at viewports where the shell content
box > 720px (≈ ≥980px). In the 769–~980px band the content box is already
<720px so .post-body was already full width — the change is a visual no-op
there (BA E2). Net: the fix is desktop-effective; mobile ≤768px is provably
untouched.

---

## 4. Confirmed non-negotiables (D1–D4 compliance)

  D1  Alignment = full shell content-box width (parity with .post-header /
      .fixture-note). ✓ Confirmed. Not a widened measure, not re-centered.
  D2  --measure-prose stays in :root, unreferenced. ✓ Confirmed. No cleanup.
  D3  Typography FROZEN (body + all descendants). ✓ Confirmed. Untouched.
  D4  Scope guardrail: ONLY the .post-body base rule changes. ✓ Confirmed.
      No .post-header / .fixture-note / .post-byline / .content-shell /
      .site-container / media-query / noindex edits.
  (D5 source-of-truth = build_blog.py, one commit; D6 expected 890px/890px —
   both BA-owned, unchanged, and re-confirmed by §3 measurements.)

---

## 5. Edge cases (design view, aligns BA §5)

  E1  Wide code blocks: .post-body pre has overflow-x:auto. Verified at 890px:
      pre clientWidth == scrollWidth == 888 (no current fixture line overflows;
      max pre line = 37 chars). If a future long code line appears, it scrolls
      INSIDE the pre block (inset), not at page level. Acceptable — no action.
  E2  769–~980px band: no-op (content < 720px already full width). ✓.
  E3  Mobile ≤768px: invariant 304px / x=43 (390px measured). ✓ no regression.
  E4  Ultra-wide >1200px: capped at 890px by .site-container max-width:1100px.
      ✓ bounded, verified at 1920px. Design notes the ~91 cpl trade-off;
      accepted per D1 (see §2).
  E5  Regeneration drift: if build_blog.py output differs from committed pages
      beyond the .post-body rule, do NOT absorb silently — report and hand-
      patch the 3 pages identically (BA-owned; Dev executes).
  E6  No-JS / reduced-motion: pure CSS; no JS, no interaction, no motion impact.

---

## 6. Optional follow-up (NOT part of ACE-22)

  • Remove the now-unreferenced `--measure-prose: 720px;` token in a separate,
    later cleanup commit if the team wants a lean :root. Out of scope here
    (BA D2 keeps it). Do not bundle with ACE-22 (A4 diff purity).

---

## 7. What QA should visually verify (design sign-off view)

  • At 1440px, all 3 pages: the body prose LEFT and RIGHT edges align exactly
    with the title/byline and the amber fixture-note banner — one clean left
    guide, no floating inset. (Design's primary aesthetic goal.)
  • No text touching the shell padding; spacing/rhythm between heading,
    paragraphs, banner, byline unchanged.
  • At 390px: layout byte-identical to pre-fix (parity already held); no
    horizontal scrollbar; code blocks behave.
  • Wide `pre` (if present) scrolls internally, page does not.

Screenshots (evidence, in this workspace):
  baseline-1440-top.png   pre-fix: prose inset 85px from header/banner edges
  after-fix-1440-top.png  post-fix (2 lines removed): prose edges == banner edges
  baseline-1440.png, baseline-1440-code.png, baseline-390.png  reference

---
End of design spec.

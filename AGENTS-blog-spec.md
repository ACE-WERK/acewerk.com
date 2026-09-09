# AceWerk Blog Build — Frozen Requirements (authoritative)

Source: Illya's autonomous task brief (2026-09-05). This file is the frozen spec
for the whole blog run. Any card or design decision conflicts with THIS file:
this file wins.

TIME_BOX = 6 hours · BRANCH = feature/blog (in ACE-WERK/acewerk-dev) · WORK REPO = /home/illya/projects/acewerk.com

## 0. Hard constraints
- Work only in the acewerk-dev repo (remote: dev-origin), working tree /home/illya/projects/acewerk.com.
- Branch feature/blog from dev-origin/main (no dev integration branch exists).
- Push target is dev only. Never commit/push to main. No production tag, deploy, release, or publish. No production config or hosting changes.
- No new framework, bundler, CSS library, or CMS. Use what the repo already uses (plain static HTML + GitHub Pages). If a new dependency seems genuinely required, park a blocker card instead of installing.
- Do not modify the WebGL mosaic shaders, geometry, or render loop except where section 5 explicitly allows (static backdrop replaces mosaic ONLY on blog routes).
- No secrets, API keys, analytics, or third-party scripts.
- Scope is frozen. Anything not in section 3 goes on the backlog as a card, not into this build.

## 3. Requirements

### 3.1 Navigation
- Add a Blog entry to the top nav. It is the last item in the list.
- Blog is visually distinguished from the other nav items, but subtly. design-agent decides the treatment. Must NOT read as a CTA button or promotional badge.
- Mobile: replace the nav with a hamburger menu anchored to the right. The logo hyperlink stays exactly where it is on the left, unchanged.
- Hamburger: aria-expanded + aria-controls on the trigger; focus moves into the panel on open and returns to the trigger on close; Esc closes; background scroll locked while open; focus trapped in the panel.
- Hamburger breakpoint is chosen by design-agent and recorded in the design system, not hardcoded ad hoc in one stylesheet.
- Desktop nav behaviour otherwise unchanged.

### 3.2 Blog index — /blog/
- Reverse-chronological timeline, newest first.
- Each post is a card component. Clicking anywhere on the card opens the full post.
- Card shows at minimum: title, publish timestamp, author, excerpt. design-agent decides on thumbnail/tag/read-time and defines truncation rules for long titles and excerpts.
- Search: per 3.6. Pagination: per 3.7.
- Defined empty state for zero posts.

### 3.3 Post page — /blog/<slug>/
- Full post with title, publish timestamp, author.
- Timestamps use semantic <time datetime="..."> with ISO value; visible format is design-agent's call, consistent across card and post page.
- In-page back control returning to /blog/, labelled as a Blog link (e.g. ← Blog). Real anchor to /blog/, not history.back().
- Post body content must be real HTML in the DOM. No hidden text, no cloaking.

### 3.4 Content model
- Posts authored as source files in the repo (markdown or existing content convention) with front matter: title, slug, date, author, excerpt, optional tags. BA confirms exact format against the repo inventory.
- Each post builds to a real static HTML page at its own URL. No client-side-only routing for post pages.
- Adding a new post in future must require only adding a source file. Document in content/README.md.

### 3.5 Sample content
- Three lorem ipsum sample posts (not one). One short, one long with headings/lists/blockquote/inline links, one with unusually long title and long author name (truncation test). Distinct dates. Clearly marked as dev-environment fixtures.

### 3.6 Search spec
No search library, no fuzzy matching, no stemming, no ranking.
- Build step generates a static JSON index: one entry per post with title, excerpt, author, date, slug, and body text stripped of markup.
- Matching: lowercase both sides, split query on whitespace, a post matches if EVERY token appears as a substring in ANY indexed field. Results stay reverse-chronological.
- Input debounced 200ms, minimum 2 characters, clear (×) control.
- Query reflected in URL as ?q= (linkable, survives refresh and browser back).
- Filtering resets pagination to page 1.
- Distinct no-results state that echoes the query and offers one-click clear.
- If the generated index exceeds ~200KB, fetch it lazily on first focus of the search field rather than page load.
- With JavaScript disabled, the full post list still renders; the search input is hidden rather than shown broken.

### 3.7 Pagination spec
- Page-size selector: options 5, 10, 20; default 5.
- Reverse-chronological order preserved across pages.
- Numbered pages plus prev/next. design-agent defines the component and disabled/current states.
- State in URL alongside search: ?q=&size=&page=. Selected page size persists across searches; changing page size returns to page 1.
- Pagination is client-side over the fully rendered list, so a JS-disabled visitor sees every post, not a truncated one.

## 4. Design system (design-agent owns and delivers)
- Blog post card component: anatomy, states (default/hover/focus-visible/active), behaviour in the glass-tile visual language.
- Long-form prose style set for post bodies: h2/h3/h4, paragraph rhythm and measure, lists, blockquote, inline links, code blocks, images with captions, horizontal rules. Does not currently exist; largest design deliverable. dev-agent must not improvise it.
- Nav treatment for the Blog item and the mobile hamburger panel.
- Search input with no-results and empty states, pagination component including page-size selector.
- A static backdrop for /blog/ and post pages, replacing the WebGL mosaic entirely on these routes. Solid, gradient, or geometric shapes, built from existing design tokens. Documented as a page-level backdrop variant in the design system.
- Any new tokens go into the existing token layer with names consistent with current conventions.

## 5. Cross-cutting non-negotiables
- Accessibility: semantic landmarks (nav, main, article, time), visible focus states, keyboard operability for nav and search, contrast checked against the backdrop at its brightest, prefers-reduced-motion respected for card/menu animation.
- Performance: blog routes use the static backdrop. The mosaic must NOT be instantiated on these pages: no Three.js import on the critical path, no WebGL context created, no shader compilation. Pausing the render loop is NOT sufficient. Verify in devtools that no WebGL context exists on /blog/. Record a Lighthouse score for /blog/ and one post page.
- Browsers: verify Safari specifically (glass/backdrop-filter over WebGL differs).
- Responsive: verify at 375, 768, 1024, 1440 px.

## 6. Anti-overconfidence clause
- Never state a test/build/check passed unless you have the actual command output in front of you. Paste command + real output into the card.
- Timed out / interrupted / not run = say exactly that.
- If you did not verify something, write "not verified" next to it.
- QA: a card cannot leave QA on reasoning or code reading. It needs artifacts.
- Do not claim a file/branch exists without listing it first.
- Supervisor: verify "in progress"/"done" against git log, git status, file timestamps every cycle.

## 7. Definition of done
1. Branch builds clean from a fresh checkout; build command and output pasted.
2. /blog/ renders three sample posts, newest first.
3. Clicking a card opens the correct post page at its own URL; back control returns to /blog/.
4. Direct navigation to a post URL works (not just in-app).
5. Search returns correct subsets, handles no results, reflects ?q= in URL, and the list still renders with JS disabled.
5b. Pagination works at sizes 5/10/20, defaults to 5, interacts correctly with active search.
5c. /blog/ and a post page create NO WebGL context; static backdrop renders instead.
6. Desktop nav shows Blog last with the agreed subtle treatment.
7. Mobile hamburger opens, closes, traps focus, closes on Esc, logo unmoved.
8. Screenshots at 375/768/1024/1440 px for /blog/ and one post page.
9. Playwright checks written and run for: index renders, card click navigates, back control returns, search filters and updates URL, page-size selector changes visible count, hamburger opens and closes.
10. Lighthouse run on /blog/ and one post page, scores recorded.
11. Design spec and token additions committed as documentation, not just code.
12. content/README.md explains how to add a post.

QA note: Playwright lives in the qa-agent venv on the host. Use the terminal tool. execute_code runs in a separate container and will not see that venv.

## 8. Out of scope (log as backlog cards, do not build)
- SEO metadata follow-up: Open Graph/Twitter tags, meta descriptions, canonical URLs, JSON-LD Article schema, sitemap entries, RSS/Atom. (NOTE: unique descriptive <title> per page and stable /blog/<slug>/ URL structure with real HTML in the DOM stay IN scope.)
- Comments, reactions, sharing buttons, newsletter signup, author profile pages, tag archive pages, related posts, CMS/admin UI, auth, i18n, drafts/scheduling, analytics, any real (non-lorem) content.

## 9. Final report (supervisor writes as a summary card at the end)
- What shipped; what was deferred and why.
- Every section-7 check marked verified or not verified, each with evidence.
- All open blockers with exact error output; any NEEDS-HUMAN cards.
- Diff stat for the branch + confirmation of what was pushed to dev (commit SHA).
- Supervision log: every stall detected, escalation-ladder rung used, every card that hit the three-attempt cap.
- Which stop condition ended the run.

## Supervisor loop (ba-agent)
- Every 10 min: read board; for each non-Done card compute time since last real update; verify claimed progress against git log/status/file mtimes (not the agent's report); confirm at least one card is actively moving; confirm nothing waits on a satisfied gate.
- Every 60 min: write a checkpoint card (cards moved, blocked, commands with real exit codes, attempt counts, remaining estimate).
- Stall: no board+filesystem+git change attributable to a card for 15 min; OR output but no artifact; OR 20 min in a stage with an available owner and no stated blocker; OR completion reported but verification shows nothing changed.
- Escalation ladder (record rung used on the card): 1. re-issue (restated AC + ask for next command), 2. narrow to smallest piece, 3. reassign to correct stage, 4. park after 3 attempts with exact error output and pull next card, 5. NEEDS-HUMAN card if parking blocks everything downstream.
- Cap: 3 attempts per card; never re-issue the same card text twice verbatim.
- Keep the pipeline full: always at least one card in an active stage; pull forward independent work (sample content, docs, Playwright scaffolding); move dependent cards to ready in the same cycle when a gate is satisfied; do not open new cards outside section 3.
- Stop conditions: all cards Done with evidence + branch pushed to dev + nothing blocked; OR time box expires; OR every remaining card parked + NEEDS-HUMAN written; OR same card fails QA 3x; OR build broken >20 min without fix; OR continuing would violate section 0.
- "Ready for production" = merged to dev, verified per section 7, awaiting human review. NOT deployed. The run never touches production.

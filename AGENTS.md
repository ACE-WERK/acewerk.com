# AGENTS.md — Rules for automated agents / tooling

Use this file as guidance whenever editing this repo.
These rules apply to ALL public-facing pages, not just index.html:
- index.html
- services/index.html
- our-team/index.html
- contact/index.html

## 1. Each page is the live canonical source

- The current version of each page in the repo is the live source of truth.
- Any design or feature change must be merged into the existing file.
- Never blindly replace a page with an older “design version” (e.g. indexV12) unless:
  - The user has explicitly named it,
  - And you understand what will be lost.

## 2. Things that must be preserved (unless explicitly asked to remove)

For index.html:
- Title and basic SEO:
  - `<title>Ace Werk — Product Studio for Design, Code, Localization & Growth</title>`
  - `meta name="description"` and primary meta tags.
- Branding:
  - The “Ace Werk” title styling (e.g. Orbitron or chosen brand font).
- CTA:
  - The “See what we do” call-to-action element (`#entercta` / `.enter-cta`).
- Core animation:
  - The WebGL vortex / wormhole canvas setup.
  - The `screenlink` and its click-to-enter animation configuration.
- a11y:
  - Canvas aria-label / role, structured headings, and noscript fallback.

For services / our-team / contact:
- All existing navigation links.
- All existing content blocks (no silent deletions).
- All SEO meta tags and structured headings.

If in doubt, keep it.

## 3. Merge, don’t overwrite

- When syncing from a design repo:
  - Prefer incremental changes (scripts, styles, layout tweaks).
  - Preserve existing CTAs, SEO, accessibility, animations, and content unless instructed otherwise.
- If a conflict appears between a “new design HTML” and current live version:
  - Ask the user; do not silently discard the live page.

## 4. Git rules

- Every meaningful change must be committed with a clear message.
- Include which page(s) you changed and why.

## 5. Dev/Production pipeline

Two repos under the ACE-WERK GitHub org:

| Repo | Branch | URL | Purpose |
|---|---|---|---|
| `ACE-WERK/acewerk.com` | `main` | `https://acewerk.com/` | Production |
| `ACE-WERK/acewerk-dev` | `main` | `https://dev.acewerk.com/` | Staging |

Rules:
- **All feature work goes to the dev repo first** (`ACE-WERK/acewerk-dev`).
- QA validates on `dev.acewerk.com` before any prod merge.
- **Dev repo**: `noindex` meta tags on all pages, `robots.txt` with `Disallow: /`, canonicals point to `acewerk.com` (production).
- **Prod repo**: NO `noindex` tags, NO `robots.txt` Disallow. All pages searchable.
- **Merge to prod**: strip `noindex` meta tags and `robots.txt` Disallow. Verify canonicals stay `acewerk.com`.
- **Internal links**: use relative paths only (`href="/"`, `href="/services/"`). Works on both environments without rewriting.
- **Git push**: use `git -c credential.helper="/usr/bin/gh auth git-credential" push` (fine-grained PAT fails with plain `git push`).

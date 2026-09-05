# CONTRIBUTING.md — How to work on AceWerk (acewerk.com)

This file is for humans and AI agents working on this repo.
It defines how to safely edit the site, especially its core pages,
without accidentally undoing previous work.

These rules apply to:
- index.html
- services/index.html
- our-team/index.html
- contact/index.html

## 1. Each page is the live canonical page

- Each page is the production source of truth.
- Any visual or interactive change must be merged into this file.
- Do NOT:
  - Replace a page with an older “design version” (e.g. indexV12)
    without explicitly confirming what will be lost.
  - Silently overwrite it from another file or branch.

## 2. Must-keep elements

Unless specifically asked to change, preserve:

For index.html:
- <title>Ace Werk — Product Studio for Design, Code, Localization & Growth</title>
  and primary meta tags / SEO.
- The “Ace Werk” title styling (Orbitron or current brand font).
- The “See what we do” call-to-action (#entercta / .enter-cta).
- The WebGL vortex / wormhole canvas and:
  - The screenlink element
  - The click-to-enter animation config
- Accessibility attributes (aria-label, headings, noscript fallback).

For services / our-team / contact:
- All navigation links (no broken or missing nav).
- All existing content sections.
- SEO meta tags and structured headings.

If you’re unsure, prefer keeping it.

## 3. Syncing from design repos

When pulling or syncing from another design repo:

- Treat the current page as the base.
- Apply:
  - Visual/layout tweaks
  - Script / animation updates
  - Font / style refinements
- Preserve:
  - CTA button (index.html)
  - SEO / meta
  - Accessibility attributes
- If there’s a conflict between “the new design HTML” and existing page:
  - Don’t auto-pick one.
  - Highlight the difference and ask for a decision.

## 4. Version control (git) rules

- Use git for all changes:
  - Commit every meaningful edit.
  - Use short, clear messages (e.g. “Home: adjust vortex hover behaviour”).
- Prefer small, focused commits:
  - One logical change per commit.
- Don’t push large, ambiguous overwrites of any page without a clear explanation
  in the commit message (why, what is preserved, what is removed).

## 5. For AI agents / automation

- If AGENTS.md exists, follow it.
- If a task says “use this HTML as the new page”:
  - Diff it against the current version.
  - Keep CTA, SEO, and core configs unless explicitly told to drop them.

## 6. Dev/Production workflow

Two repos under the ACE-WERK GitHub org:

| Repo | Branch | URL | Purpose |
|---|---|---|---|
| `ACE-WERK/acewerk.com` | `main` | `https://acewerk.com/` | Production |
| `ACE-WERK/acewerk-dev` | `main` | `https://dev.acewerk.com/` | Staging |

Rules:
- **New features go to `ACE-WERK/acewerk-dev` first** (deploys to `dev.acewerk.com`).
- QA validates on `dev.acewerk.com` before any prod merge.
- On merge to prod: remove `noindex` meta tags and `robots.txt` Disallow so prod pages are searchable.
- Never push feature work directly to `ACE-WERK/acewerk.com` without dev staging.
- Internal links: relative paths only (`href="/"`) — works on both environments.
- Git push: `git -c credential.helper="/usr/bin/gh auth git-credential" push`

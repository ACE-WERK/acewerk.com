# Ace Werk Blog — Content Guide

The blog is a static site generated from Markdown source files. There is no CMS
and no runtime framework: a Python build script turns the Markdown in this
directory into plain HTML pages.

## Directory layout

```
content/
  posts/             <- one Markdown file per post (this is where you write)
  README.md          <- this file
scripts/
  build_blog.py      <- the static generator (Python 3 stdlib only)
blog/                <- GENERATED output (do not edit by hand)
  index.html
  <slug>/index.html
  search-index.json
```

`blog/` is generated. Never edit files in `blog/` directly — they are
overwritten by the next build.

## Adding a post

1. Create a new file `content/posts/<slug>.md` where `<slug>` is the URL-safe
   identifier for the post (lowercase letters, digits, and hyphens only).
2. Give it front matter (see below).
3. Write the post body in Markdown (see "Supported Markdown").
4. Rebuild the site from the repo root:

   ```bash
   python scripts/build_blog.py
   ```

That is the entire workflow. A new post needs **only** a new source file; the
build produces its page at `blog/<slug>/index.html`, adds it to the index, and
includes it in the search index automatically.

## Front matter

Front matter is a YAML-style block at the very top of the file, delimited by
`---` lines. Supported fields:

```markdown
---
title: "Post Title"
slug: my-post-slug
date: 2026-09-05          # ISO 8601 (YYYY-MM-DD)
author: "Author Name"
excerpt: "One or two sentences shown on the card and used by search."
tags: "design, engineering"   # optional, comma-separated
fixture: true                 # optional — marks a post as a staging fixture
---

Post body starts here…
```

| Field    | Required | Notes                                                        |
|----------|----------|--------------------------------------------------------------|
| `title`  | yes      | The post title (and page `<title>`).                         |
| `slug`   | yes      | URL-safe id; must match the filename.                        |
| `date`   | yes      | ISO 8601 `YYYY-MM-DD`. Posts sort newest-first by this value.|
| `author` | yes      | Displayed on the card and the post page.                     |
| `excerpt`| yes      | Shown on the card; auto-truncated to 200 chars.              |
| `tags`   | no       | Comma-separated; up to 3 shown on a card (+`N` for the rest).|
| `fixture`| no       | `true` marks a post as a dev-environment fixture (adds a     |
|          |          | visible "Fixture" badge and a note on the post page).        |

Dates sort reverse-chronologically (newest first). If two posts share a date,
the tie is broken by slug (descending).

## Supported Markdown

The build step parses a bounded subset of Markdown (Python stdlib only — no
external parser). Supported block elements:

- ATX headings `## `, `### `, `#### ` (h2/h3/h4). The post `h1` comes from the
  `title` front matter field, so start your body at `##`.
- Paragraphs (consecutive lines are joined).
- Unordered lists (`- `, `* `, `+ `) and ordered lists (`1. `), with nesting
  via indentation.
- Blockquotes (`> `).
- Fenced code blocks (```` ```lang ```` or `~~~`).

Supported inline elements:

- Inline code `` `code` ``.
- Links `[label](url)` (also `[label](<url with spaces>)`).
- Strong `**text**` / `__text__` and emphasis `*text*` / `_text_`.

Anything outside this subset is rendered as plain text. HTML is escaped, so
raw HTML is not passed through.

## Search index

`blog/search-index.json` is generated at build time and contains one entry per
post (`title`, `excerpt`, `author`, `date`, `slug`, and `body` text stripped of
markup). Search matches when **every** whitespace-separated token in the query
(minimum 2 characters) is a substring of at least one of those fields.

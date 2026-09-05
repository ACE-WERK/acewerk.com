---
title: "A Field Guide to the Markdown We Support"
slug: dev-fixture-long
date: 2026-08-18
author: "The Editorial Team"
excerpt: "Headings, lists, blockquotes, inline links, and fenced code — a long-form sample that exercises every block and inline rule the build step understands."
tags: "docs, markdown, engineering"
fixture: true
---

## Introduction

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum id ligula porta felis euismod semper. This paragraph demonstrates **strong** and *emphasis*, plus an inline link to [the Ace Werk studio](https://acewerk.com/) and a `code` span.

### What we render

Cras mattis consectetur purus sit amet fermentum. The build step understands a bounded subset of Markdown, which is enough for real writing without pulling in a parser dependency.

#### Block elements

Donec sed odio dui. The supported block elements are:

- Unordered list item one
- Unordered list item two
  - Nested item two-a
  - Nested item two-b with `inline code`
- Unordered list item three

1. Ordered list item one
2. Ordered list item two
  1. Nested ordered item two-a
  2. Nested ordered item two-b
3. Ordered list item three

### Quotes and code

> Maecenas faucibus mollis interdum. Sed posuere consectetur est at lobortis. Read more in [our services](https://acewerk.com/services/) — the link works inside a blockquote.

```python
def greet(name):
    # a fenced code block
    return f"Hello, {name}"

print(greet("Ace Werk"))
```

## Closing notes

Nullam quis risus eget urna mollis ornare vel eu leo. Aenean lacinia bibendum nulla sed consectetur.

*Developer fixture — a long sample post for staging QA. Not published content.*

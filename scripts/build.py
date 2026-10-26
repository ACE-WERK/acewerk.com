#!/usr/bin/env python3
"""
Ace Werk build orchestrator (env-aware, with guards).

Usage:
    # Production (used by CI)
    ACEWERK_ENV=prod python scripts/build.py

    # Development / staging
    ACEWERK_ENV=dev python scripts/build.py --keep-fixtures

This script:
- Runs generate_sitemap.py
- Runs build_blog.py (prod: indexable, prod analytics, no fixtures)
- Enforces environment-specific invariants so blog / meta / sitemap / analytics
  cannot leak between prod and dev.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = (os.getenv("ACEWERK_ENV") or "prod").strip().lower()
KEEP_FIXTURES = "--keep-fixtures" in sys.argv[1:]

if ENV not in ("prod", "dev"):
    print(
        f"ERROR: ACEWERK_ENV={ENV!r} is invalid. Use 'prod' or 'dev'.",
        file=sys.stderr,
    )
    sys.exit(1)

# ── Helpers ──

def run(cmd, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL:", " ".join(cmd), file=sys.stderr)
        if r.stdout:
            print(r.stdout, file=sys.stderr)
        if r.stderr:
            print(r.stderr, file=sys.stderr)
        sys.exit(r.returncode)
    # Allow stdout to show in CI logs (useful for sitemap, blog build)
    if r.stdout:
        print(r.stdout, end="")
    if r.stderr:
        # Keep build info visible
        print(r.stderr, file=sys.stderr, end="")

def file_contains(path: Path, needle: str) -> bool:
    if not path.is_file():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")

def read_htmls(patterns):
    """Read HTML files matching any given patterns (relative to ROOT)."""
    files = []
    for root_dir, _, filenames in os.walk(ROOT):
        for fn in filenames:
            if fn.lower().endswith(".html"):
                rel = Path(root_dir, fn).relative_to(ROOT)
                if any(pat in str(rel) for pat in patterns):
                    files.append(rel)
    return files

# ── 1. Generate sitemap (both envs, but guards differ) ──

def build_sitemap():
    run(["python", "scripts/generate_sitemap.py"])

# ── 2. Blog build (ACEWERK_ENV is inherited; prod mode drops noindex and fixtures) ──

def build_blog():
    run(["python", "scripts/build_blog.py"] + (["--keep-fixtures"] if KEEP_FIXTURES else []))

# ── 3. Prods-only guards ──

def guard_prod():
    if ENV != "prod":
        return

    sitemap = ROOT / "sitemap.xml"
    errors = []

    # - Every blog page belongs to a published (non-fixture) post.
    blog_dir = ROOT / "blog"
    posts_dir = ROOT / "content" / "posts"
    blog_pages = sorted(blog_dir.glob("*/index.html")) if blog_dir.is_dir() else []
    for page in blog_pages:
        slug = page.parent.name
        src = posts_dir / f"{slug}.md"
        if not src.is_file():
            errors.append(f"blog/{slug}/ has no source post content/posts/{slug}.md.")
        elif re.search(r"^fixture:\s*(true|1|yes)\s*$", src.read_text(encoding="utf-8"), re.M | re.I):
            errors.append(f"blog/{slug}/ is a fixture and must not ship to production.")

    # - Blog pages are indexable, load prod analytics, carry no fixture text.
    prod_analytics_id = "15435e6c-c2e0-4995-bd8e-db662d4474f3"
    for page in ([blog_dir / "index.html"] if blog_dir.is_dir() else []) + blog_pages:
        rel = page.relative_to(ROOT)
        text = page.read_text(encoding="utf-8", errors="ignore")
        if "noindex" in text.lower():
            errors.append(f"Production page {rel} must not contain 'noindex'.")
        if prod_analytics_id not in text:
            errors.append(f"Production page {rel} must load the production analytics ID.")
        for phrase in ("dev-fixture", "developer fixtures", "sample post for staging qa"):
            if phrase in text.lower():
                errors.append(f"Production file {rel} must not contain fixture text: {phrase!r}")
                break

    # - Sitemap must not contain github.io or dev.acewerk.com
    if sitemap.is_file():
        text = sitemap.read_text(encoding="utf-8", errors="ignore")
        if "github.io" in text:
            errors.append(
                "Production sitemap must not contain 'github.io' hostname."
            )
        if "dev.acewerk.com" in text:
            errors.append(
                "Production sitemap must not contain 'dev.acewerk.com'."
            )
        # Check that all loc values use acewerk.com only
        locs = re.findall(r"<loc>(.*?)</loc>", text)
        for loc in locs:
            if not loc.startswith("https://acewerk.com"):
                errors.append(
                    f"Production sitemap contains disallowed URL: {loc}"
                )

    # - No noindex on main production pages
    main_pages = ["index.html", "services/index.html", "our-team/index.html", "contact/index.html"]
    for rel in main_pages:
        path = ROOT / rel
        if path.is_file():
            content = path.read_text(encoding="utf-8", errors="ignore")
            if "noindex" in content.lower():
                errors.append(
                    f"Production page {rel} must not contain 'noindex'."
                )

    # - No fixture titles in production HTML
    fixture_phrases = [
        "Fixture",
        "fixture-post",
        "dev-fixture",
        "developer fixtures",
    ]
    for rel in main_pages:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in fixture_phrases:
            if phrase.lower() in text.lower():
                errors.append(
                    f"Production file {rel} must not contain fixture text: {phrase!r}"
                )
                break

    if errors:
        for e in errors:
            print(f"FAIL (prod): {e}", file=sys.stderr)
        raise RuntimeError("Prod build guards failed.")
    else:
        print("Prod build guards: PASSED")

# ── 4. Dev-only guards ──

def guard_dev():
    if ENV != "dev":
        return

    errors = []

    blog_dir = ROOT / "blog"
    # - /blog/ must exist
    if not (blog_dir.exists() and blog_dir.is_dir()):
        errors.append("Dev build must include /blog/ directory.")

    # - Every HTML page must contain noindex
    all_html = read_htmls(["services/", "our-team/", "contact/", "index.html", "blog/"])
    for rel in all_html:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "noindex" not in text.lower():
            errors.append(
                f"Dev page {rel} must contain 'noindex, nofollow, noarchive'."
            )

    # - No dev page uses the prod analytics ID
    prod_analytics_id = "15435e6c-c2e0-4995-bd8e-db662d4474f3"
    for rel in all_html:
        path = ROOT / rel
        if not path.is_file():
            continue
        if file_contains(path, prod_analytics_id):
            errors.append(
                f"Dev page {rel} must not load the production analytics ID."
            )

    # - robots.txt must not reference a sitemap
    robots = ROOT / "robots.txt"
    if robots.is_file():
        text = robots.read_text(encoding="utf-8", errors="ignore")
        if "sitemap" in text.lower():
            errors.append(
                "Dev robots.txt must not reference a sitemap."
            )

    # - Blog posts that are dev-only must NOT canonicalize to acewerk.com/blog/
    for root_dir, _, filenames in os.walk(blog_dir):
        for fn in filenames:
            if fn.lower() == "index.html":
                path = Path(root_dir, fn)
                text = path.read_text(encoding="utf-8", errors="ignore")
                # simple canonical check
                if 'href="https://acewerk.com/blog/' in text or "href='https://acewerk.com/blog/" in text:
                    errors.append(
                        f"Dev-only blog page {path.relative_to(ROOT)} "
                        "must not canonicalize to acewerk.com/blog/."
                    )

    if errors:
        for e in errors:
            print(f"FAIL (dev): {e}", file=sys.stderr)
        raise RuntimeError("Dev build guards failed.")
    else:
        print("Dev build guards: PASSED")

# ── Main ──

def main():
    print(f"Building for ACEWERK_ENV={ENV}")

    # Sitemap
    build_sitemap()

    # Blog: only for dev
    build_blog()

    # Guards
    if ENV == "prod":
        guard_prod()
    elif ENV == "dev":
        guard_dev()

    print("Build completed successfully.")

if __name__ == "__main__":
    main()

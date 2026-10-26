#!/usr/bin/env python3
"""
test_env_separation.py

Automated assertions for prod / dev separation.

Run:
    - Production (example):
        ACEWERK_ENV=prod python -m pytest tests/test_env_separation.py
    - Development:
        ACEWERK_ENV=dev python -m pytest tests/test_env_separation.py
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = (os.getenv("ACEWERK_ENV") or "prod").strip().lower()

PROD_ANALYTICS_ID = "15435e6c-c2e0-4995-bd8e-db662d4474f3"

# ── Helpers ──

def html_files():
    out = []
    for p in ROOT.rglob("*.html"):
        out.append(p.relative_to(ROOT))
    return out

def file_text(rel):
    p = ROOT / rel
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="ignore")
    return ""

# ── PROD TESTS ──

def test_prod_blog_only_published_posts():
    if ENV != "prod":
        return
    for p in (ROOT / "blog").glob("*/index.html"):
        slug = p.parent.name
        src = ROOT / "content" / "posts" / f"{slug}.md"
        assert src.is_file(), f"blog/{slug}/ has no source post."
        assert not re.search(r"^fixture:\s*(true|1|yes)\s*$", src.read_text(encoding="utf-8"), re.M | re.I), (
            f"blog/{slug}/ is a fixture and must not ship to production."
        )

def test_prod_blog_pages_indexable_with_analytics():
    if ENV != "prod":
        return
    for p in (ROOT / "blog").rglob("index.html"):
        t = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(ROOT)
        assert "noindex" not in t.lower(), f"Production {rel} must not contain 'noindex'."
        assert PROD_ANALYTICS_ID in t, f"Production {rel} must load the production analytics ID."
        assert "dev-fixture" not in t, f"Production {rel} must not reference dev fixtures."

def test_prod_sitemap_hostname():
    if ENV != "prod":
        return
    sitemap = ROOT / "sitemap.xml"
    assert sitemap.is_file(), "Production must have sitemap.xml"

    tree = ET.parse(str(sitemap))
    root = tree.getroot()
    ns = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for url in root.findall(".//sitemap:url/sitemap:loc", ns):
        loc = (url.text or "").strip()
        assert loc.startswith("https://acewerk.com"), (
            f"Production sitemap must use https://acewerk.com, got: {loc}"
        )
        assert "github.io" not in loc, (
            "Production sitemap must not include github.io."
        )
        assert "dev.acewerk.com" not in loc, (
            "Production sitemap must not include dev.acewerk.com."
        )

def test_prod_no_noindex_on_main_pages():
    if ENV != "prod":
        return
    main = ["index.html", "services/index.html", "our-team/index.html", "contact/index.html"]
    for rel in main:
        t = file_text(rel).lower()
        assert "noindex" not in t, (
            f"Production {rel} must not contain 'noindex'."
        )

def test_prod_no_fixture_text_in_main_pages():
    if ENV != "prod":
        return
    phrases = ["fixture", "dev-fixture", "developer fixtures"]
    main = ["index.html", "services/index.html", "our-team/index.html", "contact/index.html"]
    for rel in main:
        t = file_text(rel).lower()
        for phrase in phrases:
            assert phrase not in t, (
                f"Production {rel} must not contain fixture text: {phrase!r}"
            )

# ── DEV TESTS ──

def test_dev_blog_exists():
    if ENV != "dev":
        return
    blog = ROOT / "blog"
    assert blog.exists() and blog.is_dir(), (
        "Development build must include /blog/ directory."
    )

def test_dev_pages_have_noindex():
    if ENV != "dev":
        return
    for rel in html_files():
        t = file_text(rel).lower()
        assert "noindex" in t, (
            f"Dev HTML {rel} must contain 'noindex, nofollow, noarchive'."
        )

def test_dev_no_prod_analytics_id():
    if ENV != "dev":
        return
    for rel in html_files():
        t = file_text(rel)
        assert PROD_ANALYTICS_ID not in t, (
            f"Dev page {rel} must not load the production analytics ID."
        )

def test_dev_robots_no_sitemap():
    if ENV != "dev":
        return
    robots = ROOT / "robots.txt"
    if robots.is_file():
        t = robots.read_text(encoding="utf-8", errors="ignore")
        assert "sitemap" not in t.lower(), (
            "Dev robots.txt must not reference a sitemap."
        )

def test_dev_blog_no_production_canonical():
    if ENV != "dev":
        return
    blog = ROOT / "blog"
    if not (blog.exists() and blog.is_dir()):
        return
    for p in blog.rglob("index.html"):
        t = p.read_text(encoding="utf-8", errors="ignore")
        assert 'href="https://acewerk.com/blog/' not in t, (
            f"Dev-only blog page {p.relative_to(ROOT)} "
            "must not canonicalize to acewerk.com/blog/."
        )

#!/usr/bin/env python3
"""
Copy only the public site into _site/ for GitHub Pages.

Usage (CI, after the build step):
    python scripts/assemble_site.py

Everything else in the repo (docs, specs, scripts, tests, drafts) stays out of
the published site. A new public page or folder must be added to PUBLIC below;
the link check fails the build if a published page points at a file that was
left out.
"""

import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

# Top-level files and folders that make up the public site. Missing ones are skipped.
PUBLIC = [
    "index.html", "404.html", "CNAME", "robots.txt", "sitemap.xml",
    "favicon.ico", "apple-touch-icon.png",
    "assets", "blog", "contact", "our-team", "services", "js", "data",
]
# Never published, even inside a public folder.
DROP = re.compile(r"(\.bak|\.md|\.py|\.pyc|\.mjs|\.sh|~)$|(^|/)(__pycache__|\.DS_Store)")

LINK = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\)""")


def assemble():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name in PUBLIC:
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, OUT / name)
        elif src.is_file():
            shutil.copy2(src, OUT / name)
    for p in sorted(OUT.rglob("*"), reverse=True):
        if DROP.search(p.relative_to(OUT).as_posix()):
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    (OUT / ".nojekyll").touch()


def resolve(page, ref):
    u = urlparse(ref)
    if u.scheme or u.netloc or ref.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    path = unquote(u.path)
    if not path:
        return None
    target = (OUT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    return target / "index.html" if path.endswith("/") else target


def check_links():
    missing = []
    for page in sorted(list(OUT.rglob("*.html")) + list(OUT.rglob("*.css"))):
        text = page.read_text(encoding="utf-8", errors="ignore")
        for m in LINK.finditer(text):
            ref = (m.group(1) or m.group(2)).strip()
            if "${" in ref or "{{" in ref:
                continue  # template placeholder inside inline JS
            target = resolve(page, ref)
            if target is None:
                continue
            if not (target.exists() or target.with_suffix(".html").exists() or (target / "index.html").exists()):
                missing.append(f"{page.relative_to(OUT)} -> {ref}")
    return missing


def main():
    assemble()
    files = [p for p in OUT.rglob("*") if p.is_file()]
    print(f"_site: {len(files)} files from {', '.join(n for n in PUBLIC if (ROOT / n).exists())}")
    missing = check_links()
    if missing:
        for m in missing:
            print(f"FAIL: published page links to an unpublished or missing file: {m}", file=sys.stderr)
        print("Add the folder/file to PUBLIC in scripts/assemble_site.py, or fix the link.", file=sys.stderr)
        return 1
    print("Link check: every local link resolves inside _site")
    return 0


if __name__ == "__main__":
    sys.exit(main())

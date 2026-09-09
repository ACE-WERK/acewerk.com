#!/usr/bin/env python3
"""
Generate a Sitemap Protocol 0.9 compliant sitemap.xml at the repo root.

Extensibility — adding a new page is a single-entry edit:
    1. Add a dict to the PAGES list: {"path": "/blog/", "source": "blog/index.html"}
    2. That's it. The script auto-derives <lastmod> from git history.

Requirements:
    - Python 3.9+
    - Git (to derive lastmod from commit dates)

Behaviour:
    - On success: writes sitemap.xml, exits 0.
    - On failure: prints error to stderr, removes any stale sitemap.xml, exits non-zero.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — edit this list to add / remove pages.
# ---------------------------------------------------------------------------
BASE_URL: str = "https://acewerk.com"
OUTPUT: str = "sitemap.xml"

PAGES: list[dict[str, str]] = [
    {"path": "/",           "source": "index.html"},
    {"path": "/services/",  "source": "services/index.html"},
    {"path": "/our-team/",  "source": "our-team/index.html"},
    {"path": "/contact/",   "source": "contact/index.html"},
]

# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

# Matches ISO 8601 dates like 2026-07-10T18:15:57+02:00 or 2026-07-10T18:15:57Z
_ISO_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$"
)


def _validate_base_url(base_url: str) -> None:
    """Reject non-HTTPS URLs early — misconfiguration guard."""
    if not base_url.startswith("https://"):
        raise ValueError(
            f"BASE_URL must use https:// (got: {base_url}). "
            "Non-HTTPS base URLs are rejected as misconfiguration."
        )


def _check_duplicate_paths(pages: list[dict[str, str]]) -> None:
    """Fail fast when two entries share the same public path."""
    seen: set[str] = set()
    for entry in pages:
        p = entry["path"]
        if p in seen:
            raise ValueError(
                f"Duplicate page path detected: '{p}'. "
                "Each path must appear exactly once in PAGES."
            )
        seen.add(p)


def _validate_iso8601(ts: str, context: str) -> str:
    """Return the timestamp if it's valid ISO 8601; raise otherwise."""
    ts = ts.strip()
    if not ts:
        raise ValueError(
            f"Git returned an empty lastmod for {context}. "
            "This likely means the source file has no commit history."
        )
    if not _ISO_RE.match(ts):
        raise ValueError(
            f"Git returned a non-ISO 8601 timestamp for {context}: '{ts}'. "
            "Expected output from: git log -1 --format=%aI -- <file>"
        )
    # Verify Python can parse it, too
    try:
        datetime.fromisoformat(ts)
    except ValueError as exc:
        raise ValueError(
            f"Timestamp '{ts}' for {context} looks like ISO 8601 but "
            f"could not be parsed: {exc}"
        ) from exc
    return ts


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def get_lastmod(repo_root: Path, source_file: str) -> str:
    """
    Return the ISO 8601 last-modified timestamp from the most recent
    commit that touched *source_file*.

    Uses:  git log -1 --format=%aI -- <source_file>
    """
    result = subprocess.run(
        ["git", "-C", str(repo_root), "log", "-1", "--format=%aI", "--", source_file],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git command failed for '{source_file}': {result.stderr.strip()}"
        )
    return _validate_iso8601(result.stdout, source_file)


def build_sitemap(repo_root: Path) -> ET.ElementTree:
    """Return an ElementTree for a valid sitemap 0.9 urlset."""

    _validate_base_url(BASE_URL)
    _check_duplicate_paths(PAGES)

    urlset = ET.Element(
        "urlset",
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
    )

    for entry in PAGES:
        public_path = entry["path"]
        source_file = entry["source"]

        abs_source = repo_root / source_file
        if not abs_source.is_file():
            raise FileNotFoundError(
                f"Source file for '{public_path}' not found: {abs_source}"
            )

        loc = BASE_URL.rstrip("/") + public_path  # e.g. https://acewerk.com/services/
        lastmod = get_lastmod(repo_root, source_file)

        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = loc
        ET.SubElement(url, "lastmod").text = lastmod

    return ET.ElementTree(urlset)


def write_sitemap(tree: ET.ElementTree, out_path: Path) -> None:
    """Write pretty-printed sitemap.xml."""
    ET.indent(tree, space="  ", level=0)
    tree.write(
        str(out_path),
        xml_declaration=True,
        encoding="UTF-8",
        method="xml",
    )
    print(f"OK: {out_path} written with {len(PAGES)} URLs", file=sys.stderr)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    out_path = repo_root / OUTPUT

    # Always start fresh — remove any previous sitemap so a failed run
    # never leaves a stale file behind.
    try:
        out_path.unlink(missing_ok=True)
    except OSError:
        pass

    try:
        tree = build_sitemap(repo_root)
        write_sitemap(tree, out_path)
    except Exception as exc:
        # On any failure, delete the output file so nothing partial or stale remains.
        try:
            out_path.unlink(missing_ok=True)
        except OSError:
            pass
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Quick edge-case validation for generate_sitemap.py"""
import sys, os, importlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import generate_sitemap
g = generate_sitemap

failed = 0

def test(name, pages=None, base_url=None, should_fail=True):
    global failed
    if pages is not None:
        g.PAGES = pages
    if base_url is not None:
        g.BASE_URL = base_url
    
    try:
        g.build_sitemap(g.Path(g.__file__).resolve().parent.parent)
        if should_fail:
            print(f"FAIL: {name} — should have raised, didn't")
            failed += 1
        else:
            print(f"PASS: {name}")
    except SystemExit:
        if should_fail:
            print(f"PASS: {name}")
        else:
            print(f"FAIL: {name} — should have succeeded")
            failed += 1
    except Exception as e:
        if should_fail:
            print(f"PASS: {name} — {e}")
        else:
            print(f"FAIL: {name} — {e}")
            failed += 1

# Reset to defaults before each test by reloading

def reload_mod():
    global g
    import generate_sitemap
    g = importlib.reload(generate_sitemap)
    # Clean up any leftover sitemap.xml
    out = g.Path(g.__file__).resolve().parent.parent / "sitemap.xml"
    out.unlink(missing_ok=True)

# Test 1: Duplicate page path → must fail
reload_mod()
test("duplicate paths", pages=[
    {"path": "/", "source": "index.html"},
    {"path": "/", "source": "other.html"},
])

# Test 2: Non-HTTPS base URL → must fail
reload_mod()
test("non-HTTPS base URL", base_url="http://acewerk.com", pages=[
    {"path": "/", "source": "index.html"},
])

# Test 3: Missing source file → must fail
reload_mod()
test("missing source file", pages=[
    {"path": "/", "source": "nonexistent.html"},
])

# Test 4: Normal case → must succeed
reload_mod()
test("normal case", should_fail=False, pages=[
    {"path": "/", "source": "index.html"},
])

print(f"\n{failed} test(s) failed" if failed else "\nAll edge-case tests passed.")
sys.exit(0 if failed == 0 else 1)

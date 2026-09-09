#!/usr/bin/env python3
"""ACE-26 QA: verify diamond removal on dev.acewerk.com/blog/ at 3 viewports.
Chromium via CDP. DOM-only (pure-CSS delta).
"""
import json, time, sys
from playwright.sync_api import sync_playwright

URL = "https://dev.acewerk.com/blog/"
VIEWPORTS = [(1440, 900, "desktop"), (768, 1024, "tablet"), (390, 844, "mobile")]

JS = r"""
() => {
  const out = {glyphSpans: [], cardCount: 0, firstChilds: [], padding: [], gap: [], consoleErrors: []};
  out.glyphSpans = document.querySelectorAll('.post-card-glyph').length;
  const cards = Array.from(document.querySelectorAll('.post-card'));
  out.cardCount = cards.length;
  out.firstChilds = cards.slice(0, 5).map(c => {
    const fc = c.firstElementChild;
    return fc ? (fc.className || fc.tagName) : null;
  });
  const c0 = cards[0];
  if (c0) {
    const cs = getComputedStyle(c0);
    out.padding = [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft];
    out.gap = cs.gap;
    // first-child top offset relative to card
    const fc = c0.firstElementChild;
    const cr = c0.getBoundingClientRect();
    const fr = fc.getBoundingClientRect();
    out.firstChildTopOffset = (fr.top - cr.top);
  }
  // check for orphaned .post-card-glyph rule in any <style>
  let orphanRule = false;
  for (const s of document.querySelectorAll('style')) {
    if (s.textContent.includes('.post-card-glyph')) orphanRule = true;
  }
  out.orphanGlyphRule = orphanRule;
  // article tag balance
  const open = document.querySelectorAll('article').length;
  out.articleCount = open;
  // border/radius/bg of card (to compare unchanged)
  if (c0) {
    const cs = getComputedStyle(c0);
    out.border = cs.borderTopWidth + ' ' + cs.borderTopStyle + ' ' + cs.borderTopColor;
    out.borderRadius = cs.borderTopLeftRadius;
    out.hasBackdrop = (cs.backdropFilter && cs.backdropFilter !== 'none');
  }
  return out;
}
"""

def main():
    results = {}
    console_errors_all = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.new_context()
        page = ctx.new_page()
        page.on("console", lambda m: console_errors_all.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors_all.append(str(e)))
        ts = int(time.time())
        for w, h, name in VIEWPORTS:
            page.set_viewport_size({"width": w, "height": h})
            page.goto(URL + "?t=" + str(ts), wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1500)
            data = page.evaluate(JS)
            results[name] = data
        # single-post page check (regression guard): .post-title/.post-byline intact
        sp = page
        sp.set_viewport_size({"width": 1440, "height": 900})
        # find a post link
        href = sp.evaluate("() => { const a = document.querySelector('.post-card-link'); return a ? a.getAttribute('href') : null; }")
        sp_post = {"href": href, "postTitle": None, "postByline": None, "hasGlyph": None}
        if href:
            sp.goto("https://dev.acewerk.com" + href + "?t=" + str(ts), wait_until="domcontentloaded", timeout=60000)
            sp.wait_for_timeout(600)
            sp_post["postTitle"] = sp.evaluate("() => { const e = document.querySelector('.post-title'); return e ? e.textContent.trim().slice(0,60) : null; }")
            sp_post["postByline"] = sp.evaluate("() => { const e = document.querySelector('.post-byline'); return e ? 'present' : 'MISSING'; }")
            sp_post["hasGlyph"] = sp.evaluate("() => document.querySelectorAll('.post-card-glyph').length")
        results["single_post"] = sp_post
    results["console_errors"] = console_errors_all
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

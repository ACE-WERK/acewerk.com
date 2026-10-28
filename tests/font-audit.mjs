import http from 'http';
import fs from 'fs';
import path from 'path';

const BASE = 'http://localhost:8090';
const PAGES = ['/', '/contact/', '/our-team/', '/services/'];

function fetchText(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let data = '';
      if (res.statusCode >= 400) return reject(new Error(`${url} HTTP ${res.statusCode}`));
      res.on('data', chunk => (data += chunk.toString()));
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function extractUrls(html) {
  const urls = [];
  const patterns = [
    /<link[^>]+href=["']([^"']+)["']/gi,
    /<script[^>]+src=["']([^"']+)["']/gi,
    /url\(["']?([^)"']+)["']?\)/gi,
  ];
  for (const p of patterns) {
    for (const m of html.matchAll(p)) {
      let u = m[1];
      if (!u.startsWith('http') && u.startsWith('/')) u = BASE + u;
      urls.push(u);
    }
  }
  return urls.filter(Boolean);
}

async function auditPage(pagePath) {
  const url = BASE + pagePath;
  const r = { page: pagePath, ok: true, issues: [] };

  try {
    const html = await fetchText(url);

    // 1. No Google Fonts references
    for (const g of ['fonts.googleapis.com', 'fonts.gstatic.com']) {
      if (html.includes(g)) {
        r.ok = false;
        r.issues.push(`[FAIL] Found reference to ${g} in HTML`);
      }
    }

    // 2. No external font URLs in links/scripts/url()
    const urls = extractUrls(html);
    for (const u of urls) {
      if (u.includes('fonts.googleapis.com') || u.includes('fonts.gstatic.com')) {
        r.ok = false;
        r.issues.push(`[FAIL] External font URL: ${u}`);
      }
    }

    // 3. Confirm /assets/fonts/ + .woff2
    const fontRefs = (html.match(/\/assets\/fonts\/[^"'()\s]+/g) || []);
    const woff2Refs = fontRefs.filter(f => f.endsWith('.woff2'));
    if (fontRefs.length === 0) {
      r.ok = false;
      r.issues.push('[FAIL] No /assets/fonts/ references');
    } else if (woff2Refs.length === 0) {
      r.ok = false;
      r.issues.push('[FAIL] No .woff2 font files referenced');
    } else {
      r.fontRefs = fontRefs;
      r.woff2Refs = woff2Refs;
    }

    // 4. font-family with fallbacks
    const fontFamilies = (html.match(/font-family:\s*[^;]+/gi) || []);
    const missingFallback = fontFamilies.map(f => f.trim()).filter(ff => {
      return !ff.includes('sans-serif')
          && !ff.includes('serif')
          && !ff.includes('monospace')
          && !ff.includes('system-ui');
    });
    if (missingFallback.length > 0) {
      r.issues.push(
        `[WARN] font-family without generic fallback: ${missingFallback.join(', ')}`
      );
    }

    return r;
  } catch (err) {
    r.ok = false;
    r.issues.push(`[FAIL] Failed to load ${url}: ${err.message}`);
    return r;
  }
}

async function auditFontsCss() {
  const cssPath = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../assets/fonts/fonts.css');
  const css = fs.readFileSync(cssPath, 'utf8');
  const r = { page: 'assets/fonts/fonts.css', ok: true, issues: [] };

  const blocks = (css.match(/@font-face\s*{[^}]+}/g) || []);
  for (const block of blocks) {
    if (!block.includes('font-display: swap')) {
      r.ok = false;
      r.issues.push('[FAIL] @font-face missing font-display: swap');
    }
    if (!block.includes('.woff2')) {
      r.ok = false;
      r.issues.push('[FAIL] @font-face not using .woff2');
    }
  }

  const requiredFamilies = ['Orbitron', 'Space Grotesk', 'Rajdhani', 'JetBrains Mono', 'Inter'];
  for (const family of requiredFamilies) {
    if (!css.includes(`'${family}'`)) {
      r.ok = false;
      r.issues.push(`[FAIL] Missing @font-face for required family: ${family}`);
    }
  }

  return r;
}

async function main() {
  const allResults = [];

  for (const page of PAGES) {
    allResults.push(await auditPage(page));
  }

  allResults.push(await auditFontsCss());

  let anyFail = false;
  console.log('\n=== FONT SELF-HOSTING AUDIT ===\n');

  for (const r of allResults) {
    console.log(`Page: ${r.page}`);
    console.log(`  Status: ${r.ok ? 'PASS' : 'FAIL'}`);
    if (r.issues?.length) {
      for (const issue of r.issues) console.log(`  - ${issue}`);
    }
    if (r.fontRefs) {
      console.log(`  Font refs: ${r.fontRefs.join(', ')}`);
      console.log(`  woff2 refs: ${r.woff2Refs.join(', ')}`);
    }
    if (!r.ok) anyFail = true;
    console.log();
  }

  console.log(`Overall: ${anyFail ? 'FAIL' : 'PASS'}`);
  process.exit(anyFail ? 1 : 0);
}

main();

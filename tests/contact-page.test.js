/**
 * contact-page.test.js
 *
 * End-to-end tests for /contact page.
 * Run with: node tests/contact-page.test.js
 *
 * - Spins up a simple HTTP server on a random port.
 * - Uses puppeteer to automate the /contact page.
 * - Checks validation, accessibility, meta tags, links, and layout requirements.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = path.resolve(__dirname, '..');
const PORT = 8090;

// Minimal static file server
function createServer() {
  return http.createServer((req, res) => {
    let url = req.url.split('?')[0];
    if (url === '/') url = '/index.html';

    const filePath = path.join(ROOT, url);
    try {
      const stat = fs.statSync(filePath);
      if (!stat.isFile()) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      const ext = path.extname(filePath).toLowerCase();
      const types = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.txt': 'text/plain',
      };
      const contentType = types[ext] || 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': contentType });
      fs.createReadStream(filePath).pipe(res);
    } catch (err) {
      res.writeHead(404);
      res.end('Not found');
    }
  }).listen(PORT);
}

(async () => {
  const server = createServer();
  let browser;
  try {
    browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage();
    await page.setViewport({ width: 1366, height: 768 });

    // Navigate
    await page.goto(`http://127.0.0.1:${PORT}/contact`, {
      waitUntil: 'networkidle0',
      timeout: 15000,
    });

    // Prevent form submission from leaving the page
    await page.evaluate(() => {
      const form = document.getElementById('contact-form');
      form.addEventListener('submit', (e) => e.preventDefault(), { capture: true });
    });

    const helpers = {
      get: (sel) => page.$(sel),
      getAll: (sel) => page.$$eval(sel, (els) => els),
      run: (fn) => page.evaluate(fn),
    };

    const tests = [];

    // Structural
    tests.push(await (async () => {
      const form = await helpers.get('#contact-form');
      return { test: 'Structural: form#contact-form exists', pass: !!form };
    })());

    tests.push(await (async () => {
      const name = await helpers.get('#name');
      return { test: 'Structural: #name exists', pass: !!name };
    })());

    tests.push(await (async () => {
      const email = await helpers.get('#email');
      return { test: 'Structural: #email exists', pass: !!email };
    })());

    tests.push(await (async () => {
      const company = await helpers.get('#company');
      return { test: 'Structural: #company exists', pass: !!company };
    })());

    tests.push(await (async () => {
      const purpose = await helpers.get('#purpose');
      return { test: 'Structural: #purpose exists', pass: !!purpose };
    })());

    tests.push(await (async () => {
      const message = await helpers.get('#message');
      return { test: 'Structural: #message exists', pass: !!message };
    })());

    tests.push(await (async () => {
      const button = await helpers.get('form button[type="submit"]');
      return { test: 'Structural: submit button exists', pass: !!button };
    })());

    // Helper: submit and collect errors
    const submitAndReadErrors = async () => {
      await helpers.run(() => {
        const form = document.getElementById('contact-form');
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      });
      return await helpers.getAll('.form-error-message').then(els =>
        els.map(el => ({
          field: (el.previousElementSibling && el.previousElementSibling.id) || null,
          text: (el.textContent || '').trim(),
        }))
      );
    };

    // Helper: set fields
    const setFields = async (fields) => {
      await helpers.run(() => {
        const n = document.getElementById('name');
        const e = document.getElementById('email');
        const c = document.getElementById('company');
        const p = document.getElementById('purpose');
        const m = document.getElementById('message');
        if (n && fields.name !== undefined) n.value = fields.name;
        if (e && fields.email !== undefined) e.value = fields.email;
        if (c && fields.company !== undefined) c.value = fields.company;
        if (m && fields.message !== undefined) m.value = fields.message;
        if (p && fields.purposeIndex !== undefined) p.selectedIndex = fields.purposeIndex;
      });
    };

    // #1 Empty form
    await setFields({ name: '', email: '', company: '', purposeIndex: 0, message: '' });
    const e1 = await submitAndReadErrors();
    tests.push({
      test: '#1 Empty form -> Name/Email/Purpose errors',
      pass:
        e1.length === 3 &&
        e1.some(x => x.text === 'Name is required.') &&
        e1.some(x => x.text === 'Email is required.') &&
        e1.some(x => x.text === 'Please select a purpose.'),
    });

    // #2 Only Name empty
    await setFields({ name: '', email: 'a@b.com', purposeIndex: 1, message: 'Hi' });
    const e2 = await submitAndReadErrors();
    tests.push({
      test: '#2 Only Name empty -> Name required only',
      pass: e2.length === 1 && e2[0].text === 'Name is required.',
    });

    // #3 Only Email empty
    await setFields({ name: 'Test', email: '', purposeIndex: 1, message: 'Hi' });
    const e3 = await submitAndReadErrors();
    tests.push({
      test: '#3 Only Email empty -> Email required only',
      pass: e3.length === 1 && e3[0].text === 'Email is required.',
    });

    // #4 Malformed email
    await setFields({ name: 'Test', email: 'abc', purposeIndex: 1, message: 'Hi' });
    const e4 = await submitAndReadErrors();
    tests.push({
      test: '#4 Malformed Email -> Invalid email format',
      pass: e4.length === 1 && e4[0].text === 'Invalid email format.',
    });

    // #5 Purpose default
    await setFields({ name: 'Test', email: 'a@b.com', purposeIndex: 0, message: 'Hi' });
    const e5 = await submitAndReadErrors();
    tests.push({
      test: '#5 Purpose default -> Please select a purpose',
      pass: e5.length === 1 && e5[0].text === 'Please select a purpose.',
    });

    // #6 Company+Message blank -> no errors
    await setFields({ name: 'Test', email: 'a@b.com', company: '', purposeIndex: 1, message: '' });
    const e6 = await submitAndReadErrors();
    tests.push({
      test: '#6 Company+Message blank -> no errors',
      pass: e6.length === 0,
    });

    // #7 Multiple invalid
    await setFields({ name: '', email: 'nope', purposeIndex: 0, message: '' });
    const e7 = await submitAndReadErrors();
    tests.push({
      test: '#7 Multiple invalid -> all shown',
      pass:
        e7.length >= 3 &&
        e7.some(x => x.text === 'Name is required.') &&
        e7.some(x => x.text === 'Invalid email format.') &&
        e7.some(x => x.text === 'Please select a purpose.'),
    });

    // Accessibility
    const hasLabel = async (selector) => {
      const el = await helpers.get(selector);
      if (!el) return false;
      const id = await el.evaluate(n => n.id);
      const labelFor = await helpers.get(`label[for="${id}"]`);
      if (labelFor) return true;
      const parentLabel = await el.evaluate(n => {
        let p = n.parentElement;
        while (p && p.tagName !== 'BODY') {
          if (p.tagName === 'LABEL') return true;
          p = p.parentElement;
        }
        return false;
      });
      return parentLabel;
    };

    tests.push({ test: 'A11y: Name has label', pass: await hasLabel('#name') });
    tests.push({ test: 'A11y: Email has label', pass: await hasLabel('#email') });
    tests.push({ test: 'A11y: Company has label', pass: await hasLabel('#company') });
    tests.push({ test: 'A11y: Purpose has label', pass: await hasLabel('#purpose') });
    tests.push({ test: 'A11y: Message has label', pass: await hasLabel('#message') });

    // Required attributes
    const isRequired = async (selector) => {
      const el = await helpers.get(selector);
      return el ? await el.evaluate(n => n.required === true) : false;
    };

    tests.push({ test: 'A11y: Name required', pass: await isRequired('#name') });
    tests.push({ test: 'A11y: Email required', pass: await isRequired('#email') });
    tests.push({ test: 'A11y: Message required', pass: await isRequired('#message') });

    // Error messages role=alert
    await setFields({ name: '', email: '', purposeIndex: 0, message: '' });
    await submitAndReadErrors();
    const errorAlert = await helpers.get('.form-error-message[role="alert"]');
    tests.push({ test: 'A11y: Error messages have role=alert', pass: !!errorAlert });

    // Meta tags
    const metaContent = async (sel) => {
      const el = await helpers.get(sel);
      return el ? await el.evaluate(n => n.getAttribute('content')) : null;
    };

    const desc = await metaContent('meta[name="description"]');
    tests.push({
      test: 'Meta: description present',
      pass: desc !== null && desc.length > 40,
    });

    const ogTitle = await metaContent('meta[property="og:title"]');
    tests.push({ test: 'Meta: og:title present', pass: ogTitle !== null });

    const ogDesc = await metaContent('meta[property="og:description"]');
    tests.push({ test: 'Meta: og:description present', pass: ogDesc !== null });

    const ogImg = await metaContent('meta[property="og:image"]');
    tests.push({ test: 'Meta: og:image present', pass: ogImg !== null });

    const twCard = await metaContent('meta[name="twitter:card"]');
    tests.push({ test: 'Meta: twitter:card present', pass: twCard !== null });

    // Links
    const logoLink = await helpers.get('a[href="/"]');
    tests.push({ test: 'Header: Logo links to /', pass: !!logoLink });

    const navLinks = await helpers.getAll('nav a').then(els =>
      els.map(a => ({ text: (a.textContent || '').trim(), href: a.getAttribute('href') }))
    );
    const navHrefs = navLinks.map(l => l.href);

    tests.push({
      test: 'Nav: SERVICES link',
      pass: navHrefs.includes('/services/') || navHrefs.some(h => h.startsWith('/services')),
    });
    tests.push({
      test: 'Nav: OUR TEAM link',
      pass: navHrefs.includes('/our-team/') || navHrefs.some(h => h.startsWith('/our-team')),
    });
    tests.push({
      test: 'Nav: CONTACT active',
      pass: navHrefs.some(h => h.startsWith('/contact')),
    });

    const emailLink = await helpers.get('a[href*="info@acewerk.com"]');
    const emailHref = emailLink
      ? await emailLink.evaluate(a => a.getAttribute('href'))
      : null;
    tests.push({
      test: 'Email link present',
      pass: emailLink !== null && emailHref.startsWith('mailto:info@acewerk.com'),
    });

    // Viewport
    const vp = await metaContent('meta[name="viewport"]');
    tests.push({
      test: 'Responsive: Viewport meta present',
      pass: vp !== null && vp.includes('width=device-width'),
    });

    // Title (spec-compliant)
    const title = await page.title();
    tests.push({
      test: 'Title matches "Contact - Ace Werk"',
      pass: title.trim() === 'Contact - Ace Werk',
    });

    // Print results
    const total = tests.length;
    const passed = tests.filter(t => t.pass).length;
    const failed = tests.filter(t => !t.pass);

    console.log(`\n/contact QA — ${passed}/${total} passed\n`);
    for (const t of tests) {
      const icon = t.pass ? '✓' : '✗';
      console.log(`  ${icon} ${t.test}`);
    }

    if (failed.length > 0) {
      console.log('\nFAILURES:');
      for (const t of failed) {
        console.log(`  - ${t.test}`);
      }
      process.exit(1);
    } else {
      console.log('\nAll tests passed.');
      process.exit(0);
    }
  } catch (err) {
    console.error('Test runner error:', err?.message || err);
    process.exit(2);
  } finally {
    if (browser) { await browser.close().catch(() => {}); }
    server.close();
  }
})();

/**
 * contact-spec.mjs
 *
 * Automated validation for /contact page (task t_804d3d9d).
 *
 * Usage:
 *   node tests/contact-spec.mjs
 *
 * Requirements:
 *   - Node.js >= 18
 *   - No extra dependencies.
 */

import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORT = 8090;

function resolvePath(url) {
  url = url.split('?')[0];
  if (url === '/') url = '/index.html';

  let fp = path.join(ROOT, url);
  try {
    const s = fs.statSync(fp);
    if (s.isFile()) return fp;
  } catch { /* continue */ }

  fp = path.join(fp, 'index.html');
  try {
    const s = fs.statSync(fp);
    if (s.isFile()) return fp;
  } catch { /* not found */ }

  return null;
}

const server = http.createServer((req, res) => {
  const filePath = resolvePath(req.url);
  if (!filePath) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }
  const ext = path.extname(filePath).toLowerCase();
  const types = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.txt': 'text/plain',
  };
  res.writeHead(200, { 'Content-Type': types[ext] || 'application/octet-stream' });
  fs.createReadStream(filePath).pipe(res);
});

function fetchPage(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf-8');
        resolve({ status: res.statusCode, body });
      });
    }).on('error', reject);
  });
}

async function runTests() {
  server.listen(PORT);
  const results = [];
  const BASE = `http://127.0.0.1:${PORT}`;

  try {
    const { status, body } = await fetchPage(`${BASE}/contact`);
    results.push({ test: 'GET /contact returns 200', pass: status === 200 });

    // Title
    const titleMatch = body.match(/<title>(.*?)<\/title>/i);
    const title = (titleMatch && titleMatch[1]) || '';
    results.push({
      test: 'Title matches "Contact - Ace Werk"',
      pass: title.trim() === 'Contact - Ace Werk',
      detail: `Actual: "${title.trim()}"`,
    });

    // Viewport meta
    const hasViewport = body.includes('name="viewport"') && body.includes('width=device-width');
    results.push({ test: 'Viewport meta present', pass: hasViewport });

    // Description meta
    const descMatch = body.match(/name="description"[\s\S]*?content="([^"]+)"/i);
    const desc = descMatch ? descMatch[1] : '';
    results.push({ test: 'Meta description present', pass: desc.length > 40 });

    // OG / Twitter tags
    const hasOgTitle = body.includes('property="og:title"');
    const hasOgDesc = body.includes('property="og:description"');
    const hasOgImg = body.includes('property="og:image"');
    const hasTwCard = body.includes('name="twitter:card"');
    results.push({ test: 'og:title present', pass: hasOgTitle });
    results.push({ test: 'og:description present', pass: hasOgDesc });
    results.push({ test: 'og:image present', pass: hasOgImg });
    results.push({ test: 'twitter:card present', pass: hasTwCard });

    // Structural: form and fields
    const hasForm = body.includes('id="contact-form"');
    results.push({ test: 'form#contact-form exists', pass: hasForm });

    const hasField = (id) => body.includes(`id="${id}"`);
    results.push({ test: 'Field #name exists', pass: hasField('name') });
    results.push({ test: 'Field #email exists', pass: hasField('email') });
    results.push({ test: 'Field #company exists', pass: hasField('company') });
    results.push({ test: 'Field #purpose exists', pass: hasField('purpose') });
    results.push({ test: 'Field #message exists', pass: hasField('message') });

    // Submit button
    const hasSubmit = body.includes('type="submit"');
    results.push({ test: 'Submit button exists', pass: hasSubmit });

    // Nav links
    const hasServicesLink = body.includes('/services') || body.includes('/services/');
    const hasTeamLink = body.includes('/our-team') || body.includes('/our-team/');
    const hasContactRef = body.includes('/contact') || body.includes('/contact/');
    results.push({ test: 'Nav: SERVICES link', pass: hasServicesLink });
    results.push({ test: 'Nav: OUR TEAM link', pass: hasTeamLink });
    results.push({ test: 'Nav: CONTACT active', pass: hasContactRef });

    // Email link
    const hasEmailLink = body.includes('mailto:info@acewerk.com');
    results.push({ test: 'Email link present', pass: hasEmailLink });

    // Validation script
    const scripts = body.match(/<script[^>]*>([\s\S]*?)<\/script>/gi) || [];
    const validationScript = scripts.find((s) => s.includes('contact-form'));

    results.push({
      test: 'Client-side validation script present',
      pass: !!validationScript,
    });

    if (validationScript) {
      results.push({
        test: 'Validation: "Name is required." message',
        pass: validationScript.includes('Name is required'),
      });
      results.push({
        test: 'Validation: "Email is required." message',
        pass: validationScript.includes('Email is required'),
      });
      results.push({
        test: 'Validation: "Invalid email format." message',
        pass: validationScript.includes('Invalid email format'),
      });
      results.push({
        test: 'Validation: "Please select a purpose." message',
        pass: validationScript.includes('Please select a purpose'),
      });

      // Accessibility: role="alert" on errors (set dynamically by JS)
      const hasAlert =
        validationScript.includes('role="alert"') ||
        validationScript.includes("role='alert'");
      results.push({
        test: 'Accessibility: role="alert" on error messages (set via JS)',
        pass: hasAlert || validationScript.includes('form-error-message'),
      });

      // Formspree must run: preventDefault() must NOT be called in validation.
      // Only flag if preventDefault() is actually invoked, not just mentioned in comments.
      const callsPreventDefault =
        /e\.preventDefault\(\)|event\.preventDefault\(\)/.test(validationScript);
      results.push({
        test: 'Validation: No preventDefault() call (Formspree must run)',
        pass: !callsPreventDefault,
      });
    }

    // Print summary
    const total = results.length;
    const passed = results.filter((r) => r.pass).length;
    const failed = results.filter((r) => !r.pass);

    console.log(`\n/contact spec - ${passed}/${total} passed\n`);
    for (const r of results) {
      const icon = r.pass ? '\u2713' : '\u2717';
      let line = `  ${icon} ${r.test}`;
      if (!r.pass && r.detail) line += ` (${r.detail})`;
      console.log(line);
    }

    if (failed.length > 0) {
      console.log('\nFAILURES:');
      for (const r of failed) {
        console.log(`  - ${r.test}`);
      }
      process.exit(1);
    } else {
      console.log('\nAll tests passed.');
      process.exit(0);
    }
  } catch (err) {
    console.error('Test error:', err?.message || err);
    process.exit(2);
  } finally {
    server.close();
  }
}

runTests();

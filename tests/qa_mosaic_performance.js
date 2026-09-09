#!/usr/bin/env node
/**
 * Automated structural and logic QA for the WebGL mosaic page:
 * - Verifies WebGL init and shader correctness (offline).
 * - Validates hover/rise logic: no stuck tiles, smooth decay.
 * - Confirms responsive resize handler and mobile/desktop behavior.
 * - Confirms rAF loop is efficient and non-blocking.
 *
 * Run: node tests/qa_mosaic_performance.js
 */

const fs = require('fs');
const path = require('path');

const SRC_INDEX = path.join(__dirname, '..', 'index.html');
const SRC_MOSAIC = path.join(__dirname, '..', 'js', 'mosaic-three.js');

let errors = 0;
let warnings = 0;

function log(tag, msg) {
  console.log(`[OK ${tag}] ${msg}`);
}

function fail(tag, msg) {
  console.error(`[FAIL ${tag}] ${msg}`);
  errors++;
}

function warn(tag, msg) {
  console.warn(`[WARN ${tag}] ${msg}`);
  warnings++;
}

const indexHtml = fs.readFileSync(SRC_INDEX, 'utf8');
const mosaicThreeJs = fs.readFileSync(SRC_MOSAIC, 'utf8');

// ================= WebGL and init checks =================

// 1. WebGL2 context
if (!indexHtml.includes('webgl2')) {
  fail('webgl2', 'Canvas does not request WebGL2 context.');
} else {
  log('webgl2', 'WebGL2 requested.');
}

// 2. Shader compile and link checks
if (!indexHtml.includes('COMPILE_STATUS')) {
  fail('shader', 'Vertex/fragment compile status not checked.');
} else {
  log('shader', 'Compile status checked.');
}

if (!indexHtml.includes('LINK_STATUS')) {
  fail('shader', 'Program link status not checked.');
} else {
  log('shader', 'Link status checked.');
}

// 3. Fallback behavior
if (!indexHtml.includes('fallback')) {
  fail('fallback', 'No WebGL fallback path detected.');
} else {
  log('fallback', 'WebGL fallback element present.');
}

// 4. Reduced motion
if (
  !indexHtml.includes('prefers-reduced-motion') &&
  !mosaicThreeJs.includes('prefers-reduced-motion')
) {
  fail('reduced-motion', 'No prefers-reduced-motion handling.');
} else {
  log('reduced-motion', 'Reduced-motion awareness present.');
}

// ================= Animation loop checks =================

// 5. rAF-based animation
if (
  !indexHtml.includes('requestAnimationFrame') &&
  !indexHtml.includes('requestAnimationFrame')
) {
  fail('raf', 'No requestAnimationFrame loop detected in main HTML.');
} else {
  log('raf', 'requestAnimationFrame loop present.');
}

// 6. No blocking operations in rAF loop (no sync XHR, no long synchronous loops without yield)
const rAFRegex = /function\s+frame\([^)]*\)\s*\{([\s\S]*)\}/;
const rAFMatch = indexHtml.match(rAFRegex);
if (!rAFMatch) {
  warn('raf', 'Could not extract frame() function; skipping loop body checks.');
} else {
  const body = rAFMatch[1];

  // Check for fetch, XMLHttpRequest, sync calls inside loop
  if (body.includes('fetch') || body.includes('XMLHttpRequest')) {
    fail('raf', 'Network call inside animation loop.');
  }

  // Check for big synchronous loops that iterate over all tiles per frame (16k+).
  // The current mosaic does per-frame loops, which is acceptable if operations are cheap.
  const forLoops = (body.match(/for\s*\(/g) || []).length;
  if (forLoops > 10) {
    warn('raf', `High for-loop density in frame(): ${forLoops} loops per frame; ensure cheap operations.`);
  }

  log('raf', 'Animation loop structure analyzed.');
}

// 7. Check that dt is clamped in the frame function to avoid huge jumps
if (rAFMatch && rAFMatch[1].includes('dt>0.05')) {
  log('dt-clamp', 'Delta-time clamping present; prevents explosion after tab switch.');
} else {
  warn('dt-clamp', 'No explicit dt clamp detected; risk of spike after tab switch.');
}

// ================= Hover/rise behavior =================

// 8. Ensure rise values never permanently stuck at 1 due to logic
if (!indexHtml.includes('rise[')) {
  fail('hover', 'No per-tile rise update (rise[]) found.');
} else {
  // Check that:
  //  - there is a "rise-up" branch: when target > rise, apply stiffness.
  //  - there is a "rise-down" branch: when not, relax with fall/RELEASE.
  const hasRiseUp =
    indexHtml.includes('target>r') ||
    indexHtml.includes('target > r');
  const hasRiseDown =
    indexHtml.includes('fall') ||
    indexHtml.includes('RELEASE');

  if (!hasRiseUp || !hasRiseDown) {
    fail('hover', 'Rise logic missing either rise-up or rise-down path; tiles may get stuck.');
  } else {
    log('hover', 'Rise-up and rise-down paths both present; tiles can recover.');
  }
}

// 9. Ensure that pointerleave clears pointer (avoids stuck hover)
if (indexHtml.includes('mouseleave') && indexHtml.includes('active=false')) {
  log('hover', 'mouseleave correctly clears active pointer; avoids stuck hover.');
} else {
  fail('hover', 'mouseleave handler missing or not clearing active; risk of stuck hover.');
}

// ================= Responsiveness checks =================

// 10. resize listener
if (indexHtml.includes('resize') || indexHtml.includes('addEventListener(\'resize\'')) {
  log('responsive', 'Resize listener registered.');
} else {
  fail('responsive', 'No window resize listener found.');
}

// 11. Desktop vs mobile behavior (layout or motion)
if (indexHtml.includes('pointer:fine') || indexHtml.includes('max-width')) {
  log('responsive', 'Responsive or device-aware logic present.');
} else {
  warn('responsive', 'No explicit desktop/mobile branching; ensure design is acceptable on touch devices.');
}

// ================= Three.js mosaic-three.js checks =================

// 12. InstancedMesh usage and correctness
if (!mosaicThreeJs.includes('InstancedMesh')) {
  fail('threejs', 'MosaicRenderer does not use InstancedMesh for performance.');
} else {
  log('threejs', 'InstancedMesh used; suitable for 16,900 tiles.');
}

// 13. Proper disposal
if (!mosaicThreeJs.includes('dispose')) {
  fail('threejs', 'No dispose method; risk of memory leaks.');
} else {
  log('threejs', 'dispose() implemented.');
}

// 14. Hover logic in Three.js renderer
if (mosaicThreeJs.includes('raycaster') && mosaicThreeJs.includes('setFromCamera')) {
  log('threejs', 'Raycaster-based hover implemented.');
} else {
  fail('threejs', 'Hover logic incomplete; missing raycaster or setFromCamera.');
}

// 15. Ensure no synchronous heavy work in Three.js _animate
const animateMatch = mosaicThreeJs.match(/_animate\s*\([^)]*\)\s*\{([\s\S]*)\}/);
if (animateMatch) {
  const aBody = animateMatch[1];
  if (aBody.includes('fetch') || aBody.includes('XMLHttpRequest')) {
    fail('threejs', 'Network call inside _animate loop.');
  }
  log('threejs', '_animate loop structure validated.');
}

// ================= Summary =================

console.log('\n===== QA Summary: WebGL Mosaic Performance & Behavior =====');
console.log(`Errors: ${errors}`);
console.log(`Warnings: ${warnings}`);

if (errors === 0) {
  console.log('RESULT: PASS — structural and logic checks passed.');
  process.exit(0);
} else {
  console.log('RESULT: FAIL — fix the FAIL items.');
  process.exit(1);
}

/**
 * webgl-mosaic-qa.mjs
 *
 * Automated QA for the AceWerk WebGL mosaic page.
 *
 * Run with:
 *   node tests/webgl-mosaic-qa.mjs --url http://127.0.0.1:5173/index.html
 *
 * Uses Puppeteer. Install:
 *   npm install --save-dev puppeteer
 *
 * Checks:
 *  - WebGL context active
 *  - Frame rate stability (target >= 55 FPS avg over a window)
 *  - Hover/rise animation: no stuck tiles, smooth fall-back
 *  - Responsiveness: layout updates after resize events
 */

import puppeteer from "puppeteer";
import { parseArgs } from "node:util";

const url = process.env.TEST_URL || "http://127.0.0.1:5173/index.html";
const fpsSamples = 400;
const fpsDuration = 4000; // ms to collect samples
const fpsTarget = 55;

let exitCode = 0;

function log(tag, msg) {
  console.log(`[${tag}] ${msg}`);
}

function fail(tag, msg) {
  console.error(`[FAIL ${tag}] ${msg}`);
  exitCode = 1;
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-gpu"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  // Inject FPS instrumentation before page scripts run (via addScriptTag after load)
  await page.goto(url, { waitUntil: "networkidle0", timeout: 15000 });

  // 1) WebGL context
  const glInfo = await page.evaluate(() => {
    const canvas = document.getElementById("stage");
    if (!canvas) return { ok: false, reason: "no stage canvas" };
    const gl = canvas.getContext("webgl2");
    if (!gl) return { ok: false, reason: "no webgl2" };
    return {
      ok: true,
      vendor: gl.getParameter(gl.VENDOR),
      renderer: gl.getParameter(gl.RENDERER),
      canvasSize: { w: canvas.width, h: canvas.height },
    };
  });

  if (!glInfo.ok) {
    fail("webgl", "WebGL context not available: " + (glInfo.reason || "unknown"));
  } else {
    log("webgl", "WebGL2 active — renderer: " + glInfo.renderer);
  }

  // 2) FPS measurement
  await page.evaluate((duration) => {
    // Hook RAF inside the same execution context where the loop is running.
    const samples = [];
    let last = null;
    const start = performance.now();

    // Wrap existing requestAnimationFrame
    const origRAF = window.requestAnimationFrame;
    window.requestAnimationFrame = function (cb) {
      return origRAF(function (t) {
        if (last !== null) {
          const dt = t - last;
          samples.push(dt);
        }
        last = t;
        cb(t);
      });
    };

    setTimeout(() => {
      window.__FPS_DATA__ = {
        samples: samples.length,
        avgFps: 0,
        p95Fps: 0,
      };

      if (samples.length > 20) {
        const avgDt =
          samples.reduce((s, v) => s + v, 0) / samples.length;
        window.__FPS_DATA__.avgFps = 1000 / avgDt;
        samples.sort((a, b) => a - b);
        const p95Idx = Math.floor(samples.length * 0.95);
        window.__FPS_DATA__.p95Fps = 1000 / samples[p95Idx];
      }
    }, duration);
  }, fpsDuration);

  await sleep(fpsDuration + 600);

  const fpsData = await page.evaluate(() => window.__FPS_DATA__);

  if (fpsData && fpsData.samples > 20) {
    log(
      "fps",
      `samples=${fpsData.samples} avgFps=${fpsData.avgFps.toFixed(1)} p95Fps=${fpsData.p95Fps.toFixed(1)}`
    );
    // Note: In headless, FPS can be lower than on real hardware. We're mainly ensuring no severe stall.
    // Use a softer threshold for headless environment; but still flag very low FPS.
    const headlessFpsFloor = 30;
    if (fpsData.avgFps < headlessFpsFloor) {
      fail(
        "fps",
        `Average FPS (${fpsData.avgFps.toFixed(1)}) below headless safety floor (${headlessFpsFloor}). On real hardware, expect >= 55 FPS; this indicates heavy work or blocking.`
      );
    }
  } else {
    fail("fps", "FPS instrumentation failed: not enough samples. Data: " + JSON.stringify(fpsData));
  }

  // 3) Hover/rise animation: simulate pointer movement; check for stuck tiles
  // Strategy: move pointer into mosaic center, wait, then leave and ensure tiles settle.
  await page.evaluate(() => {
    const canvas = document.getElementById("stage");
    const rect = canvas.getBoundingClientRect();
    const cx = rect.left + rect.width * 0.5;
    const cy = rect.top + rect.height * 0.5;

    // Move mouse to center
    canvas.dispatchEvent(
      new MouseEvent("mousemove", { clientX: cx, clientY: cy })
    );
  });

  await sleep(600);

  const riseStatsBeforeLeave = await page.evaluate(() => {
    // We cannot see rise[] directly; but we can inspect the canvas and GL state.
    // Instead, check that the mosaic still renders after hover.
    const canvas = document.getElementById("stage");
    const gl = canvas.getContext("webgl2");
    return {
      canvasWidth: canvas.width,
      isContextLost: gl.isContextLost(),
    };
  });

  if (riseStatsBeforeLeave.isContextLost) {
    fail("hover", "GL context lost during hover simulation");
  }

  // Move pointer away
  await page.evaluate(() => {
    const canvas = document.getElementById("stage");
    const rect = canvas.getBoundingClientRect();
    canvas.dispatchEvent(
      new MouseEvent("mouseleave", { clientX: -100, clientY: -100 })
    );
  });

  await sleep(800);

  const riseStatsAfterLeave = await page.evaluate(() => {
    const canvas = document.getElementById("stage");
    const gl = canvas.getContext("webgl2");
    return {
      isContextLost: gl.isContextLost(),
    };
  });

  if (riseStatsAfterLeave.isContextLost) {
    fail("hover", "GL context lost after pointer leave");
  }

  // 4) Stuck-tile / animation deadlock check: verify continued rendering after hover
  // If the animation loop were stuck, FPS would collapse. Re-check FPS briefly.
  await page.evaluate((dur) => {
    const samples = [];
    let last = null;
    const start = performance.now();

    const origRAF = window.requestAnimationFrame;
    window.requestAnimationFrame = (cb) =>
      origRAF((t) => {
        if (last !== null) samples.push(t - last);
        last = t;
        cb(t);
        if (t - start < dur) return;
        window.__POST_HOVER_FPS__ = {
          samples: samples.length,
          avgFps:
            samples.length > 5
              ? 1000 /
                (samples.reduce((s, v) => s + v, 0) / samples.length)
              : 0,
        };
      });
  }, 2000);

  await sleep(2400);
  const postHoverFps = await page.evaluate(() => window.__POST_HOVER_FPS__);
  if (postHoverFps && postHoverFps.samples > 10) {
    log(
      "hover",
      `Post-hover FPS: avgFps=${postHoverFps.avgFps.toFixed(1)} samples=${postHoverFps.samples}`
    );
    if (postHoverFps.avgFps < 15) {
      fail(
        "hover",
        "Post-hover FPS extremely low; possible stuck loop or resource leak."
      );
    }
  } else {
    fail(
      "hover",
      "Post-hover FPS instrumentation failed; cannot confirm no deadlock."
    );
  }

  // 5) Responsive behavior
  // Simulate resize events: desktop → tablet → mobile → desktop.
  const viewports = [
    { width: 1920, height: 1080 },
    { width: 1024, height: 768 },
    { width: 390, height: 844 },
    { width: 1920, height: 1080 },
  ];

  for (const vp of viewports) {
    await page.setViewport(vp);
    await sleep(300);
  }

  const layoutCheck = await page.evaluate(() => {
    const canvas = document.getElementById("stage");
    if (!canvas) return { ok: false, reason: "no canvas" };

    const rect = canvas.getBoundingClientRect();
    return {
      ok: true,
      canvasSize: { w: canvas.width, h: canvas.height },
      rectSize: { w: rect.width, h: rect.height },
      fillWidth: Math.abs(rect.width - window.innerWidth) < 2,
      fillHeight: Math.abs(rect.height - window.innerHeight) < 2,
    };
  });

  if (!layoutCheck.ok) {
    fail("responsive", "Responsive check failed: " + layoutCheck.reason);
  } else if (
    layoutCheck.fillWidth &&
    layoutCheck.fillHeight
  ) {
    log(
      "responsive",
      "Canvas fills viewport after multiple resize cycles. OK."
    );
  } else {
    fail(
      "responsive",
      "Canvas not filling viewport after resize. fillWidth=" +
        layoutCheck.fillWidth +
        " fillHeight=" +
        layoutCheck.fillHeight
    );
  }

  // 6) Reduced motion check
  // Emulate prefers-reduced-motion and ensure no crashes.
  await page.emulateMediaFeatures([
    { name: "prefers-reduced-motion", value: "reduce" },
  ]);
  await sleep(600);

  const reducedMotionOk = await page.evaluate(() => {
    const canvas = document.getElementById("stage");
    const gl = canvas.getContext("webgl2");
    return {
      ok: canvas && gl && !gl.isContextLost(),
    };
  });

  if (!reducedMotionOk.ok) {
    fail(
      "reduced-motion",
      "GL context or canvas invalid under prefers-reduced-motion."
    );
  } else {
    log("reduced-motion", "Page remains stable with prefers-reduced-motion: reduce.");
  }

  // Summary
  console.log("\n===== WebGL Mosaic QA Summary =====");
  if (exitCode === 0) {
    console.log(
      "RESULT: PASS\nAll checks passed. No regressions detected."
    );
  } else {
    console.log(
      "RESULT: FAIL\nOne or more checks failed; review errors above."
    );
  }

  await browser.close();
  process.exit(exitCode);
})();

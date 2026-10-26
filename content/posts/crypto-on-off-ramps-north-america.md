---
title: "Crypto On/Off-Ramps in North America: 16 Providers Compared"
slug: crypto-on-off-ramps-north-america
date: 2026-10-13
updated: 2026-10-21
author: "Illya Swan"
description: "We checked 16 providers' own documentation for Interac, ACH, RTP and SPEI coverage in Canada, the US and Mexico — both directions, conditions included."
excerpt: "A country-by-country coverage map of crypto on-ramps and off-ramps in Canada, the US and Mexico, built from 16 providers' own documentation: which local rails exist, which direction each one runs, and what each provider attaches to it."
tags: "Crypto On/Off-Ramps, Payment Infrastructure, North America"
raw_html: true
---

Local crypto rails run both ways in Canada (Interac e-Transfer), the United States (ACH and RTP) and Mexico (SPEI). The tables show both directions in each market, often with geographic, amount, fee or receiving-bank conditions, but Banxa alone has a Supported Canadian Interac payout among table providers; Kraken documents one separately as a consumer exchange. One product can serve all three markets, but no single integrable provider documents both directions everywhere; buy and sell coverage must be checked separately.

## How to read the tables

The tables compare 13 product entries from 12 providers; four other providers appear in notes below, for 16 providers checked in all. Cells were checked on 21 October 2026.

<!-- html -->
<style id="rampx-css">/* ══════════════════════════════════════════════════════════════════════════
   ACE-34 · rampx-* — country coverage component  (rev 2)
   Article: /blog/crypto-on-off-ramps-north-america/

   Paste this whole file, unchanged, into ONE <style> block in the article.
   Every selector is .rampx or .rampx-*; no shared stylesheet or template
   change. All custom properties are declared on the component, which inherits
   the Tesserae / Digital Craft tokens from :root.

   Dark is the shipping theme. Light exists behind [data-rampx-theme="light"]
   and is inert on the live blog (nothing sets it there).

   Layout is decided by CONTAINER queries on the component itself, so the
   table/card switch follows the article column, not the window:
     > 720px  → five-column table (compact below 900px)
     <= 720px → one card per provider, rail left, status right
   ══════════════════════════════════════════════════════════════════════════ */

/* ── tokens ─────────────────────────────────────────────────────────────── */
.rampx,
.rampx-howto {
  --rampx-font-body: 'Space Grotesk', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --rampx-font-display: 'Rajdhani', 'Arial Narrow', system-ui, sans-serif;
  --rampx-font-mono: 'JetBrains Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace;
  /* the self-hosted latin subsets carry none of ● ◐ ◷ ✕ ○ — they resolve to a
     system symbol face; the fixed inline-size below absorbs the metric drift */
  --rampx-font-symbol: 'Segoe UI Symbol', 'Apple Symbols', 'Noto Sans Symbols 2', 'DejaVu Sans', system-ui, sans-serif;

  --rampx-radius: var(--radius-md, 9px);
  --rampx-radius-sm: var(--radius-sm, 6px);

  --rampx-surface: var(--surface, #0c1122);
  --rampx-surface-plus: var(--surface-plus, #11182b);
  --rampx-shell: rgba(255, 255, 255, 0.02);
  --rampx-shell-hover: rgba(255, 255, 255, 0.033);
  --rampx-ink: var(--ink, #e5e7f0);
  --rampx-muted: var(--ink-muted, rgba(190, 200, 220, 0.88));
  --rampx-head-ink: rgba(190, 200, 220, 0.62);
  --rampx-glass: var(--glass-border, rgba(255, 255, 255, 0.11));
  --rampx-rule: var(--rule, rgba(255, 255, 255, 0.09));
  --rampx-rule-soft: var(--rule-soft, rgba(255, 255, 255, 0.055));
  --rampx-accent: var(--accent, #d49a2e);
  --rampx-accent-soft: var(--accent-soft, #f4d39e);
  --rampx-accent-border: var(--accent-border, rgba(212, 154, 46, 0.42));
  --rampx-tag-bg: rgba(255, 255, 255, 0.045);
  --rampx-focus: #ffffff;

  /* status hues (dark) */
  --rampx-ok: #57c99a;
  --rampx-ok-tint: rgba(87, 201, 154, 0.10);
  --rampx-ok-line: rgba(87, 201, 154, 0.32);
  --rampx-cond: #e0a83e;
  --rampx-cond-tint: rgba(224, 168, 62, 0.10);
  --rampx-cond-line: rgba(224, 168, 62, 0.34);
  --rampx-plan: #8ea2ff;
  --rampx-plan-tint: rgba(142, 162, 255, 0.10);
  --rampx-plan-line: rgba(142, 162, 255, 0.34);
  --rampx-no: #e58077;
  --rampx-no-tint: rgba(229, 128, 119, 0.10);
  --rampx-no-line: rgba(229, 128, 119, 0.32);
  --rampx-unknown: #9aa5b8;
  --rampx-unknown-tint: rgba(154, 165, 184, 0.07);
  --rampx-unknown-line: rgba(154, 165, 184, 0.24);

  container-type: inline-size;
  container-name: rampx;
}

.rampx,
.rampx *,
.rampx *::before,
.rampx *::after,
.rampx-howto,
.rampx-howto * { box-sizing: border-box; }

/* ── light theme (inert on the live blog) ───────────────────────────────── */
.rampx[data-rampx-theme="light"],
.rampx-howto[data-rampx-theme="light"],
[data-rampx-theme="light"] .rampx,
[data-rampx-theme="light"] .rampx-howto {
  --rampx-surface: #ffffff;
  --rampx-surface-plus: #eef1f6;
  --rampx-shell: #ffffff;
  --rampx-shell-hover: #f6f8fb;
  --rampx-ink: #0b1020;
  --rampx-muted: #4b5568;
  --rampx-head-ink: #5d6779;
  --rampx-glass: #d8dee9;
  --rampx-rule: #dde3ee;
  --rampx-rule-soft: #e8ecf3;
  --rampx-accent: #a8700f;
  --rampx-accent-soft: #7a5208;
  --rampx-accent-border: rgba(168, 112, 15, 0.45);
  --rampx-tag-bg: #f1f4f9;
  --rampx-focus: #0b1020;
  --rampx-ok: #17734a;
  --rampx-ok-tint: rgba(23, 115, 74, 0.09);
  --rampx-ok-line: rgba(23, 115, 74, 0.30);
  --rampx-cond: #8a5b06;
  --rampx-cond-tint: rgba(138, 91, 6, 0.09);
  --rampx-cond-line: rgba(138, 91, 6, 0.30);
  --rampx-plan: #2f5f96;
  --rampx-plan-tint: rgba(47, 95, 150, 0.09);
  --rampx-plan-line: rgba(47, 95, 150, 0.30);
  --rampx-no: #a83b2d;
  --rampx-no-tint: rgba(168, 59, 45, 0.08);
  --rampx-no-line: rgba(168, 59, 45, 0.28);
  --rampx-unknown: #5b6577;
  --rampx-unknown-tint: rgba(91, 101, 119, 0.06);
  --rampx-unknown-line: rgba(91, 101, 119, 0.22);
}

/* ══════════════════════════════════════════════════════════════════════════
   ROOT
   ══════════════════════════════════════════════════════════════════════════ */
.rampx {
  margin: 2.5em 0 2.75em;
  font-family: var(--rampx-font-body);
  font-size: 13px;
  font-weight: 300;
  line-height: 1.55;
  color: var(--rampx-ink);
}

/* ══════════════════════════════════════════════════════════════════════════
   STATUS CHIP — one geometry, five colour sets.
   Used in the key row, in table cells, in cards and in the definitions list.
   ══════════════════════════════════════════════════════════════════════════ */
.rampx-st {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 7px 2px 6px;
  border: 1px solid var(--rampx-unknown-line);
  border-radius: 4px;
  background: var(--rampx-unknown-tint);
  color: var(--rampx-unknown);
  font-family: var(--rampx-font-body);
  font-size: 11px;
  font-weight: 500;
  line-height: 1.4;
  letter-spacing: 0.005em;
  white-space: nowrap;
}

.rampx-st-glyph {
  display: inline-block;
  flex: 0 0 auto;
  inline-size: 9px;
  font-family: var(--rampx-font-symbol);
  font-size: 11px; /* --fs-min */
  line-height: 1;
  text-align: center;
  transform: translateY(-0.5px);
}

.rampx-st[data-status="documented"] { color: var(--rampx-ok); background: var(--rampx-ok-tint); border-color: var(--rampx-ok-line); }
.rampx-st[data-status="conditional"] { color: var(--rampx-cond); background: var(--rampx-cond-tint); border-color: var(--rampx-cond-line); }
.rampx-st[data-status="planned"] { color: var(--rampx-plan); background: var(--rampx-plan-tint); border-color: var(--rampx-plan-line); }
.rampx-st[data-status="not-offered"] { color: var(--rampx-no); background: var(--rampx-no-tint); border-color: var(--rampx-no-line); }
.rampx-st[data-status="not-documented"] { color: var(--rampx-unknown); background: var(--rampx-unknown-tint); border-color: var(--rampx-unknown-line); }

/* "not applicable": a plain dash, no key entry, no chip */
.rampx-na-label {
  position: absolute;
  inline-size: 1px;
  block-size: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
.rampx-na {
  display: inline-block;
  font-family: var(--rampx-font-body);
  font-size: 14px;
  font-weight: 400;
  line-height: 1.2;
  color: var(--rampx-muted);
  opacity: 0.65;
}

/* ══════════════════════════════════════════════════════════════════════════
   TABS — hidden without JS, so the three tables simply stack
   ══════════════════════════════════════════════════════════════════════════ */
.rampx-tabs {
  display: none;
  align-items: flex-end;
  gap: 2px;
  margin: 0 0 14px;
  border-bottom: 1px solid var(--rampx-rule);
}

.rampx[data-rampx-enhanced="true"] .rampx-tabs { display: flex; }

.rampx-tab {
  appearance: none;
  -webkit-appearance: none;
  position: relative;
  top: 1px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  padding: 9px 14px 10px;
  min-height: 40px;
  border: 1px solid transparent;
  border-bottom: 0;
  border-radius: var(--rampx-radius-sm) var(--rampx-radius-sm) 0 0;
  background: transparent;
  font-family: var(--rampx-font-body);
  font-size: 13px;
  font-weight: 500;
  line-height: 1.2;
  letter-spacing: 0.01em;
  color: var(--rampx-muted);
  cursor: pointer;
}

.rampx-tab:hover { color: var(--rampx-ink); }

.rampx-tab[aria-selected="true"] {
  color: #fff;
  background: var(--rampx-surface);
  border-color: var(--rampx-glass);
  box-shadow: inset 0 2px 0 var(--rampx-accent);
}
[data-rampx-theme="light"] .rampx-tab[aria-selected="true"] { color: var(--rampx-ink); }

.rampx-tab:focus-visible {
  outline: 2px solid var(--rampx-focus);
  outline-offset: 2px;
  border-radius: 3px;
}

.rampx-tab-count {
  padding: 2px 4px;
  border: 1px solid var(--rampx-rule);
  border-radius: 3px;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  line-height: 1;
  color: var(--rampx-muted);
}
.rampx-tab[aria-selected="true"] .rampx-tab-count {
  border-color: var(--rampx-accent-border);
  color: var(--rampx-accent-soft);
}

@media (prefers-reduced-motion: no-preference) {
  .rampx-tab { transition: color 0.16s ease-out, background 0.16s ease-out; }
}

/* ══════════════════════════════════════════════════════════════════════════
   PANEL · KEY ROW · TABLE
   ══════════════════════════════════════════════════════════════════════════ */
.rampx-panel { display: block; }
.rampx-panel[hidden] { display: none; }
.rampx-panel:focus-visible {
  outline: 2px solid var(--rampx-focus);
  outline-offset: 6px;
  border-radius: var(--rampx-radius);
}

.rampx-panel-title {
  margin: 0 0 8px;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--rampx-accent);
}
.rampx-panel-title span { color: var(--rampx-muted); letter-spacing: 0.06em; }

/* with working tabs the strip already names the country: keep the title for AT */
.rampx[data-rampx-enhanced="true"] .rampx-panel-title {
  position: absolute;
  inline-size: 1px;
  block-size: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}

.rampx-keybar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px 16px;
  margin: 0 0 10px;
}

.rampx-key {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.rampx-key > li { margin: 0; padding: 0; list-style: none; }
.rampx-key .rampx-st { font-size: 11px; /* --fs-min */ padding: 2px 6px 2px 5px; gap: 5px; }

.rampx-meta {
  margin: 0;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--rampx-head-ink);
  white-space: nowrap;
}
.rampx-meta a {
  color: var(--rampx-accent-soft);
  text-decoration: underline;
  text-decoration-color: var(--rampx-accent-border);
  text-underline-offset: 2px;
}
.rampx-meta a:focus-visible { outline: 2px solid var(--rampx-focus); outline-offset: 2px; }

/* ── table shell ────────────────────────────────────────────────────────── */
.rampx-tablewrap {
  border: 1px solid var(--rampx-glass);
  border-radius: var(--rampx-radius);
  background: var(--rampx-shell);
  overflow: hidden;
}

.rampx-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  font-family: var(--rampx-font-body);
  font-size: 12.5px;
  font-weight: 300;
  line-height: 1.5;
  color: var(--rampx-ink);
}

/* column measure: fixed layout, so the widths are the layout */
.rampx-col-prov { width: 18%; }
.rampx-col-rail { width: 19%; }
.rampx-col-buy,
.rampx-col-sell { width: 15%; }
.rampx-col-cond { width: 33%; }

.rampx-caption {
  position: absolute;
  inline-size: 1px;
  block-size: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}

.rampx-table thead th {
  padding: 8px 10px;
  background: var(--rampx-surface-plus);
  border-bottom: 1px solid var(--rampx-accent-border);
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.13em;
  line-height: 1.3;
  text-transform: uppercase;
  text-align: left;
  vertical-align: bottom;
  color: var(--rampx-head-ink);
}
.rampx-table thead th.rampx-c-dir { color: var(--rampx-accent-soft); }

.rampx-tr > * {
  padding: 10px;
  border-top: 1px solid var(--rampx-rule-soft);
  text-align: left;
  vertical-align: top;
}
.rampx-tbody:first-of-type .rampx-tr:first-child > * { border-top: 0; }
.rampx-tbody + .rampx-tbody .rampx-tr:first-child > * { border-top: 1px solid var(--rampx-rule); }
/* Row-group hover: a rail row highlights alone (never the provider cell);
   hovering the provider cell highlights every row it spans. */
.rampx-tr:hover:not(:has(> .rampx-prov:hover)) > :not(.rampx-prov),
.rampx-tbody:has(> .rampx-tr > .rampx-prov:hover) > .rampx-tr > * { background: var(--rampx-shell-hover); }
@supports not selector(:has(*)) {
  .rampx-tr:hover > :not(.rampx-prov) { background: var(--rampx-shell-hover); }
}

.rampx-prov {
  font-family: var(--rampx-font-body);
  font-size: 13px;
  font-weight: 500;
  line-height: 1.3;
  letter-spacing: 0.005em;
  color: #fff;
}
[data-rampx-theme="light"] .rampx-prov { color: var(--rampx-ink); }

.rampx-tag {
  display: block;
  width: max-content;
  max-width: 100%;
  margin-top: 5px;
  padding: 2px 5px;
  border: 1px solid var(--rampx-glass);
  border-radius: 3px;
  background: var(--rampx-tag-bg);
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.08em;
  line-height: 1.5;
  text-transform: uppercase;
  white-space: nowrap;
  color: var(--rampx-muted);
}

.rampx-rail {
  font-family: var(--rampx-font-body);
  font-size: 12.5px;
  font-weight: 400;
  line-height: 1.4;
  color: var(--rampx-ink);
  overflow-wrap: break-word;
}
.rampx-rail-sub {
  display: block;
  margin-top: 3px;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--rampx-muted);
}
.rampx-src {
  display: inline-block;
  margin-left: 4px;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  line-height: 1;
  color: var(--rampx-accent);
  text-decoration: none;
  vertical-align: 1px;
}
.rampx-src:hover { color: var(--rampx-accent-soft); }
.rampx-src:focus-visible { outline: 2px solid var(--rampx-focus); outline-offset: 2px; }

.rampx-dir { display: none; }

.rampx-cond { color: var(--rampx-muted); font-size: 11.5px; line-height: 1.5; }
.rampx-conds { margin: 0; padding: 0; list-style: none; }
.rampx-conds > li { margin: 0; padding: 0; }
.rampx-conds > li + li { margin-top: 4px; }
.rampx-cond-dir {
  margin-right: 5px;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--rampx-accent-soft);
}
.rampx-cond-short { display: none; margin: 0; }

/* ── excluded providers line ────────────────────────────────────────────── */
.rampx-excluded {
  margin: 9px 0 0;
  padding: 0 0 0 10px;
  border-left: 2px solid var(--rampx-rule);
  font-size: 11.5px;
  line-height: 1.55;
  color: var(--rampx-muted);
}
.rampx-excluded-label {
  display: inline;
  margin: 0 6px 0 0;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--rampx-unknown);
  white-space: nowrap;
}
.rampx-excluded-names { color: var(--rampx-ink); }

/* ══════════════════════════════════════════════════════════════════════════
   HOW TO READ THIS — definitions, collapsed, once per article
   ══════════════════════════════════════════════════════════════════════════ */
.rampx--howto { margin: 1.5em 0 1.75em; }
.rampx-howto {
  margin: 0;
  scroll-margin-top: 72px;
  border: 1px solid var(--rampx-glass);
  border-radius: var(--rampx-radius);
  background: var(--rampx-shell);
  font-family: var(--rampx-font-body);
  font-size: 13px;
  font-weight: 300;
  line-height: 1.55;
  color: var(--rampx-ink);
}
.rampx-howto > summary {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 11px 14px;
  border-radius: var(--rampx-radius);
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.12em;
  line-height: 1.4;
  text-transform: uppercase;
  color: var(--rampx-accent);
  cursor: pointer;
  list-style: none;
}
.rampx-howto > summary::-webkit-details-marker { display: none; }
.rampx-howto > summary::before {
  content: "+";
  flex: 0 0 auto;
  inline-size: 10px;
  font-size: 13px;
  line-height: 1;
  color: var(--rampx-accent);
}
.rampx-howto[open] > summary::before { content: "–"; }
.rampx-howto > summary:hover { color: var(--rampx-accent-soft); }
.rampx-howto > summary:focus-visible {
  outline: 2px solid var(--rampx-focus);
  outline-offset: -2px;
}

.rampx-howto-body { padding: 2px 14px 14px; border-top: 1px solid var(--rampx-rule-soft); }
.rampx-defs {
  display: grid;
  grid-template-columns: 172px minmax(0, 1fr);
  gap: 10px 16px;
  margin: 14px 0 0;
  padding: 0;
}
.rampx-defs dt { margin: 0; }
.rampx-defs dd {
  margin: 0;
  font-size: 12.5px;
  line-height: 1.55;
  color: var(--rampx-muted);
}
.rampx-howto-note {
  margin: 14px 0 0;
  padding-top: 12px;
  border-top: 1px solid var(--rampx-rule-soft);
  font-size: 11.5px;
  line-height: 1.6;
  color: var(--rampx-muted);
}
.rampx-howto-note strong { color: var(--rampx-ink); font-weight: 500; }

/* ══════════════════════════════════════════════════════════════════════════
   COMPACT TABLE — 701-900px of column: narrower cells, smaller chips, more
   room for the two direction columns so no label is ever clipped.
   ══════════════════════════════════════════════════════════════════════════ */
@container rampx (max-width: 900px) {
  .rampx-col-prov { width: 17%; }
  .rampx-col-rail { width: 18%; }
  .rampx-col-buy,
  .rampx-col-sell { width: 16%; }
  .rampx-col-cond { width: 33%; }

  .rampx-tr > * { padding: 9px 8px; }
  .rampx-td .rampx-st,
  .rampx-st { font-size: 11px; /* --fs-min */ padding: 2px 5px 2px 4px; gap: 5px; }
  .rampx-cond { font-size: 11px; }
  .rampx-prov { font-size: 12.5px; }
}

/* ══════════════════════════════════════════════════════════════════════════
   MOBILE — container <= 720px: one card per provider. No table.
   Card: provider · rail left · status right · one condition line under.
   ══════════════════════════════════════════════════════════════════════════ */
@container rampx (max-width: 720px) {
  .rampx { margin: 1.9em 0 2.1em; }
  .rampx-tabs { gap: 0; margin-bottom: 12px; }
  .rampx-tab {
    flex: 1 1 0;
    justify-content: center;
    min-width: 0;
    padding: 9px 5px 10px;
    font-size: 12.5px;
    gap: 5px;
    white-space: nowrap;
  }
  .rampx-keybar { display: block; margin-bottom: 12px; }
  .rampx-key { gap: 5px; }
  .rampx-key .rampx-st { font-size: 11px; /* --fs-min */ padding: 2px 5px 2px 4px; gap: 4px; }
  .rampx-meta { display: block; margin-top: 8px; white-space: normal; line-height: 1.5; }

  .rampx-tablewrap {
    border: 0;
    border-radius: 0;
    background: none;
    
    
    -webkit-overflow-scrolling: touch;
  }

  .rampx-panel {
    
    -webkit-overflow-scrolling: touch;
  }

  .rampx-src {
    display: block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .rampx-src a {
    display: block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    word-break: break-all;
  }

  .rampx-table,
  .rampx-thead,
  .rampx-tbody,
  .rampx-tr,
  .rampx-td { display: block; }

  .rampx-table { font-size: 13px; }

  .rampx-thead {
    position: absolute;
    inline-size: 1px;
    block-size: 1px;
    margin: -1px;
    padding: 0;
    overflow: hidden;
    clip-path: inset(50%);
    white-space: nowrap;
    border: 0;
  }

  .rampx-tbody {
    margin: 0 0 8px;
    padding: 11px 13px 12px;
    border: 1px solid var(--rampx-glass);
    border-radius: var(--rampx-radius);
    background: var(--rampx-shell);
  }
  .rampx-tbody:last-of-type { margin-bottom: 0; }

  .rampx-tr {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    grid-template-areas:
      "rail buy"
      "rail sell"
      "cond cond";
    column-gap: 12px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--rampx-rule-soft);
  }
  .rampx-tr:first-child {
    grid-template-areas:
      "prov prov"
      "rail buy"
      "rail sell"
      "cond cond";
    margin-top: 0;
    padding-top: 0;
    border-top: 0;
  }

  .rampx-tr > * { padding: 0; border: 0; }
  .rampx-tr:hover > :not(.rampx-prov) { background: none; }
  .rampx-tr:hover:not(:has(> .rampx-prov:hover)) > :not(.rampx-prov),
  .rampx-tbody:has(> .rampx-tr > .rampx-prov:hover) > .rampx-tr > * { background: none; }

  .rampx-prov {
    grid-area: prov;
    padding: 0 0 7px;
    font-size: 14.5px;
    line-height: 1.25;
  }
  .rampx-prov .rampx-tag { margin-top: 4px; }

  .rampx-rail {
    grid-area: rail;
    align-self: center;
    padding-top: 1px;
    font-size: 13px;
    line-height: 1.35;
  }
  .rampx-rail-sub { margin-top: 2px; }

  .rampx-buy, .rampx-sell { justify-self: end; text-align: right; }
  .rampx-buy { grid-area: buy; }
  .rampx-sell { grid-area: sell; margin-top: 2px; }

  .rampx-dir {
    display: block;
    margin-bottom: 3px;
    font-family: var(--rampx-font-mono);
    font-size: 11px; /* --fs-min */
    font-weight: 400;
    letter-spacing: 0.1em;
    line-height: 1;
    text-transform: uppercase;
    color: var(--rampx-head-ink);
  }
  .rampx-td .rampx-st { font-size: 11px; /* --fs-min */ padding: 2px 6px 2px 5px; }

  .rampx-cond {
    grid-area: cond;
    padding-top: 6px;
    font-size: 11.5px;
    line-height: 1.45;
  }
  .rampx-conds { display: none; }
  .rampx-cond-short {
    display: block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .rampx-excluded { margin-top: 10px; font-size: 11.5px; }
  .rampx-excluded-label { display: block; margin: 0 0 3px; }

  .rampx-defs { grid-template-columns: minmax(0, 1fr); gap: 5px; }
  .rampx-defs dt { margin-top: 9px; }
  .rampx-defs dd { font-size: 12px; }
  .rampx-howto > summary { padding: 10px 12px; font-size: 11px; /* --fs-min */ }
  .rampx-howto-body { padding: 2px 12px 12px; }
}

@container rampx (max-width: 380px) {
  .rampx-key .rampx-st { font-size: 11px; /* --fs-min */ letter-spacing: -0.01em; }
  .rampx-tab { font-size: 12px; padding: 8px 3px 9px; }
  .rampx-tab-count { display: none; }
}

/* ══════════════════════════════════════════════════════════════════════════
   PRINT — all three countries, no tabs
   ══════════════════════════════════════════════════════════════════════════ */
@media print {
  .rampx-tabs { display: none !important; }
  .rampx-panel[hidden] { display: block !important; }
  .rampx[data-rampx-enhanced="true"] .rampx-panel-title {
    position: static;
    inline-size: auto;
    block-size: auto;
    margin: 0 0 8px;
    clip-path: none;
    overflow: visible;
    white-space: normal;
  }
  .rampx-tbody { break-inside: avoid; }
  .rampx-howto { display: none; }
}

/* ══════ STATUS KEY TOOLTIPS ══════ */
.rampx-keychip {
  display: inline-flex; align-items: center; gap: 5px;
  font-family: var(--rampx-font-mono);
  font-size: 11px; /* --fs-min */
  font-weight: 400;
  letter-spacing: 0.02em;
  padding: 2px 6px 2px 5px;
  border: 1px solid var(--rampx-rule);
  border-radius: 999px;
  background: var(--rampx-surface-plus);
  color: var(--rampx-ink);
  cursor: pointer;
  transition: border-color var(--rampx-transition), background var(--rampx-transition);
}
.rampx-keychip:hover,
.rampx-keychip:focus-visible {
  border-color: var(--rampx-accent);
  background: var(--rampx-surface);
}
.rampx-keychip[aria-expanded="true"] {
  border-color: var(--rampx-accent);
  background: var(--rampx-surface);
}
/* ══════ SHARED STATUS TOOLTIP (R2) ══════
   INVARIANT: #rampx-tooltip is a direct child of <body> and position: fixed,
   so no ancestor (overflow: hidden, clip-path, overflow-wrap column, table
   wrapper) can clip it or shift its coordinate system. It must never be
   nested inside a transformed or filtered element. JS sets top/left only. */
#rampx-tooltip {
  --rampx-tip-bg: #141b2e;
  --rampx-tip-border: rgba(255, 255, 255, 0.14);
  --rampx-tip-ink: var(--rampx-ink, #e5e7f0);
  position: fixed;
  top: 0;
  left: 0;
  display: none;
  width: max-content;
  max-width: 260px;
  padding: 8px 12px;
  border: 1px solid var(--rampx-tip-border);
  border-radius: 6px;
  background: var(--rampx-tip-bg);
  color: var(--rampx-tip-ink);
  font-family: var(--rampx-font-body, 'Space Grotesk', system-ui, sans-serif);
  font-size: 12px;
  font-weight: 400;
  line-height: 1.4;
  text-align: left;
  white-space: normal;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  pointer-events: none;
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.12s ease-out;
  z-index: 999;
}
#rampx-tooltip.is-open {
  display: block;
  visibility: visible;
  opacity: 1;
}
#rampx-tooltip::after {
  content: "";
  position: absolute;
  top: 100%;
  left: var(--rampx-tip-arrow-x, 50%);
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: var(--rampx-tip-border);
}
#rampx-tooltip.rampx-tip-below::after {
  top: auto;
  bottom: 100%;
  border-top-color: transparent;
  border-bottom-color: var(--rampx-tip-border);
}
#rampx-tooltip[data-rampx-theme="light"] {
  --rampx-tip-bg: #ffffff;
  --rampx-tip-border: #d8dee9;
  --rampx-tip-ink: #0b1020;
}
</style>
<div class="rampx rampx--howto">
<details class="rampx-howto" id="rampx-howto">
  <summary>How to read this table</summary>
  <div class="rampx-howto-body">
    <dl class="rampx-defs">
      <dt><span class="rampx-st" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></dt>
      <dd>The provider's own documentation says this rail works in this direction.</dd>
      <dt><span class="rampx-st" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></dt>
      <dd>Supported, with a limit: for example region, amount, account type, invitation-only access, or a bank that must support the rail.</dd>
      <dt><span class="rampx-st" data-status="planned"><span class="rampx-st-glyph" aria-hidden="true">◷</span>Planned</span></dt>
      <dd>Announced by the provider for a future date. Not live when we checked.</dd>
      <dt><span class="rampx-st" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></dt>
      <dd>The provider's documentation says this rail or country isn't available.</dd>
      <dt><span class="rampx-st" data-status="not-documented"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</span></dt>
      <dd>We found nothing either way in the provider's documentation. This isn't the same as not supported.</dd>
    </dl>
    <p class="rampx-howto-note"><strong>Buy</strong> is fiat in, <strong>Sell</strong> is fiat out; a merchant-side row that collects fiat sits in Buy. A dash (–) means the direction does not apply to that rail, so there is nothing to document. Each table lists only providers with at least one Supported, With conditions or Planned rail in that country; the rest are named under the table. 131 records in the dataset, 16 providers checked on 21 October 2026.</p>
  </div>
</details>
</div>
<div class="rampx" data-rampx="coverage">
  <div class="rampx-tabs" role="tablist" aria-label="Country">
    <button class="rampx-tab" type="button" role="tab" id="rampx-tab-ca" aria-controls="rampx-panel-ca" aria-selected="true" tabindex="0" aria-label="Canada, 6 providers">Canada<span class="rampx-tab-count">6</span></button>
    <button class="rampx-tab" type="button" role="tab" id="rampx-tab-us" aria-controls="rampx-panel-us" aria-selected="false" tabindex="-1" aria-label="United States, 12 providers">United States<span class="rampx-tab-count">12</span></button>
    <button class="rampx-tab" type="button" role="tab" id="rampx-tab-mx" aria-controls="rampx-panel-mx" aria-selected="false" tabindex="-1" aria-label="Mexico, 10 providers">Mexico<span class="rampx-tab-count">10</span></button>
  </div>
  <div class="rampx-panel" role="tabpanel" id="rampx-panel-ca" aria-labelledby="rampx-tab-ca" tabindex="0">
    <h3 class="rampx-panel-title">Canada <span>· 6 providers, 8 rows</span></h3>
<div class="rampx-keybar">
  <ul class="rampx-key" aria-label="Status key">
    <li><button type="button" class="rampx-keychip" data-status="documented" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</button></li><li><button type="button" class="rampx-keychip" data-status="conditional" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</button></li><li><button type="button" class="rampx-keychip" data-status="planned" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">◷</span>Planned</button></li><li><button type="button" class="rampx-keychip" data-status="not-offered" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</button></li><li><button type="button" class="rampx-keychip" data-status="not-documented" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</button></li>
  </ul>
  <p class="rampx-meta">6 of 13 product entries · <a href="#rampx-howto">How to read this</a></p>
</div>
<div class="rampx-tablewrap">
  <table class="rampx-table">
    <caption class="rampx-caption">Canada — local rail coverage by provider and direction, checked 21 October 2026</caption>
    <colgroup>
      <col class="rampx-col-prov"><col class="rampx-col-rail">
      <col class="rampx-col-buy"><col class="rampx-col-sell">
      <col class="rampx-col-cond">
    </colgroup>
    <thead class="rampx-thead">
      <tr>
        <th scope="col">Provider</th>
        <th scope="col">Rail</th>
        <th scope="col" class="rampx-c-dir">Buy</th>
        <th scope="col" class="rampx-c-dir">Sell</th>
        <th scope="col">Conditions</th>
      </tr>
    </thead>
    <tbody class="rampx-tbody" data-provider="Banxa">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">Banxa<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Interac e-Transfer<a class="rampx-src" href="https://docs.banxa.com/products/hosted-checkout/docs/reference/supported-payment-methods" aria-label="Source: Banxa, Interac e-Transfer, Canada" title="Source: Banxa, Interac e-Transfer, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Instant, in CAD</li></ul><p class="rampx-cond-short">Instant, in CAD</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://docs.banxa.com/products/hosted-checkout/docs/reference/supported-payment-methods" aria-label="Source: Banxa, Card, Canada" title="Source: Banxa, Card, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>No prepaid cards</li><li><span class="rampx-cond-dir">sell</span>Card payouts: selected EU countries only</li></ul><p class="rampx-cond-short">Card payouts: selected EU countries only</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Mercuryo">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Mercuryo<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Interac e-Transfer<a class="rampx-src" href="https://help.mercuryo.io/hc/en-gb/articles/14806047888669-Which-payment-methods-does-Mercuryo-support" aria-label="Source: Mercuryo, Interac e-Transfer, Canada" title="Source: Mercuryo, Interac e-Transfer, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-documented"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Interac e-Transfer buy supported in Canada</li><li><span class="rampx-cond-dir">sell</span>No Interac sell; card payouts only</li></ul><p class="rampx-cond-short">No Interac sell; card payouts only</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="MoonPay">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">MoonPay<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Interac e-Transfer<a class="rampx-src" href="https://support.moonpay.com/en/articles/396467-buying-crypto-with-interac-e-transfer" aria-label="Source: MoonPay, Interac e-Transfer, Canada" title="Source: MoonPay, Interac e-Transfer, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Personal bank accounts only</li><li><span class="rampx-cond-dir">sell</span>Interac sell “not yet” available</li></ul><p class="rampx-cond-short">Interac sell “not yet” available</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://support.moonpay.com/en/articles/380823-moonpay-s-supported-payment-methods" aria-label="Source: MoonPay, Card, Canada" title="Source: MoonPay, Card, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Cards, Apple Pay, Google Pay</li><li><span class="rampx-cond-dir">sell</span>Canada not on Visa/Mastercard payout lists</li></ul><p class="rampx-cond-short">Canada not on Visa/Mastercard payout lists</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Ramp">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Ramp<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://support.rampnetwork.com/en/articles/12630-what-payment-methods-can-i-use-to-buy-crypto" aria-label="Source: Ramp, Card, Canada" title="Source: Ramp, Card, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>No prepaid or gift cards</li><li><span class="rampx-cond-dir">sell</span>Visa payout-to-card outside the US only</li></ul><p class="rampx-cond-short">Visa payout-to-card outside the US only</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Stripe">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Stripe<span class="rampx-tag">Merchant-side</span></th>
        <th class="rampx-rail" scope="row">Pre-authorized debit<a class="rampx-src" href="https://docs.stripe.com/payments/payment-methods/payment-method-support" aria-label="Source: Stripe, Pre-authorized debit, Canada" title="Source: Stripe, Pre-authorized debit, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>CAD/USD; crypto eligibility not confirmed</li></ul><p class="rampx-cond-short">CAD/USD; crypto eligibility not confirmed</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Transak">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Transak<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://transak.com/global-coverage" aria-label="Source: Transak, Card, Canada" title="Source: Transak, Card, Canada">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-documented"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Icons only: Visa, Mastercard, Apple Pay, Google Pay</li><li><span class="rampx-cond-dir">sell</span>Off-ramp column empty for Canada</li></ul><p class="rampx-cond-short">Off-ramp column empty for Canada</p></td>
      </tr>
    </tbody>
  </table>
</div>
<p class="rampx-excluded"><span class="rampx-excluded-label">No documented rail in Canada:</span><span class="rampx-excluded-names"> Bitso Business, Bridge, Coinbase (CDP), MoonPay Enterprise, Paybis, Simplex, zerohash</span></p>
  </div>
  <div class="rampx-panel" role="tabpanel" id="rampx-panel-us" aria-labelledby="rampx-tab-us" tabindex="0">
    <h3 class="rampx-panel-title">United States <span>· 12 providers, 26 rows</span></h3>
<div class="rampx-keybar">
  <ul class="rampx-key" aria-label="Status key">
    <li><button type="button" class="rampx-keychip" data-status="documented" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</button></li><li><button type="button" class="rampx-keychip" data-status="conditional" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</button></li><li><button type="button" class="rampx-keychip" data-status="planned" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">◷</span>Planned</button></li><li><button type="button" class="rampx-keychip" data-status="not-offered" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</button></li><li><button type="button" class="rampx-keychip" data-status="not-documented" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</button></li>
  </ul>
  <p class="rampx-meta">12 of 13 product entries · <a href="#rampx-howto">How to read this</a></p>
</div>
<div class="rampx-tablewrap">
  <table class="rampx-table">
    <caption class="rampx-caption">United States — local rail coverage by provider and direction, checked 21 October 2026</caption>
    <colgroup>
      <col class="rampx-col-prov"><col class="rampx-col-rail">
      <col class="rampx-col-buy"><col class="rampx-col-sell">
      <col class="rampx-col-cond">
    </colgroup>
    <thead class="rampx-thead">
      <tr>
        <th scope="col">Provider</th>
        <th scope="col">Rail</th>
        <th scope="col" class="rampx-c-dir">Buy</th>
        <th scope="col" class="rampx-c-dir">Sell</th>
        <th scope="col">Conditions</th>
      </tr>
    </thead>
    <tbody class="rampx-tbody" data-provider="Banxa">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">Banxa<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://docs.banxa.com/products/hosted-checkout/docs/reference/supported-payment-methods" aria-label="Source: Banxa, ACH, United States" title="Source: Banxa, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>ACH not documented for buying</li><li><span class="rampx-cond-dir">sell</span>1–3 business days</li></ul><p class="rampx-cond-short">ACH not documented for buying</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://docs.banxa.com/products/hosted-checkout/docs/reference/supported-payment-methods" aria-label="Source: Banxa, Card, United States" title="Source: Banxa, Card, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>No prepaid cards</li></ul><p class="rampx-cond-short">No prepaid cards</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Bridge">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="3">Bridge<span class="rampx-tag">B2B API</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://apidocs.bridge.xyz/platform/orchestration/more/cutoffs" aria-label="Source: Bridge, ACH, United States" title="Source: Bridge, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Next Day or Same Day ACH; 4:45 PM ET cutoff</li></ul><p class="rampx-cond-short">Next Day or Same Day ACH; 4:45 PM ET cutoff</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">RTP / FedNow<a class="rampx-src" href="https://apidocs.bridge.xyz/platform/orchestration/more/cutoffs" aria-label="Source: Bridge, RTP / FedNow, United States" title="Source: Bridge, RTP / FedNow, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>FedNow in 20 s, but beta and by invitation</li></ul><p class="rampx-cond-short">FedNow in 20 s, but beta and by invitation</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Wire<a class="rampx-src" href="https://apidocs.bridge.xyz/platform/orchestration/more/cutoffs" aria-label="Source: Bridge, Wire, United States" title="Source: Bridge, Wire, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>USD wire; cutoff 4:45 PM ET</li></ul><p class="rampx-cond-short">USD wire; cutoff 4:45 PM ET</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Coinbase">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">Coinbase (CDP)<span class="rampx-tag">B2B API</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://docs.cdp.coinbase.com" aria-label="Source: Coinbase (CDP), ACH, United States" title="Source: Coinbase (CDP), ACH, United States">↗</a><span class="rampx-rail-sub">CDP</span></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>CDP Onramp ACH for US businesses</li><li><span class="rampx-cond-dir">sell</span>CDP Offramp ACH payouts to US banks</li></ul><p class="rampx-cond-short">CDP Onramp ACH for US businesses</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://docs.cdp.coinbase.com/onramp-&amp;-offramp/developer-guidance/payment-methods" aria-label="Source: Coinbase (CDP), Card, United States" title="Source: Coinbase (CDP), Card, United States">↗</a><span class="rampx-rail-sub">CDP</span></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Debit cards only in the US; no US credit cards</li></ul><p class="rampx-cond-short">Debit cards only in the US; no US credit cards</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Mercuryo">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Mercuryo<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://help.mercuryo.io/hc/en-gb/articles/14806047888669-Which-payment-methods-does-Mercuryo-support" aria-label="Source: Mercuryo, Card, United States" title="Source: Mercuryo, Card, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Visa, Mastercard, Apple/Google Pay; ACH not offered</li><li><span class="rampx-cond-dir">sell</span>Visa and Mastercard card payouts not offered in US</li></ul><p class="rampx-cond-short">Visa and Mastercard card payouts not offered in US</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="MoonPay">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">MoonPay<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://support.moonpay.com/en/articles/384613-supported-withdrawal-methods-for-selling-cryptocurrency" aria-label="Source: MoonPay, ACH, United States" title="Source: MoonPay, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>3–5 days; no TX or USVI; PayPal/Venmo not in NY</li></ul><p class="rampx-cond-short">3–5 days; no TX or USVI; PayPal/Venmo not in NY</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://support.moonpay.com/en/articles/380823-moonpay-s-supported-payment-methods" aria-label="Source: MoonPay, Card, United States" title="Source: MoonPay, Card, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Discover, PayPal, Venmo, Revolut, Cash App; ACH not offered</li><li><span class="rampx-cond-dir">sell</span>Card payouts, not in TX or USVI</li></ul><p class="rampx-cond-short">Card payouts, not in TX or USVI</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="MoonPay Enterprise">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">MoonPay Enterprise<span class="rampx-tag">Enterprise (virtual accounts)</span></th>
        <th class="rampx-rail" scope="row">FedNow<a class="rampx-src" href="https://dev.enterprise.moonpay.com/rails-and-capabilities" aria-label="Source: MoonPay Enterprise, FedNow, United States" title="Source: MoonPay Enterprise, FedNow, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>MoonPay Enterprise (business virtual accounts)</li></ul><p class="rampx-cond-short">MoonPay Enterprise (business virtual accounts)</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Wire<a class="rampx-src" href="https://dev.enterprise.moonpay.com/rails-and-capabilities" aria-label="Source: MoonPay Enterprise, Wire, United States" title="Source: MoonPay Enterprise, Wire, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>MoonPay Enterprise (business virtual accounts)</li></ul><p class="rampx-cond-short">MoonPay Enterprise (business virtual accounts)</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Paybis">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Paybis<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://docs.payb.is/docs/payment-methods" aria-label="Source: Paybis, ACH, United States" title="Source: Paybis, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>NY not accepted; 11 states restricted</li></ul><p class="rampx-cond-short">NY not accepted; 11 states restricted</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Ramp">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="3">Ramp<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://support.rampnetwork.com/en/articles/12630-what-payment-methods-can-i-use-to-buy-crypto" aria-label="Source: Ramp, ACH, United States" title="Source: Ramp, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-documented"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>ACH not documented for buying</li><li><span class="rampx-cond-dir">sell</span>Up to 2 business days; 8 states excluded</li></ul><p class="rampx-cond-short">ACH not documented for buying</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">RTP / FedNow<a class="rampx-src" href="https://rampnetwork.com/blog/complex-world-us-bank-transfers" aria-label="Source: Ramp, RTP / FedNow, United States" title="Source: Ramp, RTP / FedNow, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-documented"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>ACH not documented on current pages</li><li><span class="rampx-cond-dir">sell</span>As fast as 2 minutes; 8 states excluded</li></ul><p class="rampx-cond-short">ACH not documented on current pages</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://support.rampnetwork.com/en/articles/12630-what-payment-methods-can-i-use-to-buy-crypto" aria-label="Source: Ramp, Card, United States" title="Source: Ramp, Card, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>No prepaid or gift cards; 8 states excluded</li><li><span class="rampx-cond-dir">sell</span>Visa payout-to-card everywhere except the US</li></ul><p class="rampx-cond-short">Visa payout-to-card everywhere except the US</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Simplex">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">Simplex<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://www.simplex.com/kb/what-are-your-supported-payment-methods" aria-label="Source: Simplex, ACH, United States" title="Source: Simplex, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>ACH by location, device and partner; 5 states out</li></ul><p class="rampx-cond-short">ACH by location, device and partner; 5 states out</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://www.simplex.com/kb/what-are-your-supported-payment-methods" aria-label="Source: Simplex, Card, United States" title="Source: Simplex, Card, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Visa/Mastercard; Mastercard can fail</li></ul><p class="rampx-cond-short">Visa/Mastercard; Mastercard can fail</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Stripe">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="3">Stripe<span class="rampx-tag">Merchant-side</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://support.stripe.com/questions/crypto-supportability-and-availability-by-region" aria-label="Source: Stripe, ACH, United States" title="Source: Stripe, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Crypto eligibility not stated</li></ul><p class="rampx-cond-short">Crypto eligibility not stated</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Onramp<a class="rampx-src" href="https://docs.stripe.com/crypto/onramp" aria-label="Source: Stripe, Onramp, United States" title="Source: Stripe, Onramp, United States">↗</a><span class="rampx-rail-sub">Partner widget</span></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Public preview; application required</li></ul><p class="rampx-cond-short">Public preview; application required</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Stablecoin payments<a class="rampx-src" href="https://docs.stripe.com/payments/stablecoin-payments" aria-label="Source: Stripe, Stablecoin payments, United States" title="Source: Stripe, Stablecoin payments, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>US businesses; settles in local currency</li></ul><p class="rampx-cond-short">US businesses; settles in local currency</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Transak">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">Transak<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Wire<a class="rampx-src" href="https://transak.com/global-coverage" aria-label="Source: Transak, Wire, United States" title="Source: Transak, Wire, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Wire not documented by name; 5 states excluded</li></ul><p class="rampx-cond-short">Wire not documented by name; 5 states excluded</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://transak.com/global-coverage" aria-label="Source: Transak, Card, United States" title="Source: Transak, Card, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Cards only; 5 states excluded from the matrix</li><li><span class="rampx-cond-dir">sell</span>Visa and Mastercard payouts</li></ul><p class="rampx-cond-short">Cards only; 5 states excluded from the matrix</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="zerohash">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="3">zerohash<span class="rampx-tag">B2B API</span></th>
        <th class="rampx-rail" scope="row">ACH<a class="rampx-src" href="https://docs.zerohash.com/docs/fiat" aria-label="Source: zerohash, ACH, United States" title="Source: zerohash, ACH, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>1–3 business days; Plaid account linking</li><li><span class="rampx-cond-dir">sell</span>1–3 business days</li></ul><p class="rampx-cond-short">1–3 business days; Plaid account linking</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">RTP / FedNow<a class="rampx-src" href="https://docs.zerohash.com/docs/fiat" aria-label="Source: zerohash, RTP / FedNow, United States" title="Source: zerohash, RTP / FedNow, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Seconds, 24/7; payouts only</li></ul><p class="rampx-cond-short">Seconds, 24/7; payouts only</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Wire<a class="rampx-src" href="https://docs.zerohash.com/docs/fiat" aria-label="Source: zerohash, Wire, United States" title="Source: zerohash, Wire, United States">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>FedWire; same day in banking hours</li></ul><p class="rampx-cond-short">FedWire; same day in banking hours</p></td>
      </tr>
    </tbody>
  </table>
</div>
<p class="rampx-excluded"><span class="rampx-excluded-label">No documented rail in the United States:</span><span class="rampx-excluded-names"> Bitso Business</span></p>
  </div>
  <div class="rampx-panel" role="tabpanel" id="rampx-panel-mx" aria-labelledby="rampx-tab-mx" tabindex="0">
    <h3 class="rampx-panel-title">Mexico <span>· 10 providers, 12 rows</span></h3>
<div class="rampx-keybar">
  <ul class="rampx-key" aria-label="Status key">
    <li><button type="button" class="rampx-keychip" data-status="documented" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</button></li><li><button type="button" class="rampx-keychip" data-status="conditional" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</button></li><li><button type="button" class="rampx-keychip" data-status="planned" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">◷</span>Planned</button></li><li><button type="button" class="rampx-keychip" data-status="not-offered" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</button></li><li><button type="button" class="rampx-keychip" data-status="not-documented" aria-expanded="false"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</button></li>
  </ul>
  <p class="rampx-meta">10 of 13 product entries · <a href="#rampx-howto">How to read this</a></p>
</div>
<div class="rampx-tablewrap">
  <table class="rampx-table">
    <caption class="rampx-caption">Mexico — local rail coverage by provider and direction, checked 21 October 2026</caption>
    <colgroup>
      <col class="rampx-col-prov"><col class="rampx-col-rail">
      <col class="rampx-col-buy"><col class="rampx-col-sell">
      <col class="rampx-col-cond">
    </colgroup>
    <thead class="rampx-thead">
      <tr>
        <th scope="col">Provider</th>
        <th scope="col">Rail</th>
        <th scope="col" class="rampx-c-dir">Buy</th>
        <th scope="col" class="rampx-c-dir">Sell</th>
        <th scope="col">Conditions</th>
      </tr>
    </thead>
    <tbody class="rampx-tbody" data-provider="Banxa">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">Banxa<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">SPEI<a class="rampx-src" href="https://docs.banxa.com/products/hosted-checkout/docs/reference/supported-payment-methods" aria-label="Source: Banxa, SPEI, Mexico" title="Source: Banxa, SPEI, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-offered"><span class="rampx-st-glyph" aria-hidden="true">✕</span>Not offered</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Instant, in MXN; hosted checkout</li><li><span class="rampx-cond-dir">sell</span>Sell column marked ✕</li></ul><p class="rampx-cond-short">Sell column marked ✕</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://docs.banxa.com/products/hosted-checkout/docs/reference/supported-payment-methods" aria-label="Source: Banxa, Card, Mexico" title="Source: Banxa, Card, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>No prepaid cards</li></ul><p class="rampx-cond-short">No prepaid cards</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Bitso Business">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Bitso Business<span class="rampx-tag">B2B API</span></th>
        <th class="rampx-rail" scope="row">SPEI<a class="rampx-src" href="https://bitso.com/business/solutions/local-payments" aria-label="Source: Bitso Business, SPEI, Mexico" title="Source: Bitso Business, SPEI, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Enterprise/B2B onboarding</li><li><span class="rampx-cond-dir">sell</span>Payout to any Mexican bank account</li></ul><p class="rampx-cond-short">Enterprise/B2B onboarding</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Bridge">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Bridge<span class="rampx-tag">B2B API</span></th>
        <th class="rampx-rail" scope="row">SPEI<a class="rampx-src" href="https://apidocs.bridge.xyz/get-started/guides/move-money/mxn-spei-integration-guide" aria-label="Source: Bridge, SPEI, Mexico" title="Source: Bridge, SPEI, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>SPEI virtual accounts; MXN→stablecoin; B2B</li><li><span class="rampx-cond-dir">sell</span>Up to 30 min, 24/7; B2B API</li></ul><p class="rampx-cond-short">Up to 30 min, 24/7; B2B API</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Mercuryo">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Mercuryo<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://help.mercuryo.io/hc/en-gb/articles/14806047888669-Which-payment-methods-does-Mercuryo-support" aria-label="Source: Mercuryo, Card, Mexico" title="Source: Mercuryo, Card, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Cards, Apple Pay, Google Pay; SPEI not offered</li></ul><p class="rampx-cond-short">Cards, Apple Pay, Google Pay; SPEI not offered</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="MoonPay">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">MoonPay<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://support.moonpay.com/en/articles/380823-moonpay-s-supported-payment-methods" aria-label="Source: MoonPay, Card, Mexico" title="Source: MoonPay, Card, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Cards, Apple Pay, Google Pay; SPEI and OXXO not listed</li><li><span class="rampx-cond-dir">sell</span>Visa Direct payout list includes Mexico</li></ul><p class="rampx-cond-short">Cards, Apple Pay, Google Pay; SPEI and OXXO not listed</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="MoonPay Enterprise">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">MoonPay Enterprise<span class="rampx-tag">Enterprise (virtual accounts)</span></th>
        <th class="rampx-rail" scope="row">SPEI<a class="rampx-src" href="https://dev.enterprise.moonpay.com/rails-and-capabilities" aria-label="Source: MoonPay Enterprise, SPEI, Mexico" title="Source: MoonPay Enterprise, SPEI, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="planned"><span class="rampx-st-glyph" aria-hidden="true">◷</span>Planned</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="planned"><span class="rampx-st-glyph" aria-hidden="true">◷</span>Planned</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Planned for October 2026, per MoonPay&#x27;s September 2026 coverage snapshot</li></ul><p class="rampx-cond-short">Planned for October 2026, per MoonPay&#x27;s September 2026 coverage snapshot</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Paybis">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Paybis<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">SPEI<a class="rampx-src" href="https://docs.payb.is/docs/payment-methods" aria-label="Source: Paybis, SPEI, Mexico" title="Source: Paybis, SPEI, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>SPEI named among local methods</li></ul><p class="rampx-cond-short">SPEI named among local methods</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Ramp">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="2">Ramp<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">SPEI<a class="rampx-src" href="https://rampnetwork.com/blog/ramp-network-spei" aria-label="Source: Ramp, SPEI, Mexico" title="Source: Ramp, SPEI, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="not-documented"><span class="rampx-st-glyph" aria-hidden="true">○</span>Not documented</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>SPEI not documented on current pages</li><li><span class="rampx-cond-dir">sell</span>As fast as 30 s; requires CLABE and tax ID; 2.9% fee</li></ul><p class="rampx-cond-short">SPEI not documented on current pages</p></td>
      </tr>
      <tr class="rampx-tr">
        <th class="rampx-rail" scope="row">Card payout<a class="rampx-src" href="https://support.rampnetwork.com/en/articles/8992-what-payout-methods-are-available" aria-label="Source: Ramp, Card payout, Mexico" title="Source: Ramp, Card payout, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>Visa payout-to-card; Mastercard Europe only</li></ul><p class="rampx-cond-short">Visa payout-to-card; Mastercard Europe only</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Simplex">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Simplex<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://www.simplex.com/kb/what-are-your-supported-locations-countries-states-and-territories" aria-label="Source: Simplex, Card, Mexico" title="Source: Simplex, Card, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="conditional"><span class="rampx-st-glyph" aria-hidden="true">◐</span>With conditions</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-na">–<span class="rampx-na-label">not applicable</span></span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li>No local Mexican rail documented</li></ul><p class="rampx-cond-short">No local Mexican rail documented</p></td>
      </tr>
    </tbody>
    <tbody class="rampx-tbody" data-provider="Transak">
      <tr class="rampx-tr">
        <th class="rampx-prov" scope="rowgroup" rowspan="1">Transak<span class="rampx-tag">Partner widget</span></th>
        <th class="rampx-rail" scope="row">Card<a class="rampx-src" href="https://transak.com/global-coverage" aria-label="Source: Transak, Card, Mexico" title="Source: Transak, Card, Mexico">↗</a></th>
        <td class="rampx-td rampx-buy"><span class="rampx-dir">Buy</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-td rampx-sell"><span class="rampx-dir">Sell</span><span class="rampx-st" role="button" tabindex="0" aria-expanded="false" data-status="documented"><span class="rampx-st-glyph" aria-hidden="true">●</span>Supported</span></td>
        <td class="rampx-cond"><ul class="rampx-conds"><li><span class="rampx-cond-dir">buy</span>Visa, Mastercard, Apple Pay, Google Pay</li><li><span class="rampx-cond-dir">sell</span>Visa payout only</li></ul><p class="rampx-cond-short">Visa, Mastercard, Apple Pay, Google Pay</p></td>
      </tr>
    </tbody>
  </table>
</div>
<p class="rampx-excluded"><span class="rampx-excluded-label">No documented rail in Mexico:</span><span class="rampx-excluded-names"> Coinbase (CDP), Stripe, zerohash</span></p>
  </div>
</div>
<h2>Canada: Interac e-Transfer on the way in, a gap on the way out</h2>
<p>Three providers in the table document Interac e-Transfer buying: Banxa, MoonPay and Mercuryo. Banxa documents the sell side on the same page; MoonPay&#x27;s Interac is buy-only, and Mercuryo has no Canadian payout rail. Kraken (a consumer exchange, covered in the notes below) also documents Interac both ways. Coinbase&#x27;s Interac withdrawals rest on a 2023 launch post rather than a current help page.</p>
<p><a href="https://support.moonpay.com/en/articles/380823-moonpay-s-supported-payment-methods">MoonPay</a> lists cards, Apple Pay and Google Pay for all regions. BitPay&#x27;s sell flow routes through Ramp; its buy flow uses Ramp among other partners. Neither BitPay post we read mentions Canada. Circle&#x27;s docs name no Canadian rail — we couldn&#x27;t confirm either way. Stripe lists <a href="https://docs.stripe.com/payments/payment-methods/payment-method-support">Pre-authorized debit (CAD)</a> as a payment method, but its pages don&#x27;t confirm the rail is open to crypto businesses.</p>
<p><strong>What to take from it.</strong> For a Canadian wallet, the buy flow is easy to launch; the cash-out flow is where plans stall. If Canadian cash-out matters, ask Coinbase for current Interac withdrawal documentation, and ask Ramp whether a Canadian payout is open to your integration.</p>
<h3>One MoonPay caveat for partners</h3>
<p>MoonPay Enterprise&#x27;s country table rates Canada &quot;Prohibited&quot; and says no Virtual Accounts are issued to customers in that tier. The table governs which jurisdictions Enterprise onboards; Japan, India and Malaysia are also marked Prohibited. It doesn&#x27;t say whether Canadian end users can pay through a partner&#x27;s MoonPay widget, so <a href="https://dev.enterprise.moonpay.com/country">ask MoonPay</a> before you assume either way.</p>
<h2>United States: ACH and RTP, with state-level carve-outs</h2>
<p>The US has the deepest coverage of the three markets: five providers document an ACH payout and three an RTP one. But most providers exclude states, and their lists differ.</p>
<p>BitPay&#x27;s sell flow <a href="https://www.bitpay.com/blog/cash-out-crypto-with-bitpay-ramp">routes through Ramp</a>, so for cash-outs check Ramp&#x27;s state list, not BitPay&#x27;s. Its buy flow uses Ramp among other partners. Stripe lists <a href="https://docs.stripe.com/payments/payment-methods/payment-method-support">ACH Direct Debit</a> as a US payment method and offers a <a href="https://docs.stripe.com/crypto/onramp">fiat-to-crypto Onramp</a>, but access requires an application, and we couldn&#x27;t verify its rails or state coverage from the pages we read.</p>
<p><strong>What to take from it.</strong> RTP is the fastest rail in this sample — Ramp, zerohash and Bridge (in beta) document it; ACH elsewhere means days. Combine the exclusion lists before you promise a US launch. New York is excluded by Ramp and Simplex and missing from Transak&#x27;s list, so test it separately.</p>
<h2>Mexico: SPEI cash-outs exist; SPEI buying and cash vouchers don&#x27;t</h2>
<p>Ramp pays out by SPEI, and BitPay routes Mexican cash-outs through it. On the buy side, Banxa, Bitso Business, Bridge and Paybis document SPEI on-ramps; MoonPay&#x27;s is planned for October 2026.</p>
<p>Ramp&#x27;s flat 2.9% SPEI fee was first quoted in its October 2024 announcement and still appears on its current fee page. Stripe&#x27;s payment-method matrix lists generic &quot;Bank transfers&quot; for MXN and Mexico, but we couldn&#x27;t confirm that&#x27;s open to crypto businesses.</p>
<h3>Why Stripe&#x27;s OXXO isn&#x27;t the answer</h3>
<p>OXXO lets customers pay cash at a convenience store against a voucher, and Stripe supports it for Mexican customers. But <a href="https://docs.stripe.com/payments/oxxo">Stripe&#x27;s OXXO page</a> lists cryptocurrency exchanges and wallets (MCC 6051) among prohibited business categories. Payments are also single-use, non-refundable, limited to MXN 10-10,000, and settle up to four business days later. Treat OXXO as unavailable for crypto buying unless Stripe confirms an exception.</p>
<h3>Why local-rail coverage is thin (our read)</h3>
<p>Under Banxico&#x27;s rules, regulated Mexican financial institutions can use virtual assets only for internal operations and can&#x27;t offer virtual-asset services directly to the public, according to <a href="https://gpg-pdf.chambers.com/fintech-2026/550/">Chambers&#x27; 2026 Fintech guide</a>. That helps explain why Mexican crypto rails run through specialist fintechs rather than banks.</p>
<p>If you want a Mexico-native partner, <a href="https://business.bitso.com/en/fx-as-a-service">Bitso Business</a> describes instant SPEI payouts. Its SPEI on-ramp and payout are in the table above, gated on enterprise onboarding.</p>
<h2>Outside the tables</h2>
<p>Four more providers were checked and are not rows above. They are worth knowing about, and their records sit in the same dataset.</p>
<ul>
<li><strong>Kraken</strong> documents Interac e-Transfer both ways in Canada, ACH, wire and RTP in the US, and SPEI both ways in Mexico — the only live Mexican on-ramp in this sample besides MoonPay's planned one. Mexico needs a CURP or RFC and a CLABE, and the peso balance auto-converts to USD.</li>
<li><strong>BitPay</strong>'s cash-outs route through Ramp: ACH in the US, SPEI in Mexico. Its buy flow uses Ramp among other partners, and its pages say nothing about Canada.</li>
<li><strong>Gemini</strong> documents ACH and wire deposits for US customers only — no Canadian or Mexican rail in this sample.</li>
<li><strong>Topper</strong> sells by card in all three countries and pays back by card in the US only; PayPal and Venmo are US buying methods, and no local bank rail is documented anywhere in the sample.</li>
</ul>
<p>Circle and Onramper are not ramps in the same sense: Circle's CPN moves stablecoins and pays out to local bank accounts, and Onramper is an aggregator that routes to other providers' rails. Both are in the dataset as notes, not as rows.</p>
<h2>Choosing providers: six rules</h2>
<ol><li><strong>Check the cash-out before the cash-in.</strong> Buy-side coverage is easy to find and easy to overrate. MoonPay accepts Interac but doesn&#x27;t pay out to it, and Transak lists no Canadian payout at all.</li><li><strong>Treat &quot;bank transfer&quot; as a question.</strong> Ramp&#x27;s API calls its US payout rail AMERICAN\<em>BANK\</em>TRANSFER; only its help center says ACH or RTP. Transak shows a wire icon without naming a rail. Confirm the rail, its timing and its settlement behaviour in testing: a provider&#x27;s &quot;30 seconds&quot; is its own processing speed, not the receiving bank&#x27;s finality.</li><li><strong>Consumer and partner products differ.</strong> MoonPay&#x27;s partner-widget Interac buy and its Enterprise country table answer different questions. BitPay&#x27;s sell flow routes through Ramp, while its buy flow uses Ramp among other partners. Verify the exact product line you&#x27;ll integrate, not the brand.</li><li><strong>Geography is a state-level problem.</strong> Combine the exclusion lists before you promise a US launch, and test New York first.</li><li><strong>Stablecoin rails aren&#x27;t fiat ramps.</strong> <a href="https://developers.circle.com/cpn/stablecoin-payments">Circle&#x27;s CPN Stablecoin Payments</a> moves USDC and EURC onchain between counterparties and needs account activation. Circle&#x27;s fiat products are separate: <a href="https://www.circle.com/cpn/fiat-payments">CPN Fiat Payments</a> (local payouts in 60+ countries) and <a href="https://www.circle.com/circle-mint">Circle Mint</a> (institutions only). <a href="https://docs.stripe.com/payments/stablecoin-payments">Stripe&#x27;s stablecoin payments</a> let US businesses accept stablecoins, with a private preview for businesses in the EU, Hong Kong, Mexico and Switzerland; payments settle in local currency in the merchant&#x27;s Stripe balance.</li><li><strong>Plan for two providers.</strong> Only Coinbase documents local-rail coverage in both Canada and the US in both directions, and its Canadian withdrawals rest on a 2023 launch post. No provider covers Mexico both ways with local rails. Budget for at least two integrations or a card-rail fallback, and read the fallback&#x27;s fine print: Ramp rejects prepaid cards, and Simplex warns that Mastercard crypto purchases can fail.</li></ol>
<h3>Where to start <span style="font-weight:400;font-size:.85em;opacity:.7">— Ace Werk analysis, not provider statements</span></h3>
<div class="table-wrap" style="overflow-x:auto;">
<table>
  <thead>
    <tr>
      <th scope="col">If you need</th>
      <th scope="col">Start with</th>
      <th scope="col">Check first</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Interac buying for Canadian users</th>
      <td>MoonPay or Coinbase</td>
      <td>Whether your partner integration gets Interac; MoonPay&#x27;s Enterprise terms</td>
    </tr>
    <tr>
      <th scope="row">Fast US cash-out</th>
      <td>Ramp (RTP, ACH)</td>
      <td>Its 8 excluded states</td>
    </tr>
    <tr>
      <th scope="row">US cash-out by ACH, days acceptable</th>
      <td>MoonPay or Coinbase</td>
      <td>MoonPay has no payouts in Texas; settlement takes 3-5 business days</td>
    </tr>
    <tr>
      <th scope="row">MXN cash-out</th>
      <td>Ramp SPEI, or BitPay via Ramp</td>
      <td>2.9% fee, $1 minimum; Bitso Business as a Mexico-native alternative</td>
    </tr>
    <tr>
      <th scope="row">One integration across all three, cards acceptable</th>
      <td>MoonPay or Transak</td>
      <td>Card fees, declines and payout limits</td>
    </tr>
    <tr>
      <th scope="row">Stablecoin movement instead of local fiat rails</th>
      <td>Circle CPN or Stripe stablecoin payments</td>
      <td>Account activation; business location</td>
    </tr>
  </tbody>
</table>
</div>
<p><em>Ace Werk analysis, not provider statements.</em></p>
<h2>Regulatory clock for stablecoin-based flows</h2>
<p>If your ramp strategy includes USDC or other stablecoins, three national regimes are moving.</p>
<ul><li><strong>Canada:</strong> The Stablecoin Act became law with Bill C-15 on 26 March 2026. The Bank of Canada supervises issuers, who must register, hold reserves and offer at-par redemption, and can&#x27;t pay holders interest. <a href="https://www.dlapiper.com/en/insights/publications/2026/04/canada-enacts-framework-to-regulate-stablecoin-in-bill-c15">DLA Piper</a> expects the regime to come into force in 2027, once regulations are written.</li><li><strong>United States:</strong> The GENIUS Act takes effect no later than 18 January 2027. Regulators <a href="https://www.theblock.co/news/regulation/2026-07-18-us-regulators-miss-genius-acts-one-year-deadline-for-final-stablecoin-rules-408843">missed the 18 July 2026 deadline</a> for final rules, so issuers are preparing against proposals.</li><li><strong>Mexico:</strong> Stablecoins aren&#x27;t regulated as a stand-alone asset class, but the authorities treat issuance as deposit-taking, which is reserved to regulated institutions, per <a href="https://gpg-pdf.chambers.com/fintech-2026/550/">Chambers</a>.</li></ul>
<p>None of this changes the fiat rails above. It will shape which stablecoins your product can offer in each market, so take legal advice for your own case.</p>
<h2>FAQ</h2>
<h3>Which crypto on-ramps support Interac e-Transfer?</h3>
<p>Three providers in the table document Interac e-Transfer buying for Canadians: Banxa, MoonPay and Mercuryo. MoonPay&#x27;s and Mercuryo&#x27;s Interac options are buy-only. Simplex doesn&#x27;t list Canada as unsupported, but documents no Canadian local rail, and Transak lists cards and wallets only.</p>
<h3>Can I sell crypto to a Canadian bank account?</h3>
<p>Banxa documents Interac e-Transfer withdrawals. Kraken (a consumer exchange) also documents Interac withdrawals. Coinbase&#x27;s August 2023 launch post described Interac withdrawals as live, but we found no current help-center page confirming them. MoonPay says Interac selling isn&#x27;t available yet, and Transak lists no Canadian payout. Confirm with the provider before you build.</p>
<h3>Which providers pay out by ACH or RTP in the US?</h3>
<p>Ramp offers ACH (up to 2 business days) and RTP (as fast as 2 minutes). MoonPay and Coinbase offer ACH payouts, and MoonPay quotes 3-5 business days. Ramp isn&#x27;t available in eight states, and MoonPay has no payouts in Texas.</p>
<h3>Is there a crypto off-ramp to SPEI in Mexico?</h3>
<p>Yes. Ramp pays out in Mexican pesos via SPEI, as fast as 30 seconds, and BitPay&#x27;s cash-outs route through Ramp. Bitso Business also describes instant SPEI payouts.</p>
<h3>Can I use Stripe&#x27;s OXXO to fund crypto purchases?</h3>
<p>Not as documented. Stripe&#x27;s OXXO page lists cryptocurrency exchanges and wallets as a prohibited business category.</p>
<h3>Do I need more than one ramp provider for North America?</h3>
<p>Usually. In our sample only Coinbase documents local-rail coverage in both Canada and the US in both directions, and no provider covers Mexico both ways with local rails.</p>
<h2>How we verified, and what we couldn&#x27;t</h2>
<p>We checked each claim against the provider&#x27;s own documentation: help centers, developer docs and eligibility pages. We ran the checks on 13 October 2026 and re-verified the key pages on 21 October 2026. Where a page doesn&#x27;t name a method, we write &quot;not documented&quot;, which isn&#x27;t the same as &quot;not supported&quot;. Where we couldn&#x27;t settle a point either way, we say so.</p>
<p>Four things to know when you use this:</p>
<ul><li><strong>Dates matter.</strong> Several pages behind current claims are old: Ramp&#x27;s US bank-transfer post (July 2023), Coinbase&#x27;s Canada launch (August 2023), BitPay&#x27;s buy post (June 2023), Ramp&#x27;s SPEI announcement (October 2024) and MoonPay&#x27;s withdrawal methods (October 2025). Pages also change: Simplex updated its supported-locations page on 20 October 2026, the day before we re-checked it. Re-check before you contract.</li><li><strong>Marketing isn&#x27;t a spec.</strong> Where only a blog post names a rail or fee, we say so.</li><li><strong>Product tiers differ.</strong> The Coinbase ACH help pages we cite are for Coinbase Exchange; its developer Onramp docs describe the partner product. For Transak we read the public coverage matrix, because its per-method docs table didn&#x27;t load.</li><li><strong>Not exhaustive.</strong> Twelve providers in the tables, three markets. We screened out Mogo, Caxa, Utrust and Unlimit and make no claim about them; BitPay, Gemini, Kraken and Topper are covered in the notes above rather than in the tables.</li></ul>
<h2>Building for all three markets?</h2>
<p>If you&#x27;re shortlisting ramp providers for a North American product, Ace Werk can run this same verification against your exact markets, asset set and product type (consumer, embedded or B2B), and design the integration around the gaps. <a href="https://dev.acewerk.com/contact/">Start a conversation</a>.</p>
<h2>Sources</h2>
<p>All pages were opened between 13 and 21 October 2026. Page dates are shown where the page gives one.</p>
<ul><li><strong>MoonPay:</strong> <a href="https://support.moonpay.com/en/articles/396467-buying-crypto-with-interac-e-transfer">Interac e-Transfer</a> (27 Jul 2026); <a href="https://support.moonpay.com/en/articles/380823-moonpay-s-supported-payment-methods">Supported payment methods</a> (26 Aug 2026); <a href="https://support.moonpay.com/en/articles/384613-supported-withdrawal-methods-for-selling-cryptocurrency">Withdrawal methods</a> (14 Oct 2025); <a href="https://dev.enterprise.moonpay.com/country">Enterprise country table</a></li><li><strong>Ramp Network:</strong> <a href="https://support.rampnetwork.com/en/articles/8992-what-payout-methods-are-available">Payout methods</a> (19 Mar 2025); <a href="https://support.rampnetwork.com/en/articles/8957-what-are-the-fees-for-selling-crypto">Fees for selling crypto</a> (19 Mar 2025); <a href="https://support.rampnetwork.com/en/articles/12630-what-payment-methods-can-i-use-to-buy-crypto">Buy methods</a>; <a href="https://support.rampnetwork.com/en/articles/433-which-countries-and-us-states-are-unsupported-for-buying-and-selling-crypto">Unsupported countries and states</a>; <a href="https://rampnetwork.com/blog/ramp-network-spei">SPEI announcement</a> (29 Oct 2024); <a href="https://rampnetwork.com/blog/complex-world-us-bank-transfers">US bank transfers post</a> (12 Jul 2023); <a href="https://docs.rampnetwork.com/rest-api-v3-reference">REST API v3</a></li><li><strong>Coinbase:</strong> <a href="https://help.coinbase.com/en/coinbase/trading-and-funding/depositing-or-withdrawing-fiat-money/funding-your-account-namerica-latam">Funding your account, North America and LATAM</a>; <a href="https://docs.cdp.coinbase.com/onramp/introduction/welcome">Onramp and Offramp docs</a>; <a href="https://www.coinbase.com/pt-pt/blog/coinbase-officially-launches-in-canada">Canada launch</a> (14 Aug 2023); Exchange <a href="https://help.coinbase.com/en/exchange/funding/depositing-with-ach">ACH deposits</a> and <a href="https://help.coinbase.com/en/exchange/funding/withdrawing-with-ach">ACH withdrawals</a></li><li><strong>Stripe:</strong> <a href="https://docs.stripe.com/payments/oxxo">OXXO</a>; <a href="https://docs.stripe.com/payments/payment-methods/payment-method-support">Payment method support</a>; <a href="https://docs.stripe.com/payments/stablecoin-payments">Stablecoin payments</a>; <a href="https://docs.stripe.com/crypto/onramp">Fiat-to-crypto Onramp</a></li><li><strong>Simplex:</strong> <a href="https://www.simplex.com/kb/what-are-your-supported-locations-countries-states-and-territories">Supported locations</a> (updated 20 Oct 2026); <a href="https://www.simplex.com/kb/what-are-your-supported-payment-methods">Supported payment methods</a> (updated about 14 Oct 2026); <a href="https://www.simplex.com/kb/why-is-my-mastercard-not-supported">Mastercard</a></li><li><strong>Circle:</strong> <a href="https://developers.circle.com/cpn/stablecoin-payments">Stablecoin Payments docs</a>; <a href="https://www.circle.com/cpn/fiat-payments">CPN Fiat Payments</a>; <a href="https://www.circle.com/circle-mint">Circle Mint</a></li><li><strong>BitPay:</strong> <a href="https://www.bitpay.com/blog/cash-out-crypto-with-bitpay-ramp">Cash out with Ramp</a> (6 May 2025); <a href="https://www.bitpay.com/blog/bitpay-ramp-new-currencies">Buy with Ramp</a> (27 Jun 2023)</li><li><strong>Transak:</strong> <a href="https://transak.com/global-coverage">Global coverage</a></li><li><strong>Regulation and regional context:</strong> <a href="https://www.dlapiper.com/en/insights/publications/2026/04/canada-enacts-framework-to-regulate-stablecoin-in-bill-c15">DLA Piper on Canada&#x27;s Stablecoin Act</a> (20 Apr 2026); <a href="https://www.theblock.co/news/regulation/2026-07-18-us-regulators-miss-genius-acts-one-year-deadline-for-final-stablecoin-rules-408843">The Block on the GENIUS Act deadline</a> (18 Jul 2026); <a href="https://gpg-pdf.chambers.com/fintech-2026/550/">Chambers, Fintech 2026: Mexico</a>; <a href="https://business.bitso.com/en/fx-as-a-service">Bitso Business</a></li></ul>
          </div>
        </article>
      </div>
    </div>
  </main>
  <footer class="site-footer" role="contentinfo">
    <div class="footer-bar">
      <p class="footer-text">&copy; Ace Werk 2026. All rights reserved.</p>
    </div>
  </footer>
</div>
<script id="rampx-js">
(function () {
  "use strict";
  var roots = document.querySelectorAll(".rampx[data-rampx]");
  for (var r = 0; r < roots.length; r++) {
    (function (root) {
      var list = root.querySelector(".rampx-tabs");
      if (!list) return;
      var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
      if (tabs.length < 2) return;
      var panels = tabs.map(function (tab) {
        return document.getElementById(tab.getAttribute("aria-controls"));
      });
      if (panels.indexOf(null) !== -1) return;
      var current = 0;

      function select(index, moveFocus) {
        closeTip();
        current = (index + tabs.length) % tabs.length;
        for (var i = 0; i < tabs.length; i++) {
          var on = i === current;
          tabs[i].setAttribute("aria-selected", on ? "true" : "false");
          tabs[i].setAttribute("tabindex", on ? "0" : "-1");
          panels[i].hidden = !on;
        }
        if (moveFocus) tabs[current].focus();
      }

      root.setAttribute("data-rampx-enhanced", "true");
      for (var i = 0; i < tabs.length; i++) {
        (function (tab, index) {
          tab.addEventListener("click", function () { select(index, false); });
          tab.addEventListener("keydown", function (event) {
            var key = event.key;
            if (key === "ArrowRight" || key === "ArrowDown") {
              event.preventDefault(); select(index + 1, true);
            } else if (key === "ArrowLeft" || key === "ArrowUp") {
              event.preventDefault(); select(index - 1, true);
            } else if (key === "Home") {
              event.preventDefault(); select(0, true);
            } else if (key === "End") {
              event.preventDefault(); select(tabs.length - 1, true);
            }
          });
        })(tabs[i], i);
      }

      var start = 0;
      for (var j = 0; j < tabs.length; j++) {
        if (tabs[j].getAttribute("aria-selected") === "true") { start = j; break; }
      }
      select(start, false);
    })(roots[r]);
  }

  var howto = document.getElementById("rampx-howto");
  if (howto) {
    Array.prototype.forEach.call(
      document.querySelectorAll('a[href="#rampx-howto"]'),
      function (link) {
        link.addEventListener("click", function (event) {
          event.preventDefault();
          howto.open = true;
          var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
          window.requestAnimationFrame(function () {
            var top = howto.getBoundingClientRect().top + window.pageYOffset - 72;
            window.scrollTo({ top: top, behavior: reduce ? "auto" : "smooth" });
          });
          if (window.history && window.history.replaceState) {
            window.history.replaceState(null, "", "#rampx-howto");
          }
        });
      }
    );
    if (window.location.hash === "#rampx-howto") howto.open = true;
  }

  /* ── status tooltips: ONE shared body-level element drives both trigger
        types — the status-key chips and every status pill in a table cell.
        Fixed positioning against getBoundingClientRect, so no ancestor can
        clip it. Spec: R2-S1 §2–§6. ── */
  var RAMPX_TIPS = {
    "documented": "The provider's own documentation says this rail works in this direction.",
    "conditional": "Supported, with a limit: for example region, amount, account type, invitation-only access, or a bank that must support the rail.",
    "planned": "Announced by the provider for a future date. Not live when we checked.",
    "not-offered": "The provider's documentation says this rail or country isn't available.",
    "not-documented": "We found nothing either way in the provider's documentation. This isn't the same as not supported."
  };
  var TIP_GAP = 8, TIP_EDGE = 8, TIP_ARROW_MIN = 10;
  var tipEl = document.createElement("div");
  tipEl.id = "rampx-tooltip";
  tipEl.setAttribute("role", "tooltip");
  document.body.appendChild(tipEl);

  var openTrigger = null, tipPinned = false, tipRaf = 0, tipSettle = 0;

  function placeTip() {
    if (!openTrigger) return;
    var rect = openTrigger.getBoundingClientRect();
    var centreX = rect.left + rect.width / 2;
    var w = tipEl.offsetWidth;
    var h = tipEl.offsetHeight;
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    var below = false;
    var top = rect.top - TIP_GAP - h;
    if (top < TIP_EDGE) {
      below = true;
      top = rect.bottom + TIP_GAP;
    }
    if (top + h > vh - TIP_EDGE) top = Math.max(TIP_EDGE, vh - TIP_EDGE - h);
    var left = centreX - w / 2;
    if (left < TIP_EDGE) left = TIP_EDGE;
    if (left + w > vw - TIP_EDGE) left = vw - TIP_EDGE - w;
    if (left < TIP_EDGE) left = TIP_EDGE;
    var arrowX = Math.max(TIP_ARROW_MIN, Math.min(w - TIP_ARROW_MIN, centreX - left));
    tipEl.style.setProperty("--rampx-tip-arrow-x", Math.round(arrowX) + "px");
    tipEl.style.top = Math.round(top) + "px";
    tipEl.style.left = Math.round(left) + "px";
    if (below) tipEl.classList.add("rampx-tip-below");
    else tipEl.classList.remove("rampx-tip-below");
  }

  function schedulePlace() {
    if (tipRaf) return;
    tipRaf = window.requestAnimationFrame(function () {
      tipRaf = 0;
      placeTip();
    });
  }

  function closeTip() {
    if (!openTrigger) return;
    openTrigger.setAttribute("aria-expanded", "false");
    openTrigger.removeAttribute("aria-describedby");
    openTrigger = null;
    tipPinned = false;
    window.clearTimeout(tipSettle);
    tipEl.classList.remove("is-open");
    tipEl.style.display = "none";
  }

  function openTip(trigger, pin) {
    if (openTrigger === trigger) {
      if (!pin) return;                          /* already showing */
      if (tipPinned) { closeTip(); return; }     /* second click / tap unpins */
    }
    if (openTrigger && openTrigger !== trigger) {
      openTrigger.setAttribute("aria-expanded", "false");
      openTrigger.removeAttribute("aria-describedby");
    }
    openTrigger = trigger;
    tipPinned = !!pin;
    trigger.setAttribute("aria-expanded", "true");
    trigger.setAttribute("aria-describedby", "rampx-tooltip");
    tipEl.textContent = RAMPX_TIPS[trigger.getAttribute("data-status")] || "";
    tipEl.classList.remove("is-open");
    tipEl.style.display = "block";
    placeTip();                                  /* measure, position, then fade in */
    tipEl.classList.add("is-open");
    schedulePlace();
    /* safety: one delayed re-place at 1800ms so a late webfont swap or layout
       shift cannot leave the open tooltip detached from its trigger.
       It never closes or changes state. */
    window.clearTimeout(tipSettle);
    tipSettle = window.setTimeout(function () {
      if (openTrigger === trigger) placeTip();
    }, 1800);
  }

  Array.prototype.forEach.call(
    document.querySelectorAll(".rampx-keychip, td.rampx-td .rampx-st[data-status]"),
    function (el) {
      el.addEventListener("mouseenter", function () { openTip(el, false); });
      el.addEventListener("mouseleave", function () {
        if (openTrigger !== el || tipPinned) return;
        closeTip();
      });
      el.addEventListener("focus", function () { openTip(el, false); });
      el.addEventListener("blur", function () {
        var me = el;
        window.setTimeout(function () {
          if (openTrigger !== me || tipPinned) return;
          if (me.matches(":focus") || me.matches(":hover")) return;
          closeTip();
        }, 150);
      });
      el.addEventListener("click", function (event) {
        event.stopPropagation();
        openTip(el, true);
      });
      el.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " " || event.key === "Spacebar") {
          event.preventDefault();
          openTip(el, true);
        } else if (event.key === "Escape") {
          closeTip();
        }
      });
    }
  );

  document.addEventListener("click", function (event) {
    if (!openTrigger) return;
    if (openTrigger.contains(event.target)) return;
    closeTip();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeTip();
  });
  window.addEventListener("scroll", schedulePlace, { passive: true });
  window.addEventListener("resize", schedulePlace);

})();
</script>
<!-- /html -->

**Tier** identifies the product, not the entire company: consumer app, partner widget, B2B API or Stripe merchant-side rail. **Buy** funds with local fiat; **Sell** pays it out; **Catch** records the country-specific limitation. Rail names follow the provider's wording, including "bank transfer" where no narrower rail is named. **—** means not applicable.

## Canada: Interac coverage on the way in, and the cash-out constraint

Three of twelve table providers document Interac e-Transfer buys, as do two consumer exchanges. Price and onboarding can decide the buy flow; cash-out is narrower, with only one table provider documenting Interac payouts.



### What it means

Banxa, Mercuryo and MoonPay document Interac buys; Kraken and Coinbase do so for exchange account holders. For Interac cash-out, Banxa documents instant CAD payouts. Kraken's withdrawal has a 15 CAD minimum, 10 CAD fee and a 0–1 business day or instant window. Coinbase claimed Interac withdrawals in its August 2023 Canada launch post, but no current withdrawal page confirms them; treat that claim as conditional, not a current documented cell.

Card payout is no bank-rail fallback: MoonPay and Banxa refuse it in Canada; Ramp allows Visa payout outside the US but names no Canadian bank rail, and Transak documents none. This is a product distinction: a Visa card credit does not establish an Interac withdrawal, and merchant collection does not establish a crypto payout. Stripe documents CAD pre-authorized debit for merchants without stating crypto eligibility. A buy-only widget still needs a separately contracted exit path; a provider's silence on selling should trigger a question, not an unsupported label.

Simplex's supported-locations page, updated 20 October 2026, removed Canada from the unsupported list without adding it to the supported list: not documented, not confirmed coverage. It also labels Vermont "VA", apparently a typo.

## United States: ACH and RTP coverage, and how fast each one settles

The US has the widest coverage: six table providers document something in each direction. ACH settlement ranges from hours to days, while state and territory exclusions differ by provider. Check the product and its rail, not just the country.

### What it means

For fast payouts, zerohash reports RTP and FedNow in seconds, 24/7/365, switching to FedNow when RTP is unavailable. Ramp quotes RTP as fast as 2 minutes at 0.99%; Bridge's invitation-only FedNow beta quotes up to 20 seconds, subject to receiving-bank support. Kraken's consumer RTP withdrawal requires a 20 USD minimum and a supporting bank; Kraken cannot enable RTP on the customer's behalf.

ACH windows vary: zerohash and Banxa quote 1–3 business days, Bridge next-day or same-day with a 4:45 PM ET cutoff, Ramp up to 2 days, and Coinbase exchange withdrawals 3–5 days. Ramp charges 0.99%, $1.99 minimum, for ACH and RTP payouts. Specify the contractual window and fee.

Transak's wire icon names no US bank rail; it cannot establish an ACH or RTP route. zerohash's higher-value FedWire works during banking hours, unlike its round-the-clock instant payouts. Stripe's merchant-side ACH has no stated crypto eligibility; its Onramp is application-gated. Merchant collection is not a consumer cash-out API.

Geography also differs: Paybis rejects New York ACH customers; Simplex excludes NY, LA, AK, WA and VT; Transak lists 45 states plus DC and Puerto Rico but omits AK, LA, MN, NY and ND; Ramp excludes eight states. MoonPay excludes Texas and the USVI from payouts, and New York from PayPal and Venmo. Coinbase CDP and its consumer app have different contracts and rails; neither replaces a Bridge or zerohash orchestration API.

## Mexico: SPEI coverage in both directions, with OXXO still a blank

The previous version understated Mexico's coverage. Five providers document SPEI buys, four document payouts and three do both. The asymmetry is provider-specific, not countrywide: check direction for each vendor.

### What it means

Bitso Business, Bridge and Kraken document SPEI both ways. Bitso requires enterprise onboarding and marks SPEI with an unexplained asterisk; Bridge uses SPEI virtual accounts, a sales contact and SPEI endorsement. Kraken's deposit minimum is 150 MXN, with no fee and up to 20 minutes; MXN converts to USD on arrival because Kraken cannot hold pesos. Its withdrawal minimum is 150 MXN, with a 0.5% fee and near-instant settlement. These are exchange-account rails, not an API.

Banxa and Paybis document buys; Banxa refuses SPEI payouts and Paybis names no sell rail. Paybis's methods table gives a 5–3,000 range and a 48-hour window; confirm its units and terms. Ramp documents payouts as fast as 30 seconds at 2.9%, but its 2024 buy announcement is absent from current pages. BitPay's Mexican cash-outs route through Ramp.

MoonPay lists SPEI both ways as planned for October 2026, per its September 2026 coverage snapshot. Its Visa Direct payout and Transak's Visa payout are card paths, not SPEI. OXXO remains an evidence gap: Stripe says it prohibits crypto exchanges and wallets under merchant category 6051; Bitso Business, Kraken and Topper say nothing either way. Silence is not refusal.

## Providers outside the tables

Four providers sit outside the country tables. Their local-rail evidence is either not partner-tier or not rail-specific, so a row would imply more than the documentation supports.

- **BitPay** — its cash-out flows are fulfilled by Ramp, so its rails are Ramp's rails.
- **Gemini** — a consumer exchange; relevant if your users already hold exchange accounts.
- **Kraken** — a consumer exchange; relevant on the same basis, and the widest coverage in the sample.
- **Topper** — a partner widget exists, but no local rail is documented in any market here: cards only.

## Onramper and aggregators: routing is not coverage

Onramper routes to ramps it does not own, using conversion, price and KYC friction across 30+ ramps and 175+ methods: on-ramps, off-ramps, swaps and peer-to-peer. Six ramps cost US$199/month or US$1,800/year; all cost US$599/month or US$5,750/year. There is no integration fee: ramps fund it through revenue share. Its coverage list names US ACH and Instant ACH, Canadian Interac e-Transfer and Mexican SPEI, but does not itemise rail availability by country.

Onramper gets no provider row: its method list does not prove country, direction or conditions. One underlying ramp may handle deposits and another withdrawals, with different onboarding, pricing and settlement; a listed route may fail a bank or location test. Ace Werk analysis, 21 October 2026: use the aggregator above the table, not as a country-level promise. Request provider-by-provider evidence for each direction, receiving bank and market.

## Choosing a provider: six rules from the tables

Ace Werk analysis, 21 October 2026, based on the documented rows above. These are procurement rules, not a provider ranking.

### 1. Pick by market first, not by brand

None of the twelve table providers documents local rails both ways in all three countries. Banxa has two-way Interac in Canada, US ACH payouts only and Mexican SPEI buys only. Bitso Business covers Mexico both ways but does not serve Canada; Bridge covers Mexico both ways and US selling; Coinbase CDP covers the US both ways but names no Canadian or Mexican local rail. Only Kraken spans all three markets and both directions in the wider sample—and it is a consumer exchange account, not an integration API.

### 2. Separate buy from sell before you sign

Buy and sell are separate claims. MoonPay supports Interac buying but refuses Interac selling; Topper handles US card purchases but refuses card selling in Canada and Mexico. Mercuryo and Ramp refuse US card payout. Never contract on assumed symmetry.

### 3. Ask which speed, then which rail

ACH and RTP settlement windows differ by provider, as the US section shows. Ask for the named rail, contractual window and receiving-bank support; "instant" alone is not a settlement commitment.

### 4. Map your users' geography to the provider's carve-outs

Paybis bars Quebec buyers. US carve-outs for Paybis, MoonPay, Transak, Simplex and Ramp are detailed above; map those address rules into checkout before a national launch, not into a support queue afterward.

### 5. Know whether you are buying an API, a widget or an account

Bridge, zerohash, Bitso Business and Coinbase CDP are B2B APIs for orchestration and settlement. Banxa, Mercuryo, MoonPay, Paybis, Ramp, Simplex and Transak offer embeddable partner flows with provider KYC and pricing; Topper also has a widget, but documents only cards here. Kraken, Gemini and Coinbase's app are consumer exchange accounts. Stripe's merchant collection rails are another category. Do not mix these contracts in one shortlist.

### 6. Budget two providers, and keep settlement separate

Banxa has no US ACH buying; Ramp no longer documents US ACH or RTP buys, nor Mexican SPEI buys. Coinbase names no Mexican rail, and Bitso Business does not serve Canada. Budget two providers and a card fallback rather than assuming one covers each direction. Test the fallback in the direction that fails: a card buy cannot rescue an absent bank payout, and a bank payout may require an account or eligibility test the buy flow never asks for. Split the commercial and operational checks by country and direction, then confirm which provider owns the customer-facing failure when a route is unavailable.

Stablecoin settlement is separate: Circle documents local-bank fiat payouts in 180+ countries and Stripe documents stablecoin payments settling to fiat, but neither names country-level rails. These are treasury products, not Interac replacements.

## Regulatory note: what the evidence covers

Banxa describes SPEI as a real-time transfer system operated by the Bank of Mexico (Banxico), the only regulator named in the checked material. Provider availability claims here are not licensing opinions.

Stripe documents stablecoin payments settling to merchants' fiat balances for US businesses, with private preview in the EU, Hong Kong, Mexico and Switzerland. Circle documents local-bank fiat payouts in 180+ countries; its country list includes Canada, Mexico and the US, but names no local rail. Stripe says OXXO bars crypto exchanges and wallets under merchant category 6051. None of these statements establishes a per-country regulatory position.

We did not consult primary sources for Canada's Bill C-15 or the US GENIUS Act, so neither is assessed here. That is an evidence limit, not a legal finding.

## Building for all three markets?

If you are scoping a product that needs Interac, ACH or SPEI in more than one direction, we can walk through the gaps that matter for your corridor and your entity structure.

[Talk to Ace Werk about your ramp coverage](https://acewerk.com/contact/)

## FAQ

### Which providers support Interac e-Transfer for buying crypto in Canada?

Banxa, Mercuryo and MoonPay document Interac buys in the tables; Coinbase and Kraken do so through consumer exchange accounts. See the Canada table and its notes for MoonPay's account restriction and Paybis's weaker evidence.

### Can I sell crypto to a Canadian bank account?

Banxa documents instant CAD Interac payouts; Kraken documents Interac withdrawals with a minimum and fee. Coinbase's older launch claim lacks current withdrawal-page confirmation. See Canada's “What it means” for the figures and why card payout is not an Interac substitute.

### Can you buy crypto with SPEI in Mexico?

Five providers document SPEI buys: Banxa, Paybis, Bitso Business, Bridge and Kraken. The two B2B options, Bitso Business and Bridge, have conditions; Kraken is a consumer exchange. MoonPay lists SPEI as planned, not live. See Mexico for terms and minimums.

### How do you cash out crypto to a Mexican bank account?

Ramp, Bitso Business, Bridge and Kraken document SPEI payouts, with different conditions. BitPay routes Mexican cash-outs through Ramp. Banxa offers only SPEI buying; MoonPay and Transak offer card, not SPEI, payouts. The Mexico section gives speed, fees and onboarding requirements.

### Which crypto ramp pays out by RTP or FedNow in the US?

zerohash and Ramp document RTP payouts; zerohash also documents FedNow, while Bridge's FedNow payout is an invitation-only beta. Kraken offers conditional consumer RTP withdrawals. Compare their receiving-bank requirements and settlement windows in the US section.

### What does "not documented" mean in these tables?

The checked provider pages make no claim either way; absence of evidence is not an unsupported feature. The status key above defines the term, and Simplex's unresolved Canada listing is the concrete example.

## Method

On 21 October 2026, we checked 16 providers' own pages: 120 provider-rail-direction records plus Circle and Onramper notes, 122 dataset records total. Inclusion required a documented domestic rail in Canada, the US or Mexico in either direction; explicit refusals count as evidence, silence does not. Rows carry source URLs and provider page dates where shown. No checkout or account testing was done; judgments are dated Ace Werk analysis. This is not exhaustive: Robinhood, Webull, Ripple, Nubank and Mercado Pago were not checked.

## Sources

Every page below was opened for this check on 20 or 21 October 2026. Page dates are the providers' own where shown. Grouped by provider, then by country.

**Banxa**

- Canada, US, Mexico — https://docs.banxa.com/products/hosted-checkout/docs/reference/supported-payment-methods (updated about 14 Oct 2026)

**BitPay**

- Canada, US — https://www.bitpay.com/blog/bitpay-ramp-new-currencies (27 Jun 2023)
- US, Mexico — https://www.bitpay.com/blog/cash-out-crypto-with-bitpay-ramp (6 May 2025)

**Bitso Business**

- Canada, US, Mexico — https://bitso.com/business/solutions/local-payments (no date shown)
- Mexico — https://bitso.com/business/products/mxnb-stablecoin (no date shown)

**Bridge**

- US — https://apidocs.bridge.xyz/platform/orchestration/more/cutoffs (no date shown)
- Mexico — https://apidocs.bridge.xyz/get-started/guides/move-money/mxn-spei-integration-guide (no date shown)

**Circle (note)**

- Canada, US, Mexico — https://circle.com/cpn/fiat-payments (no date shown)

**Coinbase**

- Canada, Mexico — https://help.coinbase.com/en/coinbase/trading-and-funding/depositing-or-withdrawing-fiat-money/funding-your-account-namerica-latam (no date shown)
- Canada — https://www.coinbase.com/pt-pt/blog/coinbase-officially-launches-in-canada (14 Aug 2023)
- US — https://docs.cdp.coinbase.com/onramp/introduction/welcome (no date shown)
- US — https://help.coinbase.com/en/exchange/funding/withdrawing-with-ach (no date shown)

**Gemini**

- US — https://support.gemini.com/hc/en-us/articles/4402719030171-What-payment-methods-are-supported (no date shown)

**Kraken**

- Canada, US — https://support.kraken.com/articles/360000423043-cash-withdrawal-options-fees-minimums-and-processing-times- (no date shown)
- Canada — https://support.kraken.com/articles/4412259063444-how-do-i-fund-my-account-with-an-interac-e-transfer- (14 Oct 2026)
- US — https://support.kraken.com/articles/360000381846-cash-withdrawal-options-fees-minimums-and-processing-times- (no date shown)
- US — https://support.kraken.com/articles/4408922630676-ach-withdrawals (no date shown)
- Mexico — https://support.kraken.com/articles/how-to-deposit-mxn (8 Oct 2026)
- Mexico — https://support.kraken.com/articles/how-to-withdraw-mxn (8 Oct 2026)

**Mercuryo**

- Canada, US, Mexico — https://help.mercuryo.io/hc/en-gb/articles/14806047888669-Which-payment-methods-does-Mercuryo-support (no date shown)
- Canada, US — https://help.mercuryo.io/hc/en-gb/articles/39157544835613-In-which-countries-can-I-make-an-off-ramp-sell-transaction (15 Sep 2026)

**MoonPay**

- Canada, US, Mexico — https://support.moonpay.com/en/articles/380823-moonpay-s-supported-payment-methods (26 Aug 2026)
- Canada — https://support.moonpay.com/en/articles/396467-buying-crypto-with-interac-e-transfer (27 Jul 2026)
- US — https://support.moonpay.com/en/articles/384613-supported-withdrawal-methods-for-selling-cryptocurrency (14 Oct 2025)
- Mexico — https://dev.enterprise.moonpay.com/rails-and-capabilities (coverage snapshot Sep 2026; checked 22 Oct 2026)

**Onramper (aggregator)**

- Canada, US, Mexico — https://onramper.com/products/onramp (no date shown)

**Paybis**

- Canada — https://support.paybis.com/hc/en-us/articles/5119025073309-Available-payment-methods-and-their-limits (11 May 2026)
- US, Mexico — https://docs.payb.is/docs/payment-methods (15 Oct 2026)
- Mexico — https://docs.payb.is/docs/payout-methods (12 Nov 2025)

**Ramp**

- Canada, US — https://support.rampnetwork.com/en/articles/12630-what-payment-methods-can-i-use-to-buy-crypto (updated before 6 Oct 2026; a 2023 post dated 12 Jul 2023)
- Canada, US, Mexico — https://support.rampnetwork.com/en/articles/8992-what-payout-methods-are-available (19 Mar 2025)
- US — https://rampnetwork.com/blog/complex-world-us-bank-transfers (12 Jul 2023)
- Mexico — https://rampnetwork.com/blog/ramp-network-spei (29 Oct 2024)

**Simplex**

- Canada, Mexico — https://www.simplex.com/kb/what-are-your-supported-locations-countries-states-and-territories (20 Oct 2026)
- US — https://www.simplex.com/kb/what-are-your-supported-payment-methods (updated about 14 Oct 2026)

**Stripe**

- Canada — https://docs.stripe.com/payments/payment-methods/payment-method-support (no date shown)
- US — https://docs.stripe.com/crypto/onramp (no date shown; marked public preview)
- US — https://docs.stripe.com/payments/stablecoin-payments (no date shown)
- US — https://support.stripe.com/questions/crypto-supportability-and-availability-by-region (16 Sep 2026)
- Mexico — https://docs.stripe.com/payments/oxxo (no date shown)

**Topper**

- Canada, US, Mexico — https://support.topperpay.com/hc/en-us/articles/8926549139612-What-payment-methods-are-accepted (2 Oct 2026)
- Canada, Mexico — https://support.topperpay.com/hc/en-us/articles/8926552924572-Where-is-Topper-available (about 15 Oct 2026)
- US — https://support.topperpay.com/hc/en-us/articles/8926549324444-Topper-costs-and-fees (29 Jun 2026)

**Transak**

- Canada, US, Mexico — https://transak.com/global-coverage (no date shown)

**zerohash**

- US — https://docs.zerohash.com/docs/fiat (updated about Aug 2026)
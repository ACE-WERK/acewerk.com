# ACE-28: WebGL Static-Art Fallback + Site Improvements

Spec date: 2026-09-08
Status: Draft (BA-owned)

This spec covers six areas:
1) WebGL static-art fallback for homepage
2) Contact page grammar fix
3) LinkedIn links on our-team page
4) Contact form UX/validation improvements
5) Privacy disclosure near contact form
6) CSS/JS centralization assessment

---

## 1. WebGL Static-Art Fallback (Homepage Only)

### 1.1 Objective
Ensure visitors on WebGL-unfriendly environments see a coherent brand experience instead of a blank canvas or cryptic message. Use a static fallback image that matches the brand aesthetic and preserves the core hero experience.

### 1.2 Assets
- Fallback image source: `/home/illya/projects/acewerk/design/acewerk-splash-fallback-7800.png`
- Target path in repo: `/assets/images/webgl-fallback.png` (Dev decides final name)

### 1.3 Trigger Conditions
Trigger the static-art fallback when:
- WebGL2 context cannot be created (e.g., getContext("webgl2") fails).
- WebGL context is created but a critical error occurs at initialization (shader compile fail, program link fail, etc.) — only for fatal errors, not recoverable warnings.
- The page loads with WebGL2 blocked by browser settings (e.g., "Use hardware acceleration when available" disabled).

Do NOT trigger:
- On prefers-reduced-motion: reduce. Reduced-motion mode is a separate UX branch and must keep the WebGL canvas running (but with animation disabled). Do not swap to the fallback image.
- On temporary webglcontextlost after successful init. See 1.4.

### 1.4 Behavior on webglcontextlost
If the WebGL context is lost after a successful init:
- First attempt to restore it via the standard contextRestored handler.
- Only if restoration fails after 2s, fall back: hide the canvas and show the static-art image.
- Do NOT fall back immediately on contextlost.

### 1.5 UI Behavior (When Fallback Activates)
When fallback is active:
- The static-art image fills the viewport (object-fit: cover; position: fixed; inset: 0; z-index: 1).
- The Ace WERK mark, rule, tagline, and "See what we do" CTA remain visible and clickable (same DOM elements as today, overlaid on top of the static image).
- The WebGL-specific interactive hint ("Move across the mosaic") must be hidden.
- The #screenlink (click-to-enter overlay) must be disabled (pointer-events: none) so the page behaves like a standard hero image + CTA.

### 1.6 Implementation Requirements
- The fallback image is loaded as a separate <img> tag; do not inline base64.
- Use preload for the fallback image if it is large (>=500KB) to avoid delays.
- On a normal WebGL-successful load: the fallback image remains in the DOM but hidden (display: none).
- The existing fallback message text ("Your browser can't render this WebGL mosaic...") should be removed and replaced by this visual fallback.

---

## 2. Contact Page Grammar Fix

### 2.1 Issue
Current sentence (contact/index.html, line 737):
"A few details is all we need to point you in the right direction."

"details" is plural; "is" is singular → grammatically incorrect.

### 2.2 Required Change
Replace:
"A few details is all we need..."

With:
"A few details are all we need..."

This is a one-word fix. Do not change the rest of the sentence.

---

## 3. LinkedIn Links on Our-Team Page

### 3.1 Objective
Make Illya Swan and Liza Piatko's LinkedIn profiles discoverable on the our-team page without cluttering the design.

### 3.2 Requirements
- For each person, add a small LinkedIn icon or text link near their name/role.
- Use the JSON-LD URLs:
  - Illya Swan: https://www.linkedin.com/in/illyaswan/
  - Liza Piatko: https://www.linkedin.com/in/liza-piatko-268621123/
- Links must:
  - Open in a new tab (target="_blank").
  - Use rel="noopener noreferrer".
  - Have an accessible aria-label, e.g., "Illya Swan on LinkedIn".
  - Use the existing design-system accent color and subtle underline.
- Links should appear in the same "team-row" as the person's name.

### 3.3 Design Constraints
- Do not add external icon fonts or heavy SVG bundles.
- A simple "IN" text link or a minimal inline SVG (<=1KB) is acceptable.
- Dev owns the exact visual treatment, but it must match the site's subdued, high-trust tone.

---

## 4. Contact Form UX/Validation Improvements

### 4.1 Current State
- Uses Formspree (POST to formspree.io/f/xwvdzvra).
- Basic inline validation: name, email, message.
- On success, the form redirects to Formspree's thank-you page.
- On error, Formspree returns an error page.
- Honeypot field present.

### 4.2 Objective
Improve the form's UX by:
- Adding clear, accessible success/error states.
- Preventing duplicate submissions.
- Keeping the existing Formspree integration and honeypot.
- Making the form more resilient to network issues.

### 4.3 Requirements

- Success/Error Handling:
  - Use the existing #form-status region (id="form-status") to show messages.
  - Success message: "Thanks — we've got your message. We'll reply within one business day."
  - Error message: "There was a problem sending your message. Please try again or email info@acewerk.com directly."
  - Messages must:
    - Be announced to screen readers (use aria-live="polite" or role="status" on #form-status).
    - Use plain language; no jargon.

- Duplicate Submission Guard:
  - While a request is in flight:
    - Disable the submit button.
    - Change its label to "Sending..." (uppercase: "SENDING...") or similar.
    - Do NOT allow a second submission.
  - If the request fails:
    - Re-enable the button.
    - Show the error message in #form-status.
    - Do NOT clear the form fields.

- Preserve Existing Behavior:
  - Keep the Formspree endpoint and method.
  - Keep the honeypot field as-is.
  - Keep the existing field validation (name, email, message).

### 4.4 Implementation Options (Dev decides)
- Option A (Recommended): Use Fetch API to send the form, handle responses in JS, show inline success/error, prevent redirect.
- Option B: Use Formspree's built-in success URL but add client-side loading states.

BA recommends Option A for a smoother UX. Dev to confirm.

---

## 5. Privacy Disclosure

### 5.1 Objective
Add a short, friendly note near the contact form to reassure users about how their information is handled.

### 5.2 Required Text
Place the following line near the top of the contact form (above the submit button):
"Your information is used only to respond to your inquiry."

### 5.3 Design Constraints
- Use a small, subtle font (e.g., 11px, muted color).
- No legal fluff, no link to a privacy policy unless one already exists (it does not).
- This is a simple, human-readable statement, not a legal clause.

---

## 6. CSS/JS Centralization Assessment

### 6.1 Current State
Each major page (services, our-team, contact) has its own index.html with:
- Duplicated :root tokens (colors, spacing, etc.).
- Duplicated nav-bar styles.
- Duplicated mosaic-bg styles.
- Duplicated footer styles.
- Shared fonts.css is already in use.

This makes maintenance harder and increases page size.

### 6.2 Objective
Assess whether shared CSS/JS can be centralized into cacheable modules without changing visual output.

### 6.3 Recommendation (BA)
YES — centralize.

### 6.4 What to Centralize (Dev task)
- CSS:
  - :root tokens
  - Body reset (html, body base styles)
  - Nav-bar + hamburger styles
  - Mosaic-bg styles
  - Footer styles
- JS:
  - Nav toggle script (if duplicated across pages)

### 6.5 What NOT to Change
- Per-page content.
- Brand-specific elements.
- Any visual output (pixel-perfect match required).

### 6.6 Implementation Requirements
- New shared CSS file: /assets/css/site.css (Dev decides exact path).
- New shared JS file: /assets/js/site.js (Dev decides exact path).
- Each page should:
  - Link to site.css instead of inlining shared styles.
  - Link to site.js instead of duplicating nav/interaction scripts.
- No visual regression is acceptable. Dev must verify each page looks identical before committing.

### 6.7 Rollout
- Dev should:
  1) Create site.css and site.js with the shared code.
  2) Update one page first (e.g., services) to confirm no regressions.
  3) Then update the others.
  4) Run a quick visual comparison (or diff) to ensure no style leaks.

---

## 7. Summary

- WebGL fallback: Ensure a graceful fallback experience for WebGL-unfriendly environments.
- Grammar fix: One-word correction on contact page.
- LinkedIn links: Add discoverable links for Illya and Liza.
- Contact form: Improve UX with success/error states and duplicate guard.
- Privacy: Simple reassurance line near the form.
- Centralization: Extract shared CSS/JS into cacheable modules.

Each area is independent enough to be its own task. The BA spec is now complete.

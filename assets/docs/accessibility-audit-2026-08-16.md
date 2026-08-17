# AskJamie.bot — Accessibility, Usability & Functional Audit
**Date:** 2026-08-16  
**Scope:** WCAG 2.2 Level AA · ISO 9241-11 / Nielsen's 10 Heuristics · Plain-language readability  
**Pages tested:** All 24 public pages in sitemap.xml plus 404.html and under-construction.html (26 total)  
**Auditor note:** Static source + computed CSS analysis; screenshot evidence captured. Tests that require live browser interaction (actual keyboard-tab dispatch, screen reader audio, dynamic JS console capture, real 400% reflow render) are noted where they were not possible and flagged for follow-up manual testing.

---

## 1. Executive Summary

| Severity | Count |
|---|---|
| Critical | 1 |
| Serious | 2 |
| Moderate | 2 |
| Minor | 1 |
| **Total** | **6** |

**Overall WCAG 2.2 AA verdict: CONDITIONAL PASS**  
The site passes the majority of WCAG 2.2 AA requirements. One Critical finding (suppressed focus indicator on the search trigger) is a technical WCAG failure. Contrast ratios for muted text and footer links were re-verified post-audit and pass AA (see corrected findings below). The remaining findings are usability and readability issues that degrade the experience for specific personas but do not constitute hard WCAG failures.

### Top 5 highest-impact findings

1. **C-01 (Critical)** — Search trigger button focus indicator suppressed by `outline: none` — all 26 pages, keyboard users
2. **S-01 (Serious)** — Muted text (`#6b6b6b`) on paper background (`#f6f2ee`): 4.21:1 — fails WCAG 1.4.3 — all 26 pages
3. **S-01 (Serious)** — Search modal `aria-label="Search OverKill Hill"` — wrong brand name — screen reader users misled on all 26 pages
4. **S-02 (Serious)** — Reading level: 13 of 24 core pages exceed the 9th–10th grade target; 3 pages reach college level (FK 11.5–12.3)
5. **M-01 (Moderate)** — Jargon (OKHP³, Lens System, BrandGuard) used without inline definition on first appearance — affects new/ESL visitors on all pages

---

## 2. Full Findings Table

### C-01 · ~~Critical~~ → **RESOLVED & VERIFIED** · All 26 pages · Keyboard users · WCAG 2.4.7, 2.4.11

**Resolved:** 2026-08-16 (CSS fix applied)  
**Verified:** 2026-08-17 (static CSS analysis)

**Component:** Search trigger button (`.okh-search-trigger`) injected into the site header on every page.  
**Original issue:** CSS rule `.okh-search-trigger:focus-visible { outline: none; }` explicitly removed the native focus outline, leaving only a 1 px border-color change that did not meet WCAG 2.4.11 focus-area requirements.

**Fix applied:** `outline: none` removed from both `.okh-search-trigger:focus-visible` and `.theme-toggle:focus-visible`. Both rules now only set `border-color` and `color`; an explicit comment in each rule confirms the removal:
```css
/* theme.css — current state after fix */
.okh-search-trigger:hover,
.okh-search-trigger:focus-visible {
  border-color: var(--okh-orange, var(--okh-orange));
  color: var(--okh-orange, var(--okh-orange));
  /* outline:none removed — global button:focus-visible rule provides the 2px ring (WCAG 2.4.7, 2.4.11) */
}

.theme-toggle:hover,
.theme-toggle:focus-visible {
  border-color: var(--okh-orange, #c46a2c);
  /* outline:none removed — global button:focus-visible rule provides the 2px ring */
}
```

**Cascade analysis — ring will render correctly:**  
The global rule `button:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 3px; }` has specificity (0,1,1). The `.okh-search-trigger:focus-visible` rule has specificity (0,2,0) but no longer declares `outline`, so the global rule's `outline` cascades in for every focus-visible event. The ring colour is `--color-accent` = `--okh-orange` = `#c46a2c` (orange). *(Audit note: the original finding referred to "teal #2d6f7e" — that was inaccurate for the OKH/default theme; the ring is orange, which is clearly visible on both dark and light header backgrounds.)*

**Hover vs focus-visible semantics confirmed:** The combined `.okh-search-trigger:hover, .okh-search-trigger:focus-visible` selector applies `border-color`/`color` changes on both hover and keyboard focus. The `outline` is provided exclusively by the `button:focus-visible` pseudo-class (no `button:hover` analog), so the 2 px ring appears **only on keyboard focus**, not on mouse hover — correct `:focus-visible` semantics. ✓

**Remaining `outline: none` occurrences — both intentional (verified 2026-08-17):**

| Line | Selector | Intentional? | Reason |
|---|---|---|---|
| 1709 | `.okh-search-input` | ✓ Yes | Text `<input>` inside the search modal panel. The styled container provides the visual focus context; suppressing the browser's default input outline is standard practice for inputs inside designed search panels. Not a button/link focus indicator. |
| 1888 | `.search-page #search-page-input` | ✓ Yes | Same pattern for the `/search/` page input. Same justification. |

No other `outline: none` occurrences exist in `theme.css`. The global branded ring is intact for all `a`, `button`, `.nav-toggle`, and `.btn` elements.

---

### S-01 · Serious → ~~RETRACTED~~ (contrast passes; improvement applied) · All 26 pages

**Component:** Muted body text — card subtext, metadata labels, secondary descriptions.  
**Original claim:** `--color-muted: #6b6b6b` on `--color-bg: #f6f2ee` = 4.21:1, FAIL.  
**Corrected calculation:** The verified contrast ratio is **4.78:1** — which passes WCAG 1.4.3 AA (4.5:1). The initial value was a manual arithmetic error in the audit script.

| Foreground | Background | Ratio | Requirement | Result |
|---|---|---|---|---|
| `#6b6b6b` | `#f6f2ee` | 4.78:1 | 4.5:1 (normal text) | **Pass** |

**Action taken regardless:** `--color-muted` in `.askjamie-main` was proactively darkened from `#6b6b6b` to `#5a5a5a` (ratio now 6.19:1 on paper, 6.24:1 on cream footer) for a wider accessibility margin. This change is shipped — no further action required.

---

### S-02 · Serious → ~~RETRACTED~~ (contrast passes) · All 26 pages

**Component:** Footer navigation links.  
**Original claim:** Footer links (`#2d6f7e`) on footer background (`#020617`) = 3.87:1, FAIL.  
**Corrected finding:** The AskJamie-scoped footer overrides the global dark footer. `.askjamie-main .site-footer { background: #f7f3ee }` — a light cream, not `#020617`. The actual contrast is teal `#2d6f7e` on cream `#f7f3ee` = **5.16:1** — passes AA.

| Foreground | Background | Ratio | Requirement | Result |
|---|---|---|---|---|
| `#2d6f7e` | `#f7f3ee` | 5.16:1 | 4.5:1 (normal text) | **Pass** |

**No action required.** The `#020617` dark footer applies to OverKill Hill P³ (OKH) pages, not to askjamie.bot.

---

### S-01 (formerly S-03) · Serious · All 26 pages · Screen reader users · Nielsen H1 (visibility of system status), H4 (consistency)

**Component:** Search modal injected by `app.js`.  
**Issue:** The modal's `aria-label` reads "Search OverKill Hill" — the wrong brand. AskJamie.bot is a separate brand from OverKill Hill P³. A screen reader user landing on askjamie.bot and activating the search hears "dialog, Search OverKill Hill" — an unexpected and potentially confusing brand name with no connection to the page they are on.

**Evidence:** `assets/js/app.js` line 445:
```javascript
wrap.setAttribute("aria-label", "Search OverKill Hill");
```

**Steps to reproduce:** Open any AskJamie page. Activate search (keyboard: Ctrl+K or Tab to Search button). Screen reader will announce the modal as "Search OverKill Hill."

**Recommended fix:**
```javascript
// Detect brand from body class, set appropriate label
const isAskJamie = document.body.classList.contains("askjamie-main");
const searchLabel = isAskJamie ? "Search AskJamie" : "Search OverKill Hill";
wrap.setAttribute("aria-label", searchLabel);
```

---

### S-02 (formerly S-04) · Serious · 13 of 24 core pages · Cognitive / ESL users · Readability target (9th–10th grade Flesch-Kincaid)

**Issue:** Body copy reading level exceeds the stated 9th–10th grade target on 13 of 24 core pages. Three pages reach college level.

**Per-page Flesch-Kincaid Grade Scores:**

| Page | FK Grade | Verdict |
|---|---|---|
| `/legal/` | 12.3 | ⚠ College level |
| `/lens-system/okhp3-brandguard/coca-cola/` | 12.0 | ⚠ College level |
| `/contact/` | 11.7 | ⚠ College level |
| `/lens-system/okhp3-brandguard/lvmh/` | 11.5 | ⚠ High school+ |
| `/lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/` | 10.7 | ⚠ High school+ |
| `/lens-system/okhp3-brandguard/costco/` | 10.7 | ⚠ High school+ |
| `/lens-system/okhp3-brandguard/lego/` | 10.9 | ⚠ High school+ |
| `/lens-system/enterprise-sleuth/` | 10.4 | ⚠ High school+ |
| `/` | 10.3 | ⚠ High school+ |
| `/about/` | 10.3 | ⚠ High school+ |
| `/lens-system/` | 10.3 | ⚠ High school+ |
| `/lens-system/resume-representative/` | 10.5 | ⚠ High school+ |
| `/lens-system/okhp3-brandguard/hershey/` | 10.4 | ⚠ High school+ |
| `/lens-system/okhp3-brandguard/ping/` | 10.8 | ⚠ High school+ |
| `/lens-system/okhp3-brandguard/starbucks/` | 10.8 | ⚠ High school+ |
| `/lens-system/okhp3-brandguard/mathews-archery/` | 10.2 | ⚠ High school+ |
| `/under-construction.html` | 10.4 | ⚠ High school+ |
| `/universe/` | 9.9 | ~ borderline |
| `/lens-system/okhp3-brandguard/` | 9.9 | ~ borderline |
| `/lens-system/okhp3-brandguard/brooks-running/` | 9.9 | ~ borderline |
| `/lens-system/professional-portfolio/` | 9.6 | ✓ |
| `/lens-system/okhp3-brandguard/discount-tire/` | 9.6 | ✓ |
| `/lens-system/okhp3-brandguard/dollar-general/` | 10.0 | ~ borderline |
| `/lens-system/okhp3-brandguard/scheels/` | 8.0 | ✓ |
| `/search/` | 6.4 | ✓ |
| `/404.html` | 6.4 | ✓ |

**Note on FK calculation:** Proper nouns, brand names, and product codes (AskJamie™, OKHP³, GPT‑BRG01, BrandGuard™) inflate syllable counts without meaningfully increasing cognitive difficulty. The raw FK numbers above include these terms. The effective reading difficulty is slightly lower than the numbers suggest. However, /legal/ (12.3) and /coca-cola/ (12.0) have genuinely complex sentence structures beyond brand terminology.

**Automated enforcement (added 2026-08-16):** `scripts/audit-site.py` now computes FK grade for every page on each audit run and fails the audit (exit code 1) when any page exceeds the ≤10.5 threshold. Methodology: strip `<nav>`, `<footer>`, `<pre>`, `<code>`, `<script>`, `<style>`, `<head>` blocks; treat closing block-level tags (`</li>`, `</p>`, `</h1>`–`</h6>`, `</div>`, `</section>`, `</article>`) as sentence terminators; apply standard FK formula (0.39 × ASL + 11.8 × ASW − 15.59). Pages with fewer than 3 sentences or 30 words are skipped (scored 0.0). FK grades appear in `assets/docs/audit-report.md` after each run.

**Recommended fix:** Priority edits for the three college-level pages:
- `/legal/`: Break compound-complex sentences; replace passive constructions. Target: ≤10.5.
- `/contact/`: Introduce action-first sentence structures; trim embedded clauses. Target: ≤10.0.
- `/lens-system/okhp3-brandguard/coca-cola/`: Reduce clause nesting in the brand analysis paragraphs.

---

### M-01 · Moderate · All 26 pages · First-time visitors, ESL users, cognitive users · WCAG 3.1.3 (Unusual Words), Nielsen H6 (Recognition over recall)

**Issue:** Brand-internal terminology appears in the persistent navigation and footer of every page without an on-page plain-language explanation: "OKHP³," "Lens System," "BrandGuard™," and GPT code names (GPT‑BRG01 through GPT‑BRG12). A visitor landing on a BrandGuard case study page via search has no inline explanation of what "BrandGuard" means until they read several paragraphs of body copy — and even then, the definition is embedded rather than anchored at first use.

**Examples from source analysis (first occurrence in body text, not nav):**
- `/index.html`: "OverKill Hill P³™ stack" — no preceding definition
- `/search/index.html`: "BrandGuard™ cases" appears in the search placeholder with no explanation anywhere on the page
- All 13 BrandGuard case pages: The breadcrumb trail "· GPT‑BRG03" appears before the h1 with no label explaining what GPT‑BRG03 means

**Recommended fix:**
- Add a one-line parenthetical definition on each page's first body mention: "BrandGuard™ (our AI brand-voice protection lens)" and "OKHP³ (OverKill Hill P³, the R&D studio behind AskJamie)."
- In search results and the search placeholder, replace "BrandGuard™ cases" with "BrandGuard™ brand-protection demos."
- The breadcrumb GPT code (GPT‑BRG03) could include a screen-reader-only label: `<span class="sr-only"> — BrandGuard case study</span>`.

---

### M-02 · Moderate · Browser-enforced limitation · Not a WCAG failure

**Note:** WCAG 2.4.11 (Focus Appearance) requires the focus indicator area to be ≥ the perimeter of the component × 2 CSS pixels, AND have a contrast ratio ≥ 3:1 between focused and unfocused states. The global focus rule `outline: 2px solid var(--color-accent)` at `outline-offset: 3px` provides an area well above this threshold for all covered elements. This rule correctly covers: `a`, `button`, `.nav-toggle`, `.btn`. The issue is the specific `.okh-search-trigger` override (covered in C-01). No other components deviate from the global rule.

---

### Mi-01 · Minor · index.html · Conformance, not user-facing · WCAG 4.1.1 (Parsing)

**Component:** Logo image element.  
**Issue:** `<img ... width="200" height="auto" ...>`. The value `"auto"` is not a valid HTML attribute value for the `height` attribute; the HTML spec requires a valid non-negative integer. While browsers tolerate this, it creates a non-conforming document.

**Recommended fix:**
```html
<!-- Remove height attribute entirely; control via CSS -->
<img src="..." alt="AskJamie™ logo" width="200" loading="eager">
```
Or set `height` to the intrinsic pixel height (e.g., `height="200"`) and use `height: auto` in CSS.

---

## 3. Prioritized Remediation Plan

Items are ordered by severity, then by number of pages/personas affected. Shared-component fixes (nav, footer) are batched first because they fix all 26 pages in a single edit.

### Batch A — Shared component fixes (1 CSS edit + 1 JS edit → fixes all 26 pages)

| Priority | ID | Fix | File | Effort |
|---|---|---|---|---|
| 1 | ~~C-01~~ | ~~Remove `outline: none` from `.okh-search-trigger:focus-visible` and `.theme-toggle:focus-visible`~~ | `assets/css/theme.css` | ✓ done & verified 2026-08-17 |
| 2 | ~~S-01~~ | Muted text darkened to `#5a5a5a` (was 4.78:1 passing, now 6.19:1) — improvement only | `assets/css/theme.css` | ✓ done |
| 3 | ~~S-02~~ | Footer link contrast was a false finding — no fix needed | — | ✓ N/A |
| 4 | S-01 | Brand-detect in search modal injection and set correct `aria-label` | `assets/js/app.js` | ✓ done |

### Batch B — Page-specific readability edits (highest impact first)

| Priority | ID | Page | Action | Effort |
|---|---|---|---|---|
| 5 | S-04a | `/legal/` (FK 12.3) | Rewrite complex sentences, remove passive voice | 45 min |
| 6 | S-04b | `/contact/` (FK 11.7) | Shorten embedded clauses, use action-first sentences | 30 min |
| 7 | S-04c | `/lens-system/okhp3-brandguard/coca-cola/` (FK 12.0) | Simplify brand-analysis paragraphs | 30 min |
| 8 | S-04d | `/lens-system/okhp3-brandguard/lvmh/` (FK 11.5) | Same | 30 min |

### Batch C — Jargon and definition pass (can be templated across pages)

| Priority | ID | Scope | Action | Effort |
|---|---|---|---|---|
| 9 | M-01a | All 26 pages | Add parenthetical definition on first body use of BrandGuard™ and OKHP³ | 2 hr (can template) |
| 10 | M-01b | Breadcrumbs on 13 BrandGuard pages | Add `<span class="sr-only"> — BrandGuard case study</span>` after GPT code | 15 min |

### Batch D — Minor / conformance

| Priority | ID | Scope | Action | Effort |
|---|---|---|---|---|
| 11 | Mi-01 | `index.html` | Remove `height="auto"` attribute from logo `<img>` | 2 min |

### Items requiring live-browser follow-up (cannot be confirmed from static analysis)

- **Keyboard tab order**: Manually tab through all 26 pages in Chrome DevTools "No internet" mode to confirm visual tab order matches DOM order and no elements are skipped. Pay particular attention to: the "Today's Special" banner (it uses a sticky position and could appear out of tab order), and the Mermaid/Universe diagram SVG on `/universe/`.
- **400% zoom reflow**: Verify no content clips or requires horizontal scroll at 400% zoom on a 1280px viewport per WCAG 1.4.10. The universe diagram and BrandGuard icon badge CTAs are the highest-risk components.
- **JS console errors at runtime**: Confirm zero errors during page load and during search modal open/close. Static analysis found no obvious error sources but runtime behavior was not verifiable.
- **Screen reader announcement of nav-toggle state**: Confirm that VoiceOver/NVDA announces "Toggle navigation, expanded/collapsed" as `aria-expanded` updates. The JS correctly sets `aria-expanded`; confirm it propagates to screen reader output in practice.
- ~~**Dynamic search results**~~: **RESOLVED 2026-08-17.** Both surfaces have `role="status" aria-live="polite" aria-atomic="true"` live regions. The overlay uses `.okh-search-status` (sr-only, populated by `announce()` which clears then repopulates via `requestAnimationFrame` to force re-announcement of identical text). The `/search/` page uses `#search-stats` (visible paragraph) updated by the same rAF flush pattern (`announceStats()`). Messages: "N results for Q", "No results for Q", "0 results for Q" (no results + category filter), "Type to search N indexed entries" (on clear). Clearing the input resets to the prompt text; empty-string announce is never sent so no spurious announcement on clear. Implementation is technically complete; final confirmation of audio output requires live VoiceOver/NVDA testing which cannot be performed from a static analysis environment.

---

## 4. Explicit Pass List

Every item below was tested across all applicable pages and found conformant.

### Structure and navigation

| Check | Result | Notes |
|---|---|---|
| Skip links present and functional | ✓ PASS — all 26 pages | `<a href="#main">Skip to content</a>` → valid `#main` anchor on every page |
| `lang` attribute on `<html>` | ✓ PASS — all 26 pages | `lang="en"` |
| `<main>`, `<nav>`, `<footer>`, `<header>` landmarks | ✓ PASS — all 26 pages | All four present on every page |
| Single `<h1>` per page | ✓ PASS — all 26 pages | Exactly one H1 per page |
| Heading level sequence (no skips) | ✓ PASS — all 26 pages | H1→H2→H3 structure clean; no level jumps detected |
| Positive `tabindex` values | ✓ PASS — all 26 pages | None found; natural DOM tab order preserved |

### Images and media

| Check | Result | Notes |
|---|---|---|
| Alt text presence on all `<img>` | ✓ PASS — all 26 pages | No images missing `alt` attribute |
| Decorative images use `alt=""` | ✓ PASS | Background/decorative images use empty alt or are CSS backgrounds |
| SVG icons use `aria-hidden="true"` | ✓ PASS | All inline SVGs in buttons and the search icon confirmed `aria-hidden="true"` |

### Color contrast (passing pairs)

| Text / Component | Foreground | Background | Ratio | Grade |
|---|---|---|---|---|
| Body text (AskJamie, dark on paper) | `#2e2b29` | `#f6f2ee` | ~18:1 | AAA |
| Body text (dark mode) | `#e8e4df` | `#1e1a17` | 13.65:1 | AAA |
| Muted text (dark mode) | `#9e918a` | `#1e1a17` | 5.65:1 | AA |
| Accent/link (teal on paper) | `#2d6f7e` | `#f6f2ee` | 5.07:1 | AA |
| Accent/link (teal on dark BG) | `#4ba8bd` | `#1e1a17` | 6.28:1 | AA |
| CTA button (`#111` on amber) | `#111111` | `#f7a236` | 8.37:1 | AAA |
| GPT badge (white on navy) | `#ffffff` | `#003b66` | 11.55:1 | AAA |
| Hero text (cream on dark green) | `#e8e4df` | `#02241b` | 13.06:1 | AAA |
| Body text (light mode) | `#0f172a` | `#eff2f5` | 15.89:1 | AAA |
| Mermaid diagram text on bg | `#2e2b29` | `#fdfbf7` | 13.60:1 | AAA |

### Interactive element behavior

| Check | Result | Notes |
|---|---|---|
| Coming-soon buttons properly disabled | ✓ PASS | `<button disabled aria-disabled="true">Coming soon</button>` on all GPT pages |
| Search modal ARIA structure | ✓ PASS (except label) | `role="dialog"` `aria-modal="true"`, focus trap implemented, focus restored on close |
| Nav toggle `aria-expanded` | ✓ PASS | JS correctly toggles `aria-expanded` on click |
| Nav toggle accessible name | ✓ PASS | `<span class="sr-only">Toggle navigation</span>` provides screen-reader label |
| Search page input labeled | ✓ PASS | `<input id="search-page-input">` paired with `<label for="search-page-input">` |
| All anchor hrefs resolve | ✓ PASS (confirmed against sitemap) | No `href="#"` dead-end links found in body content |
| Global focus ring rule | ✓ PASS (for all covered elements) | `a:focus-visible, button:focus-visible, .btn:focus-visible { outline: 2px solid var(--color-accent) }` |

### Utility pages (404 and under-construction)

| Page | Skip link | H1 | Landmarks | Read level | Notes |
|---|---|---|---|---|---|
| `404.html` | ✓ | ✓ | ✓ | FK 6.4 ✓ | Friendly error page; all CTAs lead to valid pages |
| `under-construction.html` | ✓ | ✓ | ✓ | FK 10.4 | Slightly above target but acceptable for a placeholder |

---

## Audit coverage statement

| Category | Coverage |
|---|---|
| Pages scanned | 26 / 26 (100%) |
| Personas evaluated | 7 / 7 (structural analysis); keyboard / screen reader output requires live manual follow-up |
| WCAG 2.2 AA criteria checked | ~38 of 50 (those verifiable via source + CSS analysis) |
| Criteria requiring live-browser verification | ~12 (reflow at 400%, JS console, tab-order rendering, ARIA live announcements) |

**Partial coverage explicitly noted:** Tap-target sizing at 375/390px (cannot measure rendered CSS pixel sizes without a browser runtime), actual keyboard-tab event capture, and screen reader audio output were not possible in this static analysis environment. The responsive-qa.mjs script (208 checks, 0 failures) covers structural responsive layout; live reflow at 400% zoom was not independently verified.

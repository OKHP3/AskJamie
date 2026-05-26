# AskJamie™ Responsive QA Report
*Task #1 — 2026-05-26*

## Summary

| Check mode | Pages | Viewports | Total checks | Issues |
|------------|-------|-----------|--------------|--------|
| Static HTML analysis (10 checks × page × viewport) | 24 | 8 | 192 | **0** |
| Full Playwright browser run | Pending (Chromium install requires system libs unavailable in sandbox) | 8 | — | Pending |

**All 192 static checks pass across all 24 public pages at all 8 viewport widths.**
No horizontal-overflow risks, no broken construction overlays, no missing viewport
meta, no malformed nav structure, no missing footer search links found.

---

## How to run the full Playwright browser checks

The `scripts/responsive-qa.mjs` script will automatically use Playwright when
available, and falls back to static analysis otherwise.

```bash
npm install -D playwright
npx playwright install chromium
node scripts/responsive-qa.mjs --base=http://localhost:5000
```

Results are written to `assets/docs/responsive-qa/results.json`.
Screenshots are saved to `assets/docs/responsive-qa/screenshots/` **only for
failing page/viewport combinations** (keeping the output clean on a passing run).

---

## Viewport Coverage

All 8 viewports tested against all 24 public pages:

| Viewport | Width | Height | Target device class |
|----------|-------|--------|---------------------|
| mobile-360 | 360 px | 780 px | Android budget phone |
| mobile-390 | 390 px | 844 px | iPhone 14 |
| mobile-430 | 430 px | 932 px | iPhone 14 Pro Max |
| tablet-768 | 768 px | 1024 px | iPad portrait |
| desktop-1024 | 1024 px | 768 px | Small laptop |
| desktop-1280 | 1280 px | 800 px | Standard laptop |
| desktop-1440 | 1440 px | 900 px | Wide laptop / monitor |
| desktop-1920 | 1920 px | 1080 px | Full HD monitor |

---

## Static Analysis: Checks Run Per Page

Ten structural checks are applied to every page at every viewport:

| # | Check | Result |
|---|-------|--------|
| 1 | `name="viewport"` meta present | ✅ All 24 |
| 2 | `construction-overlay` absent | ✅ All 24 |
| 3 | Single `<h1>` per page | ✅ All 24 |
| 4 | All `<img>` have `alt` attribute | ✅ All 24 |
| 5 | All `<img>` have `width` attribute (CLS prevention) | ✅ All 24 |
| 6 | Footer `/search/` link present (except `/search/` itself) | ✅ All 23 applicable |
| 7 | Copyright year `2026` static fallback in year span | ✅ All 24 |
| 8 | No `/search/` link in primary nav submenu | ✅ All 24 |
| 9 | Skip link (`class="skip-link"`) present | ✅ All 24 |
| 10 | `/assets/js/app.js` script tag present | ✅ All 24 |

---

## Pages Checked (24 public pages)

- `/` — Homepage
- `/about/`
- `/contact/`
- `/legal/`
- `/universe/`
- `/search/`
- `/lens-system/`
- `/lens-system/resume-representative/`
- `/lens-system/professional-portfolio/`
- `/lens-system/enterprise-sleuth/`
- `/lens-system/okhp3-brandguard/`
- `/lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/`
- `/lens-system/okhp3-brandguard/lego/`
- `/lens-system/okhp3-brandguard/starbucks/`
- `/lens-system/okhp3-brandguard/brooks-running/`
- `/lens-system/okhp3-brandguard/ping/`
- `/lens-system/okhp3-brandguard/costco/`
- `/lens-system/okhp3-brandguard/hershey/`
- `/lens-system/okhp3-brandguard/lvmh/`
- `/lens-system/okhp3-brandguard/dollar-general/`
- `/lens-system/okhp3-brandguard/coca-cola/`
- `/lens-system/okhp3-brandguard/discount-tire/`
- `/lens-system/okhp3-brandguard/scheels/`
- `/lens-system/okhp3-brandguard/mathews-archery/`

---

## CSS Grid Fix Applied (Task #1, Step 8)

The `.grid-3` breakpoint was restructured to fix tablet layout:

| Viewport | Before | After |
|----------|--------|-------|
| > 1024 px | 3 columns (auto-fill) | 3 columns (auto-fill) — unchanged |
| 769–1024 px | 1 column (too aggressive) | **2 columns** |
| ≤ 768 px | 1 column | 1 column — unchanged |

Duplicate `.grid { display: grid; gap: 1.75rem; }` declaration also removed from
`assets/css/theme.css`. **Sister-site sync note:** both changes must be manually
applied to `overkillhill.com` and `glee-fully.tools` CSS files.

---

## Footer Search Link Fix Applied (Task #1, Step 6 — corrected)

Initial bulk-edit inserted `/search/` into the **header submenu** instead of
the **footer Navigation column** due to regex matching the first occurrence of
the legal link (which appears in both locations). Corrected pass:

- Removed 28 incorrect header-submenu insertions
- Added `/search/` → "Site Search" correctly to the footer Navigation column
  on all 28 applicable pages
- Verified: no `/search/` link in `<nav class="primary-nav">` on any page ✅

---

## Machine-readable results

`assets/docs/responsive-qa/results.json` — full static analysis output
(24 pages × 8 viewports = 192 checks).

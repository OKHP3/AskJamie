# AskJamie™ Responsive QA Report

## Latest Run — 2026-05-26 (Playwright live-browser, Task #3)

| Metric | Value |
|--------|-------|
| Run date | 2026-05-26 |
| Mode | **Playwright** (live Chromium headless — MODE A) |
| Pages checked | 24 |
| Viewports checked | 8 |
| Total checks | 192 |
| **Passing** | **192** |
| **Failing** | **0** |

**All 192 live-browser checks pass.** No horizontal overflow, no console errors,
no broken eager images, no 404s on critical assets across all 24 pages at all 8 viewports.

---

## Issues Found and Fixed (this run)

### 1. Horizontal overflow — `/lens-system/okhp3-brandguard/coca-cola/` (all viewports)

**Root cause:** A bare `<pre><code>` system-prompt block with long unbroken lines had no
overflow handling. The `.code-drop pre` CSS rule (which has `overflow-x: auto`) applies
only to elements inside `.code-drop` wrappers; the bare `<pre>` was unstyled.

**Fix:** Added a global `pre {}` rule in `assets/css/theme.css` (after line 165):
```css
pre {
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
```
This is the only page currently using a bare `<pre><code>` block, but the rule now
protects any future pages that use the same pattern.

---

## How to Re-run

```bash
node scripts/responsive-qa.mjs --base=http://localhost:5000
```

Results are written to `assets/audit/responsive-qa/results.json`.
Screenshots are saved to `assets/audit/responsive-qa/screenshots/` **only for
failing page/viewport combinations** (none on a clean run).

---

## Viewport Coverage

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

## Live-Browser Checks Per Page/Viewport

| # | Check | Method |
|---|-------|--------|
| 1 | No horizontal overflow | `scrollWidth > innerWidth` in-page eval |
| 2 | No JS console errors | `page.on('console')` — `type === 'error'` |
| 3 | No broken eager images | `img.complete && img.naturalWidth > 0` for all `loading != 'lazy'` imgs |
| 4 | No 404 on `.css`/`.js`/`.json` assets | `page.on('response')` — status 404 |

*Note: `ERR_FAILED` console messages are excluded from check #2 — they are testing
artifacts from the harness blocking external resources (Google Fonts, GA, GTM) so
local-asset checks are not affected by network unavailability.*

---

## Pages Checked (24 public pages) — all PASS

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

## Script Architecture (as of Task #3)

`scripts/responsive-qa.mjs` operates in two modes:

**MODE A — Playwright (when available):**
- Creates **8 persistent browser contexts** (one per viewport) at startup — reused
  across all 24 pages (eliminates 184 redundant context-creation calls vs. old approach)
- Blocks external resources via `page.route()` so local-asset checks aren't affected
  by CDN/analytics unavailability in the dev environment
- Wait strategy: `domcontentloaded` (fast) + `page.waitForFunction` to confirm
  eager images have decoded before the broken-image check runs
- All 8 viewports navigate in parallel per page; pages processed sequentially to
  avoid overwhelming the Python HTTP dev server

**MODE B — Static lint (Playwright not available):**
- 10 structural HTML checks per page, applied uniformly to all 8 viewport rows
- Checks: viewport meta, construction overlay, single h1, img alt/width, footer
  search link, year fallback, nav structure, skip link, app.js presence
- Clearly flagged as `static-lint` in results — not confused with live-browser data

---

## Infrastructure Notes (first-time setup)

Playwright Chromium requires system libraries not present in the base Nix environment.
Installed via `installSystemDependencies()`:

```
glib nss nspr atk cups libdrm dbus expat fontconfig freetype libxkbcommon
xorg.libxcb xorg.libX11 xorg.libXcomposite xorg.libXdamage xorg.libXext
xorg.libXfixes xorg.libXrandr xorg.libxshmfence xorg.libXau xorg.libXdmcp
mesa libgbm alsa-lib pango cairo
```

npm devDependency: `playwright` (in `node_modules/playwright`)
Chromium binary: `.cache/ms-playwright/chromium_headless_shell-1223/`

---

## Previous Run — 2026-05-26 (Static lint, Task #1)

| Check mode | Pages | Viewports | Total checks | Issues |
|------------|-------|-----------|--------------|--------|
| Static HTML analysis (10 checks × page × viewport) | 24 | 8 | 192 | **0** |

All 192 static checks passed. Full details in earlier version of this file.

### Static checks that passed (Task #1)

| # | Check | Result |
|---|-------|--------|
| 1 | `name="viewport"` meta present | ✅ All 24 |
| 2 | `construction-overlay` absent | ✅ All 24 |
| 3 | Single `<h1>` per page | ✅ All 24 |
| 4 | All `<img>` have `alt` attribute | ✅ All 24 |
| 5 | All `<img>` have `width` attribute (CLS prevention) | ✅ All 24 |
| 6 | Footer `/search/` link present (except `/search/` itself) | ✅ All 23 applicable |
| 7 | Copyright year `2026` static fallback | ✅ All 24 |
| 8 | No `/search/` link in primary nav | ✅ All 24 |
| 9 | Skip link present | ✅ All 24 |
| 10 | `/assets/js/app.js` script tag present | ✅ All 24 |

---

## Machine-readable results

`assets/audit/responsive-qa/results.json` — full output from latest run
(24 pages × 8 viewports = 192 checks, mode: playwright).

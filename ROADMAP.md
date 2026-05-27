# Roadmap

This roadmap outlines the near-term public direction for the **AskJamie™** repository.

## Current
- BrandGuard™ case study series — ongoing documentation
- Quality gates: `scripts/audit-site.py` runs clean (0 issues across 33 pages);
  re-run on every meaningful HTML change
- Responsive QA: `node scripts/responsive-qa.mjs --static` → 208/208 pass;
  run full Playwright pass after each major round of edits

## Next
- **OG images** — commission 1200×630 landscape social-card images for the
  3 Lens System GPT pages and 12 BrandGuard case studies (currently square
  1024×1024 for all). See `assets/docs/og-image-requirements.md`.
- **Submit sitemap** to Google Search Console and Bing Webmaster Tools.
- **Heading-order auditor** (Task #17) — add automated h1→h2→h3 skip detection
  to `scripts/audit-site.py` so regressions are caught at CI time.
- **Generic-link-text auditor** (Task #18) — extend the auditor to flag bare
  "read more" / "click here" link text across all pages.
- **Sister-site sync** (Task #5) — document the `audit-site.py` and
  `build-search-index.py` sync workflow for the OverKill Hill and
  Glee-fully repos; apply `theme.css` / `app.js` patches.
- **Developer template fixes** (Tasks #10, #13) — add the 9 `assets/templates/`
  files to the QA exclusion list; apply Phase 1 baseline fixes to them.
- **CSP hardening** — refactor the `onload="this.media='all'"` lazy-CSS inline
  handlers into `assets/js/lazy-css.js` so `script-src 'unsafe-inline'` can
  be dropped. Low-risk but touches every page.
- **Self-hosted fonts** — move Baloo 2, Open Sans, and Kalam from
  `fonts.googleapis.com` to `assets/fonts/` to eliminate the third-party
  privacy boundary and two extra DNS lookups.
- **Expand Lens System** with additional BrandGuard™ case studies.

## Later
- Publish a dedicated "How AskJamie Works" deep-dive page
- Cross-link more explicitly between AskJamie, overkillhill.com, and glee-fully.tools
- Evaluate adding a public prompt library or recipe section
- Add progressive web app install flow (PWA manifest + service worker)
- Audit and prune the ~75 unused brand image variants (see `assets/docs/image-usage-report.md`)
- GA disclosure section in `legal/index.html` (GDPR/CCPA best practice)
- Organization JSON-LD `sameAs` — add social profile URLs (LinkedIn, X, Facebook, YouTube)

## Shipped
- **v1.2 (2026-05-27)** — Documentation refresh: README expanded, ROADMAP
  updated, `llms.txt` Last-Updated field, CHANGELOG consolidated, portfolio-fit
  audit document (`AUDIT-ASKJAMIE-PORTFOLIO-FIT.md`) written, auditor `.agents`
  exclusion fix. 0 audit issues.
- **v1.1 (2026-05-27)** — Accessibility & semantic polish: BrandGuard hub
  grid → semantic `<ul>`, Universe Mermaid scroll wrapper, search page
  heading-order fix. 208/208 QA, 0 audit issues.
- **v1.0 (2026-05-27)** — CTA hierarchy (BrandGuard primary), Ko-fi callout
  on homepage, BFS in-page ToC nav, BrandGuard demo notice reordered to
  top of all 13 case pages. 208/208 QA, 0 audit issues.
- **v0.9 (2026-05-26)** — Construction overlays removed, BFS legal copy fixed,
  copyright year fallback, GA4 custom events, contact inquiry cards, footer
  `/search/` link, `grid-3` tablet breakpoint fix, responsive QA script.
- **v0.8 (2026-05-12)** — GTM moved to `<head>`, deprecated meta tags removed
  (8 types × 22–25 pages), `legal/index.html` head-tag fix, 5 titles trimmed,
  root-relative path enforcement, search index rebuilt (128.5 KB, 33 pages).
- **v0.7 (2026-05-03)** — Audit tooling, BrandGuard demo notice on all
  13 case pages, multi-CTA homepage hero, site-wide theme-color sweep,
  4 broken portfolio links fixed. See `AUDIT-ASKJAMIE-FINAL.md`.
- **v0.6 (2026-05-03)** — Search page, expanded About + Legal,
  homepage `#fit` section, `.btn-disabled` component, 101-link
  `noopener noreferrer` sweep. See `AUDIT-REPORT.md`.
- **v0.5 (2026-05-02)** — All-cases BrandGuard grid, BreadcrumbList
  JSON-LD on 22 pages, `Article` JSON-LD on 13 case pages, `llms.txt`,
  sitemap `<lastmod>`, search-index bugfix.
- **v0.4 (2026-05-02)** — Theme/JS reorganisation; inline `<style>` and
  `<script>` blocks reduced to 0; GA4 moved to shared `analytics.js`.
- **v0.3 (2026-04-11)** — Internal site search (modal + JSON index).
- **v0.2 (2026-04-10)** — SEO and meta-tag hardening across all pages.

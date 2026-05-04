# Roadmap

This roadmap outlines the near-term public direction for the **AskJamie™** repository.

## Current
- BrandGuard™ case study series — ongoing documentation
- Quality gates: `scripts/audit-site.py` v0.8 runs clean (0 issues across
  17 quality gates); re-run on every meaningful HTML change

## Next
- Create 1200×630 landscape OG images for all pages (currently square 1024×1024)
- Review `scripts/image-usage-report.md` and prune unreferenced brand image
  variants once cross-checked against off-repo uses (sister sites,
  social cards, marketing materials)
- Submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools
- Mirror v0.8 changes (modern baseline: CSP/referrer meta, image
  loading attrs, prefers-reduced-motion umbrella, expanded auditor)
  into the OverKill Hill and Glee-fully repos
- Expand Lens System with new BrandGuard™ case studies
- **CSP hardening (future)** — refactor the 26 lazy-CSS
  `onload="this.media='all'"` inline handlers into an
  `assets/js/lazy-css.js` helper so `script-src 'unsafe-inline'` can be
  dropped from the CSP. Low-risk but touches every page.
- **Self-hosted fonts (privacy + perf)** — currently loads Baloo 2,
  Open Sans, and Kalam from `fonts.googleapis.com` /
  `fonts.gstatic.com`. Self-hosting under `assets/fonts/` would remove
  the third-party privacy boundary, eliminate two extra DNS lookups,
  and let the CSP drop those external `style-src` / `font-src` entries.

## Later
- Publish a dedicated "How AskJamie Works" deep-dive page
- Cross-link more explicitly between AskJamie, overkillhill.com, and glee-fully.tools
- Evaluate adding a public prompt library or recipe section
- Add progressive web app install flow (PWA manifest + service worker)
- Audit and prune the ~85 unused brand image variants

## Shipped
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

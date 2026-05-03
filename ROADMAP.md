# Roadmap

This roadmap outlines the near-term public direction for the **AskJamie™** repository.

## Current
- BrandGuard™ case study series — ongoing documentation
- Quality gates: `tools/audit-site.py` runs clean (0 issues at v0.7);
  re-run on every meaningful HTML change

## Next
- Add `datePublished` / `dateModified` to the `Article` JSON-LD blocks
  on the 13 BrandGuard case pages (the blocks themselves shipped v0.5)
- Create 1200×630 landscape OG images for all pages (currently square 1024×1024)
- Submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools
- Mirror v0.7 changes (`theme.css`, `tools/audit-site.py`,
  hero-actions wrap) into the OverKill Hill and Glee-fully repos
- Expand Lens System with new BrandGuard™ case studies

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

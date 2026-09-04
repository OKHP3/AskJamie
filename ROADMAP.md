# Roadmap

This roadmap outlines the near-term public direction for the **AskJamie™** repository.

## Current
- BrandGuard™ case study series — ongoing documentation
- Quality gates: `scripts/audit-site.py` runs clean (0 issues across 26 public
  QA paths); 35 HTML files exist on disk, including 9 excluded developer
  templates. Re-run on every meaningful HTML change.
- Responsive QA: `node scripts/responsive-qa.mjs --static` → 192/192 pass
  across the 24 sitemap routes; run full Playwright pass after each major
  round of edits
- Unconditional GA4 is the intentional policy. The page shell loads
  `G-MT9Y10YY0G`, the Legal page discloses aggregate use, and the repository
  contains no visitor export. Counts, engagement, conversions, and funnel rates
  remain unknown rather than estimated from code.
- Google Fonts are intentionally external. Mermaid 11.17.2 is vendored locally
  under `assets/vendor/mermaid/`.
- Twenty landscape WebP OG cards are shipped. Six utility or informational
  pages still use existing square artwork and are not blocked from publication.
- The single current status source is
  [`assets/docs/project-scorecard.md`](assets/docs/project-scorecard.md).

## Next
- **Submit sitemap** to Google Search Console and Bing Webmaster Tools. This is
  an owner or administrator action, not a repository code task.
- **Sister-site sync** — decide whether the documented `theme.css` / `app.js`
  changes should be applied in the OverKill Hill and Glee-fully repositories.
  No sibling repository is modified by this project.
- **Assistive technology verification** — confirm search live-region, keyboard
  focus, theme, and Mermaid fallback behavior with human-operated VoiceOver or
  NVDA testing. Spoken output is currently unknown.
- **CSP hardening** — refactor the remaining inline initialization and lazy-CSS
  handlers so `script-src 'unsafe-inline'` can be dropped.
- **GA4 reporting** — obtain an authorized, read-only export and report the
  stated date range and measurement limitations. Do not infer visitor counts
  from site code.
- **Recurring hosted checks** — retain hosted smoke and public GPT probe
  results outside the static validation path.
- **Optional OG enhancement** — create cards for the remaining pages that use
  square artwork if social-sharing optimization is prioritized. See
  `assets/docs/og-image-requirements.md`.
- **Developer template maintenance** — keep the 9 `assets/templates/` files
  excluded from public QA and update them deliberately when the page shell
  changes.
- **Heading-order auditor** — shipped in `scripts/audit-site.py`.
- **Generic-link-text auditor** — shipped in `scripts/audit-site.py`.
- **Post-merge browser checks** — queued separately from the static audit.
- **Public GPT availability checks** — queued separately from static HTML
  validation.
- **Hosted JavaScript result retention** — queued separately from deployment.
- **Performance budgets** — desktop targeted results clear 90; mobile
  thresholds remain an evidence gap and need a separate performance task.
- **Expand Lens System** with additional BrandGuard™ case studies.

## Later
- Publish a dedicated "How AskJamie Works" deep-dive page
- Cross-link more explicitly between AskJamie, overkillhill.com, and glee-fully.tools
- Evaluate adding a public prompt library or recipe section
- Add progressive web app install flow (PWA manifest + service worker)
- Audit and prune the ~75 unused brand image variants (see `assets/docs/image-usage-report.md`)
- GA4 disclosure in `legal/index.html` — shipped; retain owner/legal review as
  needed
- Organization JSON-LD `sameAs` — add social profile URLs (LinkedIn, X, Facebook, YouTube)

## Shipped
- **v1.2 (2026-05-27)** — Documentation refresh: README expanded, ROADMAP
  updated, `llms.txt` Last-Updated field, CHANGELOG consolidated, portfolio-fit
  audit document (`assets/docs/audit-askjamie-portfolio-fit.md`) written, auditor `.agents`
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
  root-relative path enforcement, search index rebuilt (128.5 KB).
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

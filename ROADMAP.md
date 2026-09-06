# Roadmap

This is the delivery direction for the AskJamie static website as of September
5, 2026. The detailed, assigned work packages and acceptance criteria are in
[`assets/docs/assessment-2026-09-05/delivery-plan.md`](assets/docs/assessment-2026-09-05/delivery-plan.md).
The [project scorecard](assets/docs/project-scorecard.md) separates current
capability from dated verification and remaining uncertainty.

## Current

- Vanilla static HTML, CSS, and browser JavaScript, with 27 source pages and
  25 sitemap/search routes. Nine developer templates are separate from those
  source pages. Generated release copies are not another product.
- GitHub Actions validates source, asset fingerprints, generated search data,
  Python regressions, browser behavior, and the canonical audit before
  preparing the allowlisted Pages artifact for deployment.
- The How AskJamie Works page, scheduled hosted JavaScript checks, public GPT
  probes, retained diagnostics, and generated CSP/asset fingerprints exist.
  They are shipped implementations, not future backlog items.
- Unconditional GA4 and external Google Fonts remain intentional policies.
  Analytics outcomes require an authorized export; code does not establish
  traffic or conversion rates.
- Mermaid 11.17.2 is vendored locally with a static fallback. Human-operated
  VoiceOver/NVDA spoken output remains unverified.

## Now: complete the scoped assessment and first repair batch

- Finish the Architect, Project Manager, and Worker evidence reports and retain
  pre-change observations separately from post-change results.
- Harden artifact preparation against unintended directory deletion and
  accidental packaging of hidden files, symlinks, and source artwork.
- Correct AskJamie search dialog branding and the dedicated search page's
  promised Escape/Enter keyboard behavior.
- Align the operating guide, scorecard, and architecture clarifications with
  the verified source and release workflow.
- Re-run relevant static and browser checks. Report the baseline ignored
  `.DS_Store` audit findings honestly instead of calling a partial suite clean.

## Next: visitor trust, accessibility, and release reliability

- Review no-JavaScript content visibility, skip-link focus, reduced-motion
  behavior, search result semantics, and measured footer contrast. Implement
  confirmed defects in separate bounded batches with browser evidence.
- Resolve contradictory prototype, affiliation, and capability wording. Retain
  the owner's voice while making availability and evidence clear at the point
  of each claim or outbound action.
- Review case-study source destinations. Private working context needs a
  confirmed public publication route before it is offered to visitors.
- Prevent browser QA from silently falling back to static checks in required
  CI runs; retain actionable CSP and dependency-failure diagnostics.
- Update the CI runtime to a supported Node release and review dependency and
  Action pinning without introducing application dependencies.
- Make the active sibling-sync tool refuse unsafe mutation, dirty preimages,
  and live Git locks. No sibling repository change is included here.
- Reconcile tracked generated release copies with the source-of-truth and
  clean-artifact policy while preserving recoverable owner work.

## Later: measured improvements and owner decisions

- Measure mobile performance on agreed representative routes, then optimize
  oversized logo assets and justified shared payload costs. Keep external
  Google Fonts and the AskJamie brand treatment.
- Review a lighter shared page-shell authoring mechanism only if duplication
  remains a demonstrated maintenance cost. A framework migration is not a
  prerequisite.
- Conduct human-operated VoiceOver/Safari and NVDA/Firefox journey sessions.
- Submit the sitemap through authorized Google/Bing webmaster accounts and
  inspect indexing results. This is an administrator task.
- Obtain a read-only GA4 export with an explicit date range and measurement
  limits if the owner wants traffic and journey analysis.
- Evaluate remaining OG artwork, additional Lens System cases, or public
  recipes only after existing visitor journeys and evidence gaps are addressed.
- Decide separately whether approved shared CSS/JavaScript changes should be
  synchronized to sibling repositories.

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

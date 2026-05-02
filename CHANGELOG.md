# Changelog

All notable changes to the **AskJamie™** public repository are recorded here.

## [Unreleased]

### Planned
- Expand Lens System with additional BrandGuard™ case studies
- Add JSON-LD Article schema to all BrandGuard case study pages
- Create landscape (1200×630) OG images for optimal social card display
- Add BreadcrumbList schema to all inner pages
- Tighten 17 over-length meta descriptions and 2 over-length titles
- Add "More BrandGuard cases" grid to BrandGuard hub + each case (resolves 4 orphaned cases)
- Surface the 12 unused Company Logos on the BrandGuard hub
- Add `llms.txt` for LLM crawler guidance
- Audit and prune the ~85 unused brand image variants

## [v0.4 — 2026-05-02]

### Restructured
- **`assets/css/theme.css`** reorganised into a stable, diff-friendly order:
  `1. GLOBAL` → `2. OVERKILL HILL P³` → `3. GLEE-FULLY` → `4. ASKJAMIE`.
  Every section now lives under exactly one tier; a SECTION INDEX header at
  the top of the file lists every section + its source-line range.
  - 21 GLOBAL sections (~2420 lines): tokens, reset, layout, header/nav,
    typography, footer, scroll reveal, article styles, construction overlay,
    Ko-fi, GPT Hero base, cross-site utilities, site search.
  - 3 OKH sections (~271 lines): Blueprint Forge hero, OKH 404, OKH Mermaid.
  - 9 GLEE sections (~745 lines): Glee tokens + hero + about/contact/legal
    paper-effect heroes + Glee Mermaid (×2).
  - 5 ASKJAMIE sections (~570 lines): AskJamie tokens, system pages,
    AskJamie Mermaid, BFS GPT-hero variant, BFS hero.
  - Brace counts verified preserved (593 opens / 594 closes — identical to
    pre-reorganise file).  No visual regression — homepage, BrandGuard case,
    About, and Universe screenshots all pixel-equivalent.
- **`tools/restructure-theme.py`** — deterministic rebuild tool: reads
  `assets/css/theme.css.bak`, slices verbatim by an explicit section map,
  reassembles in tier order with banners + TOC, and refuses to write if the
  brace count drifts.  Re-runnable any time the canonical order needs
  re-applying.

### Externalised
- **All 25 Google Analytics inline `<script>` blocks** moved to a single
  shared file: `assets/js/analytics.js` (defers cleanly behind the async
  `gtag.js` loader).  HTML pages now use:
  ```html
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-MT9Y10YY0G"></script>
  <script defer src="/assets/js/analytics.js"></script>
  ```
  Benefits: one place to update the GA4 ID, browser caches across pages,
  CSP-friendly (no need for `'unsafe-inline'` or per-page nonces), trivial
  to extend with custom `gtag('event', ...)` calls.
- **`assets/js/app.js`** restructured with explicit GLOBAL section banners:
  self-initializing IIFEs (search loader, reading progress, sticky TOC) at
  the top, single DOM-ready bootstrap below.  Removed a redundant
  DOMContentLoaded handler whose target element didn't exist yet — fixes a
  latent dark→light theme flash on subsite navigation.

### Verified
- Inline-content audit across all 25 HTML files:
  - **0** `<style>` blocks  •  **0** `style="..."` attributes  •  **0**
    inline `<script>` blocks  •  26 JSON-LD blocks (intentionally inline
    per Google's structured-data spec).
- All 7 critical assets serve HTTP 200 (`/`, `theme.css`, `app.js`,
  `analytics.js`, `search.js`, `mermaid-init.js`, `search-index.json`).

## [v0.3 — 2026-04-11]

### Added
- **Internal site search** — zero-dependency, static, client-side search engine
  - `tools/build-search-index.py` — extracts title / description / h1 / h2-h3 / body excerpts from every `.html` file into a single JSON index
  - `assets/data/search-index.json` — 23 pages, ~100 KB raw / ~25 KB gzipped
  - `assets/js/search.js` — modal UI, live results, keyboard navigation (`/` or `⌘K`, `↑↓`, `Enter`, `Esc`), match-term highlighting
  - Search trigger button injected into `.site-header` on every page
  - Search modal styles appended to `assets/css/theme.css` (light + dark theme variants, mobile responsive)
  - `app.js` lazy-loads `search.js` after DOM parse; the JSON index is only fetched when the user actually opens the modal
- Full site audit recorded in `replit.md` (orphaned pages, orphaned assets, metadata over-length report)

### Updated
- `assets/js/app.js` — added lazy loader for `search.js` at top of file
- `replit.md` — documented search architecture, audit findings, expanded "Known Gaps"

## [v0.2 — 2026-04-10]

### Changed
- Mermaid JS updated from v10 inline blocks to v11 ESM external module pattern (`assets/js/mermaid-init.js`)
- Async font loading applied to all 25 HTML files (removes render-blocking)
- Emoji removed from all `<title>` tags sitewide (retained in H1s and body)
- `Organization` JSON-LD schema added to homepage alongside `WebSite`
- `twitter:creator` standardized to `@overkillhillp3` across all pages
- `og:image:width` and `og:image:height` added to homepage

### Added
- `robots.txt` with AI bot governance rules and sitemap reference
- `sitemap.xml` with all 23 indexable pages and correct priorities
- `publisher`, `revisit-after`, `mobile-web-app-capable`, `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, `og:image:type` meta tags added to all pages
- Cross-site sync CSS utility classes appended to `theme.css`
- `site.webmanifest` updated with correct brand name, colors, and favicon paths
- Repository governance files: `AGENTS.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `LICENSE.md`, `ROADMAP.md`, `SECURITY.md`

### Fixed
- `under-construction.html` changed from `index, follow` to `noindex, nofollow`
- Inline styles extracted to utility CSS classes across 8 pages

## [v0.1 — 2026-04-07]

### Established
- Core brand README
- Public website source for askjamie.bot
- AskJamie™ homepage, About, Contact, Legal, Universe pages
- Lens System index and 13 BrandGuard™ case study pages
- Resume Representative and Professional Portfolio pages
- Custom 404 page

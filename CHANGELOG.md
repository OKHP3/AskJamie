# Changelog

All notable changes to the **AskJamie™** public repository are recorded here.

## [Unreleased]

### Planned
- Expand Lens System with additional BrandGuard™ case studies
- Create landscape (1200×630) OG images for optimal social card display
- Audit and prune the ~85 unused brand image variants

## [v0.5 — 2026-05-02] — Showpiece pass

### Added
- **Built-with-Replit footer credit** on every page (25 / 25). Left-aligned
  "Built with **Replit**" badge in brand orange (`#f26207`, hover `#ff7a2a`)
  pointing at the OverKill Hill P³ Replit referral link
  (`https://replit.com/refer/overkillhillp3/`); copyright stays optically
  centred via a flex-row layout with a same-width spacer on the opposite
  side.
- **`llms.txt`** at the project root — the emerging convention for guiding
  LLM crawlers / AI agents.  Points at every canonical URL in the site
  (core pages, Lens System GPTs, all 13 BrandGuard case studies).
- **Article JSON-LD** on every BrandGuard case study page (13 pages):
  headline, description, image, `datePublished` / `dateModified`,
  publisher / author, `inLanguage`, `mainEntityOfPage`.
- **BreadcrumbList JSON-LD** on every inner page (22 pages — all except
  homepage, 404, and under-construction).
- **`<link rel="preconnect" href="https://www.googletagmanager.com">`**
  added on all 25 pages so the GA4 handshake starts in parallel with the
  fonts handshake.
- **All 13 BrandGuard cases grid** on the BrandGuard hub
  (`lens-system/okhp3-brandguard/`).  Resolves the 4 previously
  orphaned cases (`coca-cola`, `dollar-general`, `lego`, `mathews-archery`)
  and surfaces all 12 previously-unused `Company Logos/*.png` assets.

### Changed
- **21 over-length meta descriptions tightened** to ≤165 chars (longest was
  `lego` at 299 → 148).  Mirrored to `og:description` and
  `twitter:description` on every page.
- **2 over-length titles tightened** to ≤70 chars (`enterprise-sleuth`
  80 → 70; `okhp3-brandguard/index` 75 → 64).  Mirrored to `og:title` and
  `twitter:title`.
- **78 `<img>` elements** gained `decoding="async"`; 7 below-the-fold
  images gained `loading="lazy"` (the first 2 images per page — usually
  the LCP candidates — were intentionally left eager).
- **`sitemap.xml`** rewritten with `<lastmod>2026-05-02</lastmod>` on every
  URL (the original sitemap had no `<lastmod>` tags at all).

### Fixed
- **`tools/build-search-index.py`** — body excerpts were silently empty for
  every page in the index because of two bugs:
  1. `STRIP_CLASSES_CONTAINS` included `askjamie-paper`, `brand-stripes`
     and `site-specials` — but those classes wrap the actual page
     content, not chrome.  Removed.
  2. The HTML tag stack was being polluted by void elements
     (`<img>`, `<br>`, `<input>`, …) that never receive a matching
     `handle_endtag`, so a later `</a>` would pop the wrong entry and
     leave the site `<header>` strip-zone permanently open.  Fixed by
     adding a `VOID_TAGS` set that's never pushed, plus a
     pop-the-nearest-match end-tag handler that also cleans up any
     intervening unclosed tags (e.g. HTML5 optional `</p>`).

  Result: the index went from 7.7 KB / 0 body chars → 100.6 KB / 79,965
  body chars across 23 pages.  Internal site search is now actually
  searchable.
- **`mathews-archery` canonical URL** — fixed a path-case typo
  (`okhp3-BrandGuard` → `okhp3-brandguard`).

### Tooling
- **`tools/enhance-pages.py`** — new idempotent bulk editor for
  site-wide passes (footer markup, preconnects, image attribute polish,
  meta-description / title rewrites, BreadcrumbList JSON-LD,
  Article JSON-LD, canonical typo fixes).  Re-runnable safely.

### Verified
- Inline-content audit: 0 `<style>` blocks, 0 `style=""` attributes,
  0 real inline `<script>` blocks (61 `application/ld+json` blocks
  intentionally remain inline per Google's structured-data spec).
- HTTP smoke test: every key URL returns 200
  (`/`, `/lens-system/okhp3-brandguard/`, all CSS/JS/data assets,
  `/llms.txt`, `/sitemap.xml`).
- Visual: BrandGuard cases grid renders cleanly with all 13 logos in a
  responsive 4-up grid.

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

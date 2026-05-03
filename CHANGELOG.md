# Changelog

All notable changes to the **AskJamie™** public repository are recorded here.

## [Unreleased]

### Added (Mermaid affiliate referral)
- `universe/index.html` — added a centered referral note directly under
  the Mermaid universe diagram: *"Diagram rendered with Mermaid.js.
  **Try Mermaid.AI →** if you want to explore the syntax yourself."*
  The link points to the OKH affiliate URL
  `https://mermaidchart.cello.so/UhVlNtC2MlS`, opens in a new tab with
  `noopener noreferrer`, and is styled in the official Mermaid hot pink
  **#FF3670** (hover **#ff6b95**) — matching the OverKill Hill
  reference page (`writings/first-diagram-is-a-liar`).
- `assets/css/theme.css` — new reusable `.mermaid-referral-note` and
  `a.mermaid-referral-link` rules so the same pattern works on any
  future AskJamie page that embeds Mermaid.
- `tools/audit-site.py` — new per-page check: any page containing
  `<pre class="mermaid">` must also carry the `mermaidchart.cello.so`
  link **and** the `mermaid-referral-link` class. Prevents future
  Mermaid pages from shipping without the affiliate link.

### Added (llms.txt sync)
- `llms.txt` — added the `/search/` page entry. It was already in
  `sitemap.xml` but missing from `llms.txt` (caught by a sitemap ↔
  llms diff during a final pre-push sweep).

### Changed
- Bumped `dateModified` to `2026-05-03` in the `Article` JSON-LD on all
  13 BrandGuard case pages (they were materially updated today by the
  v0.7 demo-notice + theme-color sweep).

### Added (image audit)
- `tools/image-usage-report.md` — generated report cross-referencing
  every file under `assets/img/` against every HTML / CSS / JS / JSON /
  MD / XML / webmanifest in the repo. Result: 120 image files on disk,
  45 referenced, **75 unreferenced**. Report-only — no files removed,
  pending cross-check against off-repo uses (sister sites, social
  cards, marketing materials).

### Added (Phase 13 — template library)
- `/assets/templates/` directory with **9 templates**, one per Page Type:
  `template--homepage.html`, `template--interior-single.html`,
  `template--interior-form.html`, `template--hub.html`,
  `template--lens-detail.html`, `template--case-study.html`,
  `template--error.html`, `template--holding.html`,
  `template--utility.html`. Each follows the Phase 13 rules:
  full-fidelity copy of the representative production page with
  page-specific content swapped to `[[DOUBLE-BRACKET]]` tokens, a
  template header comment block at the top, and section-level comments
  above every `<section>` inside `<main>`.
- `tools/generate-templates.py` — deterministic generator. Tokenises
  meta tags (title, description, OG, Twitter, canonical), clears
  JSON-LD bodies to a placeholder, replaces hero/section/card
  text with named tokens, and tokenises non-shared images (nav and
  footer logos preserved as Rule 5 exceptions).
- `/assets/templates/INDEX.md` — full Page-Type → template mapping
  for all 26 HTML files, plus token reference table and
  "Adding a New Template" workflow.
- `tools/audit-site.py` — `templates/` added to `EXCLUDE_DIRS` so the
  auditor skips token-bearing template files.

### Planned
- Expand Lens System with additional BrandGuard™ case studies
- Create landscape (1200×630) OG images for optimal social card display
- Audit and prune the ~85 unused brand image variants
- Mirror v0.7 shared-asset changes (`theme.css`, `tools/audit-site.py`)
  into OverKill Hill and Glee-fully repos

## [v0.7 — 2026-05-03] — Audit-tooling, BG demo notice, hero CTA cluster

See `AUDIT-ASKJAMIE-FINAL.md` at the repo root for the full v2.0 cycle
write-up.

### Added
- **`tools/audit-site.py`** — reproducible static-site auditor. Walks
  every `.html` file in the repo and reports per-page issues
  (title/description length, missing canonical, missing OG fields,
  image alt/width/height, `target=_blank` links missing
  `rel="noopener noreferrer"`, known placeholders, wrong `theme-color`),
  plus sitemap ↔ disk and search-index ↔ disk reconciliation.
  Writes `tools/audit-report.md`. Current run: **0 issues**.
- **Reusable BrandGuard™ demo notice block** injected above `</main>`
  on all 13 BrandGuard case-study pages, plus `.brandguard-demo-notice`
  CSS in the ASKJAMIE tier of `theme.css`. The notice clarifies the
  case is a public-information demonstration, not an endorsement, and
  links to `/legal/`.
- **Multi-CTA homepage hero cluster** — replaces the single
  "Open Résumé Representative" button with three buttons:
  Explore the Lens System (primary), See BrandGuard™ in action,
  Talk with Jamie. Hero-actions container is now `flex-wrap` so the
  cluster stacks on narrow viewports.
- **`AUDIT-ASKJAMIE-FINAL.md`** — v2.0 cycle deliverable.

### Fixed
- **Four broken internal links** in the BrandGuard hub
  ("Part of the AskJamie portfolio" section) repaired:
  `/resume-representative/`, `/professional-portfolio/`,
  `/enterprise-sleuth/`, and `/bfs-framing-intelligent-futures/` all
  pointed at non-existent root-level paths. Now correctly prefixed
  with `/lens-system/` (and `/lens-system/okhp3-brandguard/` for BFS).
- **Site-wide `theme-color` sweep** — 16 pages had dark-template
  leftovers (`#0f172a`, `#111827`, `#1e40af`, `#1f2937`, `#c46a2c`)
  or brand-of-the-page colors (`#006241` Starbucks, `#d4002a` Coca-Cola,
  `#2d6f7e` LVMH). All now resolve to the AskJamie brand teal `#2c5e6f`
  for consistent address-bar tinting.
- **"Discount Tires" → "Discount Tire"** typo fix in
  `universe/index.html` Mermaid diagram (label `BRG10`).
- **README** — "Resume Representative" → "Résumé Representative" for
  spelling consistency with the on-site copy.

## [v0.6 — 2026-05-03] — Search + full-site audit pass

See `AUDIT-REPORT.md` at the repo root for the full per-issue breakdown.

### Added
- **Dedicated `/search/` page** matching the OverKill Hill pattern: hero
  banner, big input, live result count, category-filter chips, and large
  result cards with category pill, URL crumb, title, and snippet with
  highlighted matches. Reads the existing
  `/assets/data/search-index.json` (no re-indexing required); the existing
  modal/overlay search continues to work site-wide.
- New `assets/js/search-page.js` (page logic only; coexists with the
  overlay's `search.js`), `.search-page` styles appended to `theme.css`,
  and `/search/` added to `sitemap.xml`.
- Deep-linkable `?q=...` query param on the search page.
- **`#fit` "Where it fits" section** on the homepage — three-card grid
  positioning AskJamie™ alongside OverKill Hill P³™ and Glee-fully PT™.
  Resolves a long-standing dead nav anchor.
- **Expanded `about/index.html`** — three new card-grid sections
  ("Who Jamie is", "What AskJamie™ is not", "Who this is for") in the
  established brand voice. Page now matches the depth of `lens-system/`.
- **Expanded `legal/index.html`** — added Trademarks, BrandGuard™
  disclaimer (public-data only / not impersonation), Privacy (GA4 only,
  no first-party cookies), and Terms-of-use sections. Stamped
  "Last updated: 2026-05-03".
- **`.btn-disabled` CSS** for non-interactive "Coming soon" CTAs.

### Fixed
- **JSON-LD `SearchAction` lie repaired site-wide.** 18 pages declared
  `target: https://askjamie.bot/?s={search_term_string}` — a pattern the
  site never implemented. Rewritten to point at the new `/search/` page
  with the correct `?q=` parameter.
- **`index.html`** "View this milestone" anchor was missing `href` —
  now points at the BFS BrandGuard case study.
- **Two placeholder GPT URLs** (`ASK-JAMIE-GPT-ID-HERE`) in
  `lens-system/index.html` and `under-construction.html` converted to
  non-link "Coming soon" buttons (`role="link"`, `aria-disabled="true"`).
- **Defer/aria shortcut fix on the dedicated search page** — global
  `/` and `Cmd+K` now focus the page input on `/search/` instead of
  popping the overlay on top of it.
- **Highlight token ordering** in `search-page.js` — sort tokens
  longest-first so a shorter token doesn't match inside the `<mark>`
  tag of a longer one (e.g. "brand" inside "brandguard").
- **`P3` → `P³`** in keyword metas across 6 pages. Body copy already
  used the correct superscript.

### Removed
- **Dead Ko-fi overlay-widget script** removed from 8 pages — the
  `kofiWidgetOverlay.draw(...)` config call was never present, so the
  third-party download had no visible effect. Ko-fi link in the footer
  Connect column remains.
- **Unused `mermaid-init.js` script tags** removed from 22 pages that
  have no `<pre class="mermaid">` blocks. Now loaded only on
  `universe/index.html` (the one page with a real diagram).

### Security
- **`rel="noopener noreferrer"`** on every external `target="_blank"`
  link site-wide (**101 occurrences** — initial `sed` pass caught 34 in
  the footer Connect column; a broader Perl regex pass caught the
  remaining 67 inside the 13 BrandGuard case-study pages and a few
  others). `noreferrer` blocks referrer leakage and implies `noopener`.

### Accessibility
- "Coming soon" CTA semantics fixed on `lens-system/index.html` and
  `under-construction.html`. Original draft used a
  `<span role="link" aria-disabled="true">` (announces interactive link
  semantics on a non-interactive element). Replaced with the correct
  `<button type="button" disabled aria-disabled="true">` so screen
  readers announce a real disabled control.

### PWA / manifest
- **`site.webmanifest` colors** corrected from a leftover dark-mode
  template (`#111827` / `#020617`) to the actual brand palette
  (`theme_color: #2c5e6f` muted teal, `background_color: #f5efe1` cream).
  PWA splash will no longer flash black on install.

### Tooling
- **Search index rebuilt** (`tools/build-search-index.py`) to capture
  the new `#fit` section and the expanded About / Legal copy.
  Now 101.7 KB / 24 pages.
- **`sitemap.xml` `<lastmod>`** bumped to 2026-05-03 on every page that
  changed.

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

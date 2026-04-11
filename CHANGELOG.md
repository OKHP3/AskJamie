# Changelog

All notable changes to the **AskJamie™** public repository are recorded here.

## [Unreleased]

### Planned
- Expand Lens System with additional BrandGuard™ case studies
- Add JSON-LD Article schema to all BrandGuard case study pages
- Create landscape (1200×630) OG images for optimal social card display
- Add BreadcrumbList schema to all inner pages

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

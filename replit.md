# AskJamie™ — OverKill Hill P³™

## Project Overview

A static marketing and documentation website for **AskJamie™**, an AI persona and "thinking partner" platform by OverKill Hill P³™ (OKHP). It showcases the AskJamie™ AI helpdesk concept, the Lens System portfolio case studies, and BrandGuard™ integrations.

## Tech Stack

- **Frontend:** Vanilla HTML5, CSS3 (CSS custom properties/variables), JavaScript
- **Diagramming:** Mermaid.js v11 ESM (via CDN, external module — no inline scripts)
- **Fonts:** Google Fonts (Alfa Slab One, DM Sans) — loaded async, non-blocking
- **No build system** — pure static files served directly

## Project Layout

```
/                     # Root: index.html, 404.html, under-construction.html
assets/
  css/theme.css        # Main stylesheet (3600+ lines, multi-brand theming + cross-site sync utilities)
  js/app.js            # Main JS (scroll reveals, theme toggles, reading progress, sticky TOC)
  js/mermaid-init.js   # Mermaid v11 ESM diagram initialization (external file, no inline scripts)
  img/                 # Brand assets, avatars, case study images
  img/favicons/        # Full favicon set (ico, 16/32/48px PNG, SVG, android-chrome, apple-touch)
about/                 # About page
contact/               # Contact page
legal/                 # Legal pages
universe/              # Universe/ecosystem overview
lens-system/           # Portfolio case studies
  enterprise-sleuth/
  okhp3-brandguard/    # BrandGuard case studies (Coca-Cola, Lego, Starbucks, LVMH, etc.)
  professional-portfolio/
  resume-representative/
```

## Development Server

- **Workflow:** "Start application"
- **Command:** `python3 -m http.server 5000 --bind 0.0.0.0`
- **Port:** 5000

## Deployment

- **Type:** Static site
- **Public directory:** `.` (project root)

## SEO & Meta Tag Status (v0.2 — 2026-04-10)

All 25 HTML files have been audited and hardened. Every page has:
- `charset`, `viewport`, `http-equiv`, `language`
- `title` (unique, emoji-free), `description`, `keywords`
- `author`, `creator`, `publisher`
- Full Open Graph set: `og:title/description/type/url/image/image:alt/image:width/image:height/image:type/site_name/locale`
- Full Twitter card set: `twitter:card/title/description/image/image:alt/site/creator`
- Robots/crawl tags: `robots`, `googlebot`, `bingbot`, `revisit-after`
- `canonical` link
- Mobile/PWA tags: `theme-color`, `color-scheme`, `mobile-web-app-capable`, `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`
- Favicon links
- `site.webmanifest` reference

## Repository Governance Files

All required files exist at root:
`AGENTS.md`, `CHANGELOG.md`, `CNAME`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`,
`favicon.ico`, `LICENSE`, `LICENSE.md`, `README.md`, `ROADMAP.md`,
`robots.txt`, `SECURITY.md`, `site.webmanifest`, `sitemap.xml`, `404.html`

## Known Gaps (require manual action)

- **OG images:** All pages use a square 1024×1024 avatar PNG as OG image. The gold standard recommends 1200×630 landscape. A purpose-built landscape OG image would improve social card display.
- **JSON-LD on inner pages:** Homepage has WebSite + Organization schema. BrandGuard™ case study pages (articles) would benefit from `Article` schema with `datePublished`/`dateModified`.
- **BreadcrumbList schema:** Recommended for all inner pages for rich results.
- **Search Console submission:** `sitemap.xml` should be submitted to Google Search Console and Bing Webmaster Tools.

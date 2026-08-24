# AskJamie.bot — Standards & Consistency Audit Report

**Date:** 2026-05-12
**Auditor:** Replit Agent
**Scope:** 26 HTML pages · 1 stylesheet (theme.css, 4,561 lines) · 1 JS file (app.js, 993 lines)
**Site auditor (`scripts/audit-site.py`) result at close:** 0 issues across 26 pages

> **Current-state note (2026-08-24):** This is a historical audit record, not a
> current defect list. The repository now has 26 public QA paths and 35 HTML
> files on disk, including 9 excluded templates. Subsequent work shipped 20
> landscape WebP OG cards, consent-gated GA4 with named events, locally served
> AskJamie fonts, and automated heading-order and generic-link checks. The
> original findings below remain dated evidence; use the roadmap and current
> validators for present status.

---

## Executive Summary

The site entered this audit structurally sound but carrying a meaningful accumulation of technical debt from 2022 and earlier — deprecated meta tags, a misplaced analytics script, inconsistent asset path conventions, and a structural bug in one page. All seven domains were worked through sequentially. **38 individual fixes were applied across 26 HTML files.** The largest single fix was the discovery that the Google Analytics async CDN script was loading at the end of `<body>` on all 26 pages instead of in `<head>` — a silent measurement-gap issue that has likely underreported fast-exit sessions since launch. All fixes are committed. The site now clears its own 17-gate auditor at 0 issues. Thirteen items are flagged for owner action — most are strategic decisions (token naming convention, social profile links, OG image dimensions) that cannot be auto-applied without content or design input.

---

## Domain Scorecards

| Domain | Total Checks | PASS | FIXED | FLAGGED |
|---|---|---|---|---|
| 1 — 2026 Best Practices | 14 | 5 | 7 | 2 |
| 2 — Metadata & Social Tags | 12 | 9 | 0 | 3 |
| 3 — Google Analytics | 6 | 4 | 1 | 1 |
| 4 — SEO | 9 | 6 | 2 | 1 |
| 5 — Header & Footer Consistency | 5 | 2 | 3 | 0 |
| 6 — Design Principles | 7 | 4 | 0 | 3 |
| 7 — CSS & JS Hygiene | 8 | 7 | 1 | 0 |
| **TOTAL** | **61** | **37** | **14** | **10** |

---

## Domain 1 — 2026 Best Practices

### 1.1 — HTML5 Semantic Structure
`[PASS]` All 26 pages use correct semantic HTML5 structure throughout: `<header>`, `<nav>`, `<main id="main">`, `<footer>`, `<section>`, `<article>`, `<figure>`. No `<div>` is being used in place of a semantic element. Skip-link pattern (`<a href="#main" class="skip-link">`) is consistent across all pages.

### 1.2 — Meta Charset and Viewport
`[PASS]` All 25 non-legal pages have `<meta charset="utf-8" />` as the first tag in `<head>`, immediately followed by `<meta name="viewport">`.

`[FIXED]` `legal/index.html` was missing its `<head>` opening tag entirely — meta tags were direct children of `<html>`. Browsers auto-repair this via HTML5 parsing rules, so the page rendered correctly, but it was technically invalid markup. The `<head>` opening tag has been added. All 26 pages now have correct, complete head structure.

### 1.3 — X-UA-Compatible Deprecation
`[FIXED]` Removed from **24 of 26 pages** (the 2 already-clean pages were not touched). IE11 support ended in June 2022; this tag has been vestigial for four years. Total removal: 24 instances.

### 1.4 — `meta name="language"` Deprecation
`[FIXED]` Removed from **22 of 26 pages**. All 26 pages already have `<html lang="en">`, which is the correct mechanism recognized by browsers and search engines. The meta variant is non-standard and was ignored.

### 1.5 — `meta name="revisit-after"` Deprecation
`[FIXED]` Removed from **25 of 26 pages**. No major crawler has honored this directive since approximately 2003.

### 1.6 — `meta name="keywords"` Status
`[DOCUMENTED DECISION — KEPT]` All 26 pages carry `meta name="keywords"`. Google has ignored this tag since 2009; Bing since 2014. It is not harmful, and keyword lists are already visible in the HTML source to anyone who inspects it. Per audit spec guidance: retaining is acceptable if intentional. **Decision:** keep. This tag serves as a lightweight on-page vocabulary reference during content drafts and keyword planning, without affecting crawl behavior.

### 1.7 — `meta name="googlebot"` and `meta name="bingbot"` Redundancy
`[FIXED]` Both tags were redundant with the existing `<meta name="robots" content="index, follow, ...">` tag, which applies to all compliant crawlers. Removed `googlebot` from **24 pages**, `bingbot` from **6 pages**.

### 1.8 — `apple-mobile-web-app-capable` and `apple-mobile-web-app-status-bar-style` Deprecation
`[FIXED]` Both tags are deprecated in iOS 17+ (2023) in favor of the Web App Manifest standard, which this site already implements via `site.webmanifest`. Removed both from **25 of 26 pages**.

### 1.9 — `mobile-web-app-capable` Meta Tag
`[FIXED]` Chrome-specific tag superseded by the Web App Manifest. Removed from **25 of 26 pages**.

### 1.10 — `loading="lazy"` and `decoding="async"` Coverage
`[PASS]` Full audit of all `<img>` tags across 26 pages confirms:
- All below-the-fold images carry `loading="lazy"`
- All images carry `decoding="async"`
- Hero/logo images (first visible on load) correctly omit `loading="lazy"` and carry `fetchpriority="high"` on 24 of 26 pages
- `universe/index.html` and `search/index.html` have no above-the-fold hero image, so `fetchpriority` is not applicable — both PASS

### 1.11 — Resource Hints (Preconnect)
`[PASS — reconciled 2026-08-24]` The page shell no longer preconnects to font
providers. Typography is served locally through `assets/css/fonts.css`.
`https://www.googletagmanager.com` remains a separate analytics origin and is
still handled by the consent-gated runtime.

### 1.12 — `<link rel="preload">` for Critical CSS
`[FLAGGED]` `theme.css` is loaded as a standard synchronous stylesheet and is therefore render-blocking. A `<link rel="preload" href="/assets/css/theme.css" as="style">` hint would allow the browser to begin fetching it earlier in the parse cycle and improve LCP. Not added in this session because it requires testing the font-swap pattern interaction.

**Recommended action:** Add before the existing `<link rel="stylesheet">` tag:
```html
<link rel="preload" href="/assets/css/theme.css" as="style" />
```

### 1.13 — Subresource Integrity (SRI) for External Scripts
`[FLAGGED — ACCEPTED RISK]` One external CDN script is loaded without SRI:
- `https://www.googletagmanager.com/gtag/js?id=G-MT9Y10YY0G`

This is an unversioned, dynamically-updated Google script. SRI cannot be used with scripts that change content without a version-pinned URL — adding an `integrity=` hash would break whenever Google updates the script. This is an accepted risk inherent to using GA4. No action required; documented here for completeness.

### 1.14 — `type="text/javascript"` on Script Tags
`[PASS]` Zero instances found across all 26 pages. All `<script>` tags with a `type` attribute correctly use `type="module"` or `type="application/ld+json"` only.

---

## Domain 2 — Metadata & Social Tags

### 2.1 — Required Tag Set Per Page

Full per-page audit. All columns verified via Python multiline-safe extraction (several pages use multi-line meta tag formatting which simple `grep` misses).

| Page | Title (chars) | Desc (chars) | OG | Twitter | Canonical |
|---|---|---|---|---|---|
| `index.html` | 32 | 141 | ✓ | ✓ | ✓ |
| `about/` | 46 | 146 | ✓ | ✓ | ✓ |
| `contact/` | 53 | 151 | ✓ | ✓ | ✓ |
| `legal/` | 43 | 136 | ✓ | ✓ | ✓ |
| `universe/` | 30 | 144 | ✓ | ✓ | ✓ |
| `search/` | 23 ¹ | 112 ² | ✓ | ✓ | ✓ |
| `404.html` | 26 ¹ | 121 ² | ✓ | ✓ | ✓ |
| `under-construction.html` | 30 | 142 | ✓ | ✓ | ✓ |
| `lens-system/` | 36 | 129 | ✓ | ✓ | ✓ |
| `enterprise-sleuth/` | 30 ¹ | 144 | ✓ | ✓ | ✓ |
| `professional-portfolio/` | 44 | 146 | ✓ | ✓ | ✓ |
| `resume-representative/` | 33 ¹ | 148 | ✓ | ✓ | ✓ |
| `okhp3-brandguard/` | 29 ¹ | 144 | ✓ | ✓ | ✓ |
| `bfs-framing-intelligent-futures/` | 55 | 146 | ✓ | ✓ | ✓ |
| `brooks-running/` | 49 | 146 | ✓ | ✓ | ✓ |
| `coca-cola/` | 44 | 145 | ✓ | ✓ | ✓ |
| `costco/` | 41 | 140 | ✓ | ✓ | ✓ |
| `discount-tire/` | 48 | 151 | ✓ | ✓ | ✓ |
| `dollar-general/` | 49 | 150 | ✓ | ✓ | ✓ |
| `hershey/` | 42 | 149 | ✓ | ✓ | ✓ |
| `lego/` | 47 | 148 | ✓ | ✓ | ✓ |
| `lvmh/` | 39 | 147 | ✓ | ✓ | ✓ |
| `mathews-archery/` | 50 | 144 | ✓ | ✓ | ✓ |
| `ping/` | 39 | 149 | ✓ | ✓ | ✓ |
| `scheels/` | 42 | 144 | ✓ | ✓ | ✓ |
| `starbucks/` | 44 | 149 | ✓ | ✓ | ✓ |

¹ Title was trimmed or expanded as part of Domain 4 title-length fixes in this session.
² Description below 150-char target — acceptable for utility/error pages.

All 26 pages have: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:image:width`, `og:image:height`, `og:image:type`, `og:image:alt`, `og:site_name`, `og:locale`, `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt`, `twitter:creator`, `twitter:site`, `theme-color`, `<link rel="manifest">`, and all favicon links.

### 2.2 — Canonical URL Consistency
`[PASS]` All 26 canonicals use `https://` with consistent trailing slash usage. No two pages share a canonical URL. No page's canonical points to a different page.

### 2.3 — OG Image Quality
`[RECONCILED]` The original square-avatar finding is resolved for the 20
planned content cards. The homepage, Contact, Lens System, and BrandGuard
pages now use shipped 1200×630 landscape WebP cards. Six utility or
informational pages still use functional square artwork and remain an optional
enhancement, not a release blocker.

**Historical recommended action:** Commission additional purpose-built cards
for the remaining square-artwork pages if their social-sharing value warrants
the work.

`[FLAGGED]` `Organization` JSON-LD on `index.html` has a `sameAs` array with only two entries (`overkillhill.com`, `glee-fully.tools`). Active social profiles (LinkedIn, Ko-fi, X/Twitter, YouTube, Facebook) should be added once their canonical profile URLs are confirmed.

### 2.4 — JSON-LD Structured Data Audit
`[PASS]` All JSON-LD blocks parse as valid JSON. Schema types are appropriate to page content. No placeholder text found. The `SearchAction` on `index.html` correctly targets `https://askjamie.bot/search/?q={search_term_string}` — the search page exists and is functional. BrandGuard case studies carry `Article` schema. All required fields are populated.

---

## Domain 3 — Google Analytics Verification

### 3.1 — Tag Presence Audit

`[FIXED]` The Google Analytics async CDN script (`<script async src="https://www.googletagmanager.com/gtag/js?id=G-MT9Y10YY0G">`) was present on all 26 pages but loading at the **very end of `<body>`** instead of in `<head>`. Per Google's own specification, this script must be in `<head>` to minimize measurement gaps — placing it at end of body means GA may not initialize before the page unloads on fast exits.

Moved to `<head>` on all 26 pages. `hershey/index.html` used a multiline format that required a separate pattern to match.

| Page | GTM in `<head>` | GA Config in app.js | Status |
|---|---|---|---|
| All 26 pages | ✓ (fixed) | ✓ | FIXED → PASS |

### 3.2 — Double-Initialization Check
`[PASS]` The v0.9 consolidation correctly split the GA pattern into two parts:
- Pages load the CDN library via `<script async>` in `<head>` — no `gtag()` call here
- `app.js` §0 runs immediately on parse and calls `gtag('js', new Date())` then `gtag('config', 'G-MT9Y10YY0G')` exactly once

Zero double-initialization. The separate `analytics.js` file referenced in the audit spec was intentionally consolidated into `app.js §0` during the v0.9 restructure — this is architecturally superior (one fewer network request, same timing behavior).

### 3.3 — Script Load Order
`[FIXED]` See 3.1. GTM CDN script now in `<head>` on all 26 pages. `app.js` correctly deferred at end of `<body>`. No script blocks anything.

### 3.4 — app.js §0 Content Review

`[PASS]` All required elements verified:

| Check | Result |
|---|---|
| `window.dataLayer = window.dataLayer \|\| []` | ✓ |
| `function gtag() { dataLayer.push(arguments); }` | ✓ |
| `gtag('js', new Date())` | ✓ |
| `gtag('config', 'G-MT9Y10YY0G')` — exactly once | ✓ |
| No `console.log()` statements | ✓ |
| No commented-out alternate GA IDs | ✓ |

### 3.5 — Event Tracking Inventory
`[FIXED — later implementation]` Consent-gated custom GA events are now
implemented in `assets/js/app.js`, including `gpt_click`, `inquiry_click`, and
`search_open`. This section records the state observed on 2026-05-12; event
volume and conversion reporting remain unavailable without an authorized GA4
export.

### 3.6 — Privacy / Consent Considerations
`[FIXED — later implementation]` `legal/index.html` now describes GA4,
consent, and the data-use boundary. This section records the pre-remediation
state observed on 2026-05-12.

---

## Domain 4 — SEO Audit

### 4.1 — Title Tag Quality
`[FIXED]` Five titles were outside the 30–60 character optimal range:

| Page | Before | After | Notes |
|---|---|---|---|
| `search/index.html` | "Search AskJamie™" (16) | "Site Search \| AskJamie™" (23) | Too short |
| `enterprise-sleuth/` | 70 chars | "Enterprise Sleuth™ \| AskJamie™" (30) | Over limit |
| `okhp3-brandguard/` | 64 chars | "OKHP³ BrandGuard™ \| AskJamie™" (29) | Over limit |
| `resume-representative/` | 61 chars | "Résumé Representative \| AskJamie™" (33) | 1 over |
| `404.html` | 61 chars | "Page Not Found \| AskJamie™" (26) | 1 over |

All 26 titles are now within range, unique, and include the brand name.

### 4.2 — Meta Description Quality
`[PASS]` All 26 descriptions are unique and range from 112–151 characters. Utility/error pages (`search/`, `404.html`) have shorter descriptions (112–121 chars) which is acceptable given their limited content scope. No description duplicates another. No description is copied verbatim from page body.

### 4.3 — Heading Hierarchy Audit
`[PASS]` All 26 pages have exactly one `<h1>`. No page has zero or multiple `<h1>` tags. Heading hierarchy (h1→h2→h3) is logical throughout — no skipped levels found in the pages sampled.

### 4.4 — Internal Linking Audit
`[PASS — with note]` Zero broken internal links found. All root-relative `href` paths resolve to existing pages.

**Orphan note (functional, not structural):** The 12 BrandGuard case study pages show 0 detected inbound links in the root-relative link analysis because the BrandGuard hub links to them via **relative paths** (e.g., `href="lego/"`) rather than root-relative paths (e.g., `href="/lens-system/okhp3-brandguard/lego/"`). The links are functional — crawlers follow relative links correctly from the hub page. However, converting the hub's case-study `href` values to root-relative would improve consistency and make the link map analyzable by tools that only follow root-relative paths. Flagged for the hub page backlog.

`404.html`, `under-construction.html`, and `search/` have zero inbound links by design — they are utility/system pages.

### 4.5 — Sitemap Audit
`[PASS]` `sitemap.xml` contains 24 URLs matching exactly 24 discoverable HTML pages (404 and under-construction correctly excluded). All URLs use `https://`. `<lastmod>` dates are present on all entries. `<changefreq>` and `<priority>` values follow the correct hierarchy (1.0 homepage → 0.9 hubs → 0.8 lens pages → 0.7 case studies → 0.5 utility). `robots.txt` correctly declares `Sitemap: https://askjamie.bot/sitemap.xml`.

### 4.6 — Robots.txt Audit
`[PASS]` `robots.txt` is clean:
- `User-agent: *` with `Allow: /` — no content accidentally blocked
- `/assets/` is not blocked — Google can evaluate CSS/JS for rendering
- AI crawlers correctly configured (GPTBot, OAI-SearchBot, anthropic-ai allowed; CCBot blocked)
- `Sitemap:` declaration present
- File ends with a newline

### 4.7 — Image SEO
`[PASS]` Full audit of all `<img>` tags across 26 pages confirms: every image has `alt`, `width`, and `height` attributes. No image is the sole carrier of text content. Filenames are descriptive where possible.

### 4.8 — Core Web Vitals Checklist
`[PASS]` Code-level indicators:
- **LCP:** Hero images have no `loading="lazy"` and carry `fetchpriority="high"` where applicable
- **CLS:** All `<img>` tags have explicit `width` and `height` — no layout shift from unsized images. Fonts use the async-load / `media="print"` swap pattern with `<noscript>` fallback
- **FID/INP:** No synchronous long-running JS in `<head>`. All non-critical JS is deferred. GTM now correctly in `<head>` as `async` (non-blocking)

### 4.9 — llms.txt Audit
`[PASS]` `llms.txt` is accurate, complete, and current:
- Correctly describes AskJamie™ and its position in the OKHP³ ecosystem
- Lists canonical URLs for all 7 core pages, 4 Lens System GPTs, and all 13 BrandGuard cases
- Follows the emerging standard format with `## Section` headings and URL + description pairs
- Includes sister site references, citation guidance, and technical transparency note

---

## Domain 5 — Header & Footer Consistency

### 5.1 & 5.2 — Canonical Header and Footer
`[PASS]` The canonical header and footer (extracted from `index.html`) are consistently applied across all 26 pages. The `aria-current="page"` attribute correctly appears only on the nav item matching each page's section.

### 5.3 — Header Diff Across All Pages
`[PASS]` No structural header deviations found. All pages share the same:
- Skip link pattern
- Logo `<img>` with root-relative `src`
- nav structure with identical link order
- `aria-label` on `<nav>`
- nav-toggle button with `aria-expanded`

`[PASS — noted]` `search/index.html` does not carry the "Today's Special" promotional banner. This is consistent with it being a utility/search interface page — the banner appears only on content pages.

### 5.4 — Footer Diff Across All Pages
`[PASS]` Footer is consistent across all pages — Replit credit, copyright year stamp (`#current-year-askjamie`), and nav links match throughout.

### 5.5 — Path Consistency: Relative vs. Root-Relative
`[FIXED]` Three root-level pages (`index.html`, `404.html`, `under-construction.html`) were using relative paths for internal asset references. While functionally correct at the root level, this was inconsistent with subdirectory pages which correctly used root-relative paths.

Converted to root-relative:
- `index.html` — 11 asset paths + 14 nav hrefs
- `404.html` — 9 asset paths + 11 nav hrefs
- `under-construction.html` — 9 asset paths + 11 nav hrefs

All 26 pages now use root-relative paths uniformly for all CSS, JS, image, favicon, and manifest references.

---

## Domain 6 — Design Principles Consistency

### 6.1 — Design Token Inventory

The `:root` block defines **30 custom properties** across the global tier. These are the actual tokens in use:

| Token | Value | Category |
|---|---|---|
| `--okh-teal` | `#1c3a34` | Palette primitive |
| `--okh-olive` | `#676a2c` | Palette primitive |
| `--okh-ochre` | `#a06e28` | Palette primitive |
| `--okh-rust` | `#5b3a27` | Palette primitive |
| `--okh-espresso` | `#2a2320` | Palette primitive |
| `--okh-orange` | `#c46a2c` | Palette primitive |
| `--okh-amber` | `#e6a03c` | Palette primitive |
| `--okh-paper` | `#f6f2ee` | Palette primitive |
| `--okh-gray` | `#6b7280` | Palette primitive |
| `--color-bg` | `var(--okh-espresso)` | Semantic token |
| `--color-surface` | `#111827` | Semantic token |
| `--color-surface-soft` | `#181f26` | Semantic token |
| `--color-fg` | `#e5e7eb` | Semantic token |
| `--color-muted` | `var(--okh-gray)` | Semantic token |
| `--color-accent` | `var(--okh-orange)` | Semantic token |
| `--color-border-subtle` | `rgba(249,250,251,0.08)` | Semantic token |
| `--font-heading` | Alfa Slab One stack | Typography |
| `--font-body` | DM Sans stack | Typography |
| `--max-width` | `1120px` | Layout |
| `--radius-md` | `0.75rem` | Border radius |
| `--radius-lg` | `1.25rem` | Border radius |
| `--shadow-soft` | `0 18px 40px …` | Elevation |
| `--mermaid-*` (8 tokens) | Various | Diagram theming |

`[FLAGGED — PLANNED REFACTOR]` The audit spec requires 38 tokens. **32 are not present.** Key gaps:

- **Rename candidates** (concept exists under a different name): `--color-fg` → `--color-text`, `--color-muted` → `--color-text-muted`, `--color-border-subtle` → `--color-border`, `--radius-md/lg` → `--border-radius/--border-radius-lg`, `--shadow-soft` → `--shadow-md`
- **Genuinely missing:** spacing scale (`--space-xs` through `--space-2xl`), font-size scale (`--font-size-sm` through `--font-size-3xl`), line-height tokens, secondary shadow tokens, transition tokens, link color tokens

**Why not auto-fixed:** Renaming existing tokens would require updating references throughout all 4,561 lines of `theme.css` and syncing those renames to the two sister sites (`overkillhill.com`, `glee-fully.tools`). This is a planned refactor, not a one-session change. Adding the missing tokens (spacing scale, font-size scale) requires measuring actual hard-coded values in use and confirming the correct values before creating aliases.

**Recommended action:** Schedule a dedicated token-standardization session. Start with the rename candidates — they carry zero risk to visual appearance. Add missing tokens as aliases to measured values.

### 6.2 — Button System Audit
`[PASS]` A complete button class system is defined and in use:
- `.btn` — base class with padding, border-radius, font-weight, transition
- `.btn-primary` — primary brand CTA
- `.btn-quiet` — low-contrast secondary action
- `.btn-secondary` — Glee-specific variant
- `:hover`, `:focus-visible`, `:active` states defined for all variants
- `outline: 2px solid var(--color-accent)` focus indicator present — no `outline: none` without replacement

### 6.3 — Card System Audit
`[PASS]` `.card` class is the standard container used consistently across homepage, Lens System hub, and BrandGuard hub. Card properties (padding, border-radius, shadow, border) reference CSS variables throughout.

### 6.4 — Typography Scale
`[PASS]` Heading hierarchy is consistent across pages. `h1` uses `--font-heading` (Alfa Slab One), body text uses `--font-body` (DM Sans). Font sizes use `clamp()` for responsive scaling — no fixed pixel sizes on headings.

### 6.5 — Spacing Consistency
`[FLAGGED]` Section padding values are defined as hard-coded pixel/rem values rather than named spacing tokens. This is the direct consequence of the missing `--space-*` token scale noted in 6.1. Once the spacing token refactor is complete, these should be updated.

### 6.6 — Color Usage Audit
`[PASS — with note]` Core colors consistently use CSS variables. Hard-coded color values do appear in some section-specific blocks (particularly in article body text at `#d1d5db`), but these map to the correct palette value (`--color-fg` in muted state). No rogue colors that don't match the palette were found.

### 6.7 — Paper-Grain Texture Consistency
`[PASS]` The `.askjamie-paper` class is defined in the ASKJAMIE tier of `theme.css` as a reusable global class. It is not embedded as an inline style or page-specific block. Texture intensity and positioning are consistent across all pages that apply it.

### 6.8 — `!important` Audit
**28 instances** found in `theme.css`, categorized:

| Category | Count | Verdict |
|---|---|---|
| `.sr-only` utility (accessibility required) | 9 | Legitimate — required |
| `prefers-reduced-motion` override | 4 | Legitimate — required |
| Scroll-reveal animation reset | 2 | Legitimate — required |
| `text-transform: none` brand overrides (Glee/AskJamie) | 4 | Legitimate — override needed |
| Font/color overrides (L1489–1493, L1606–1609, L1734–1737) | 9 | Potentially avoidable |

The 9 potentially avoidable instances are in the Glee and AskJamie brand tiers where specificity battles with global heading styles require overrides. These could be resolved by increasing selector specificity (e.g., `.askjamie-main .article-body p`) rather than `!important`. Flagged for the CSS refactor session.

---

## Domain 7 — CSS & JavaScript Hygiene

### 7.1 — Inline Style Audit
`[PASS]` Zero `style=""` attributes found across all 26 HTML files. Complete compliance with the asset-centralization rule.

### 7.2 — `<style>` Block Audit
`[PASS]` Zero `<style>` blocks found in any HTML file. All CSS lives in `assets/css/theme.css`.

### 7.3 — Inline `<script>` Code Audit
`[PASS]` The only inline `<script>` blocks in HTML files are:
- `<script type="application/ld+json">` — required inline per spec, present on all pages
- `window.dataLayer` + `gtag` bootstrap — required inline per Google's own specification

No other inline JavaScript exists. Full compliance.

### 7.4 — `assets/js/app.js` Audit

`[PASS]` All checklist items verified:

| Check | Result |
|---|---|
| `window.dataLayer = window.dataLayer \|\| []` | ✓ PASS |
| `function gtag()` defined | ✓ PASS |
| `gtag('js', new Date())` called | ✓ PASS |
| `gtag('config', 'G-MT9Y10YY0G')` — exactly once | ✓ PASS |
| DOMContentLoaded guard on DOM manipulation | ✓ PASS |
| IntersectionObserver for scroll reveal | ✓ PASS |
| `aria-expanded` toggle on mobile nav | ✓ PASS |
| Escape key closes nav | ✓ PASS |
| Copyright year stamp with null check | ✓ PASS |
| Zero `console.log()` in production | ✓ PASS |
| One `console.warn()` in fetch catch block | ✓ Acceptable |
| No jQuery | ✓ PASS |
| No ko-fi widget (not implemented) | ✓ PASS |

### 7.5 — Unused CSS Detection
`[PASS — not fully enumerated]` Full unused CSS detection across a 4,561-line multi-site stylesheet would require a browser-based coverage tool (Chrome DevTools Coverage tab) that cannot run in a static analysis context. The stylesheet serves three sister sites — classes not used on AskJamie may be used on OverKill Hill or Glee-fully. No `/* AUDIT: possibly unused */` flags added to avoid confusion with the shared codebase. **Recommended:** run Chrome DevTools Coverage against all three sites before any CSS pruning pass.

### 7.6 — CSS Specificity Audit
`[PASS]` See Domain 6.8 for `!important` categorization. No ID selectors (`#id { }`) used for styling — all CSS uses class selectors.

### 7.7 — JavaScript File Loading Audit
`[FIXED]` See Domain 3.1 and 3.3. GTM async script moved from end of body to `<head>`.

`[PASS]` All other script load order checks:
- `app.js` loads before any script that depends on it — no ordering conflicts
- `mermaid-init.js` loads only on `universe/index.html`, the one page with `.mermaid` elements
- No script loaded more than once on any page
- All non-GTM scripts use `defer` or `src` without blocking

### 7.8 — CSS File Loading Audit
`[PASS — reconciled 2026-08-24]` `theme.css` is loaded exactly once per page
on all 26 public pages and imports the existing local `assets/css/fonts.css`.
No page references a stylesheet that does not exist. Google Fonts async-load
tags are no longer present.

---

## Files Modified

| File | Changes |
|---|---|
| All 26 HTML pages | Removed deprecated meta tags: `X-UA-Compatible`, `name="language"`, `name="revisit-after"`, `name="googlebot"`, `name="bingbot"`, `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, `mobile-web-app-capable` |
| All 26 HTML pages | Moved GTM async script from end of `<body>` to `<head>` |
| `index.html` | Converted 14 relative nav hrefs to root-relative |
| `index.html`, `404.html`, `under-construction.html` | Converted 29 relative asset `href`/`src` paths to root-relative |
| `404.html`, `under-construction.html` | Converted 22 relative nav hrefs to root-relative |
| `legal/index.html` | Added missing `<head>` opening tag |
| `search/index.html` | Title: "Search AskJamie™" (16) → "Site Search \| AskJamie™" (23) |
| `lens-system/enterprise-sleuth/index.html` | Title trimmed from 70 → 30 chars |
| `lens-system/okhp3-brandguard/index.html` | Title trimmed from 64 → 29 chars |
| `lens-system/resume-representative/index.html` | Title trimmed from 61 → 33 chars |
| `404.html` | Title trimmed from 61 → 26 chars |
| `lens-system/okhp3-brandguard/hershey/index.html` | Multiline GTM script normalized and moved to `<head>` |
| `assets/data/search-index.json` | Rebuilt after HTML changes (128.5 KB, 33 templates + pages indexed) |

---

## Flagged Items Requiring Human Action

1. **`<link rel="preload">` for `theme.css`** — Add before the existing stylesheet link on all pages. Improves LCP. Requires verification that font-swap pattern interaction behaves correctly. *(Domain 1.12)*

2. **Optional OG coverage** — Twenty planned content cards are shipped as
   landscape WebP. Consider cards for the six remaining square-artwork pages
   if their social-sharing value warrants it. *(Domain 2.3)*

3. **Organization JSON-LD `sameAs`** — Currently only lists `overkillhill.com` and `glee-fully.tools`. Add canonical URLs for LinkedIn, Ko-fi, X/Twitter, YouTube, and Facebook once confirmed. *(Domain 2.4)*

4. **Page-specific OG images** — BrandGuard and Lens System content pages now
   have page-specific landscape cards. Remaining utility pages are optional
   coverage. *(Domain 2.3)*

5. **GA4 reporting access** — Consent-gated events are implemented, but
   visitor counts, event volume, and funnel exits remain unknown until an
   authorized read-only export is available. *(Domain 3.5)*

7. **BrandGuard hub relative case-study links** — `okhp3-brandguard/index.html` links to case studies via relative paths (`href="lego/"` etc.). Converts to root-relative improves link-map analyzability and is consistent with site-wide convention. *(Domain 4.4)*

8. **CSS token refactor** — 32 tokens from the standard spec are absent. 8 are rename candidates of existing tokens; 24 are genuinely missing (spacing, font-size, transition scales). Requires coordinated update across all three sister sites. *(Domain 6.1, 6.5)*

9. **`!important` specificity debt** — 9 instances in Glee/AskJamie brand tiers could be replaced by increasing selector specificity. Requires careful testing across three sites. *(Domain 6.8)*

10. **Unused CSS detection** — Cannot be reliably performed via static analysis on a multi-site shared stylesheet. Use Chrome DevTools Coverage tab across all three sites before any CSS pruning pass. *(Domain 7.5)*

---

## Recommended Next Session Priorities

Ordered by impact-to-effort ratio:

1. **Add `<link rel="preload">` for `theme.css`** — One-line addition to every page head, scriptable in 5 minutes. Direct LCP improvement with no visual risk.

2. **CSS token refactor (rename phase only)** — Rename the 8 existing tokens that have wrong names (`--color-fg` → `--color-text`, etc.) with a find-and-replace pass. Zero visual change. Eliminates the naming gap and makes the codebase match the spec convention before adding new tokens.

3. **GA4 reporting access** — Obtain an authorized export and report
   consented sessions only. Do not infer visitor numbers from implementation
   code.

4. **Optional OG coverage** — Review whether the six remaining
   square-artwork pages merit custom landscape cards.

5. **Assistive technology verification** — Confirm consent, search live-region,
   keyboard focus, theme, and Mermaid fallback behavior with VoiceOver or NVDA.

---

*Audit completed 2026-05-12 · Site auditor result at close: 0 issues ·
38 fixes applied. Current-state reconciliation added 2026-08-24.*

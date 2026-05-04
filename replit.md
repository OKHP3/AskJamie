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
  css/theme.css        # Main stylesheet — reorganised v0.4 into 4 stable tiers:
                       #   1. GLOBAL   (21 sections, ~2420 lines)
                       #   2. OKH      ( 3 sections, ~271 lines)
                       #   3. GLEE     ( 9 sections, ~745 lines)
                       #   4. ASKJAMIE ( 5 sections, ~570 lines)
                       # SECTION INDEX at top of file lists every section + line range
  js/app.js            # Single consolidated JS file (v0.9) — all four modules in one:
                       #   §0 Analytics   — GA4 gtag bootstrap (inline, replaces analytics.js)
                       #   §1a Search     — modal overlay, keyboard nav, lazy index fetch
                       #                    (inline, replaces search.js)
                       #   §1b Search pg  — dedicated /search/ page logic, category chips
                       #                    (inline, replaces search-page.js)
                       #   §1c–§1d        — reading progress bar, sticky TOC scroll-follow
                       #   §2             — mobile nav, theme toggle, year stamps,
                       #                    scroll reveal, smooth anchor scroll,
                       #                    under-construction overlay
  js/mermaid-init.js   # Mermaid v11 ESM diagram initialization (external file, no inline scripts)
  data/search-index.json  # Pre-built static search index (~100 KB, ~25 KB gzipped)
  img/                 # Brand assets, avatars, case study images
  img/favicons/        # Full favicon set (ico, 16/32/48px PNG, SVG, android-chrome, apple-touch)
tools/
  audit-site.py           # Static-site auditor (v0.8) — 17 quality gates:
                          # 13 per-page + 2 cross-file reconciliations +
                          # 2 repo-wide. Writes tools/audit-report.md.
                          # Current run: 0 issues (post v0.9 consolidation).
  apply-modern-baseline.py # Idempotent 2025/2026 baseline applier:
                          # injects security meta tags (referrer + CSP),
                          # adds loading=lazy/eager + fetchpriority=high
                          # to every <img>. Safe to re-run on new pages.
  build-search-index.py   # Regenerates assets/data/search-index.json from all .html files
  enhance-pages.py        # Bulk-edit tool for site-wide HTML enhancements (v0.5)
  restructure-theme.py    # Deterministic theme.css reorganiser (GLOBAL→OKH→GLEE→ASKJAMIE)
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

## Three-Site CSS/JS Sync Workflow (v0.4)

`theme.css`, `app.js`, `analytics.js`, `search.js`, and `mermaid-init.js`
are the **shared** front-end source of truth for three sister sites:

| Site                      | Domain               | Body class       |
| ------------------------- | -------------------- | ---------------- |
| OverKill Hill P³          | overkillhill.com     | (none — default) |
| Glee-fully Tools          | glee-fully.tools     | `.glee-main`     |
| AskJamie                  | askjamie.bot         | `.askjamie-main` |

Brand differences are expressed entirely through CSS body-class scoping
(`.glee-main .foo {}`, `.askjamie-main .bar {}`, `body:not(...)` for OKH).
No brand-specific JS exists.

**Update workflow:** edit any one repo, then paste the changed file into
the other two repos so all three stay in lock-step.  Section ordering in
`theme.css` is stable (GLOBAL → OKH → GLEE → ASKJAMIE) so diffs land in
predictable regions.

## Mermaid pages — affiliate referral convention (2026-05-03)

Any AskJamie page that embeds a Mermaid diagram (i.e. contains
`<pre class="mermaid">`) **must** also include an OKH affiliate
referral link directly under the diagram. This is enforced by
`tools/audit-site.py` — the auditor flags any Mermaid page missing
either the link or the styling class.

**Required markup** (place directly inside the same `<figure>`, after
the diagram and any captions):

```html
<p class="mermaid-referral-note">
    Diagram rendered with Mermaid.js.
    <a href="https://mermaidchart.cello.so/UhVlNtC2MlS"
       class="mermaid-referral-link"
       target="_blank" rel="noopener noreferrer">Try Mermaid.AI &#8594;</a>
    if you want to explore the syntax yourself.
</p>
```

- **Affiliate URL:** `https://mermaidchart.cello.so/UhVlNtC2MlS`
  (Jamie's paid-referral link — do not change)
- **Color:** Mermaid hot pink **#FF3670** (hover **#ff6b95**) — defined
  by `a.mermaid-referral-link` in the ASKJAMIE tier of `theme.css`
- **Reference page:** `overkillhill.com/writings/first-diagram-is-a-liar`
  uses the identical pattern across the OKH site
- **Currently used on:** `universe/index.html` (only Mermaid page on
  the site as of 2026-05-03)

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

## Internal Site Search (v0.3 — 2026-04-11)

A zero-dependency, fully static, client-side search engine.

- **Trigger:** Pill button in the right side of the site header on every page (label hidden < 720px, kbd hint hidden < 720px).
- **Keyboard:** `/` or `Cmd/Ctrl+K` to open · `↑↓` to navigate results · `Enter` to open · `Esc` to close.
- **Index:** `assets/data/search-index.json` — generated by `tools/build-search-index.py` from every `.html` file (excluding `404.html` and `under-construction.html`). Each record stores: url, title, description, section label, h1, h2/h3 list, body excerpt (capped at 4000 chars per page).
- **Loading:** lazy — `search.js` is injected by `app.js` after DOM parse; the index JSON is fetched only when the user opens the modal.
- **Scoring:** title match (10) > h1 (8) > description (5) > headings (4) > section (3) > body (1), plus phrase-match and all-tokens-in-title bonuses, with a small boost for shallower URLs.
- **Rebuilding:** run `python3 tools/build-search-index.py` after any HTML/copy change.

## Site Audit Findings (2026-04-11)

Documented for future cleanup work. None of these are bugs in the current ship; they are enhancement targets.

**Orphaned/underlinked pages:**
- 4 BrandGuard case studies (`coca-cola`, `dollar-general`, `lego`, `mathews-archery`) have **0 inbound links** from any other page on the site. They appear in `sitemap.xml` and are now reachable via the new search.
- 8 of the remaining 12 BrandGuard cases have only 1 inbound link each (the BrandGuard hub page lists only the BFS case in the body). Adding a "More BrandGuard cases" grid is the recommended fix.

**Orphaned image assets:**
- 103 of 118 images (~87%) are not referenced anywhere. Major buckets:
  - ~60 AskJamie character/title PNGs (color-variant brand library, never placed on a page)
  - All 12 `BrandGuard/Company Logos/*.png` (Brooks, Coca-Cola, Costco, Discount Tire, Dollar General, Hershey, Lego, LVMH, Mathews Archery, Ping, Scheels, Starbucks)
  - All 12 `BrandGuard/OverKill Hill P³ GPT-BRG*.png` protection icons
  - `ErrorExplosion1.png`, `ErrorExplosion2.png`, `Under Construction with Heart Elements.png`
  - `favicon.svg`, `favicon.png`, `favicon.webp`, `favicon-48x48.png` (only the 16/32/180 ICO+PNG variants are declared in `<link rel="icon">`)

**Metadata over-length issues:**
- 17 pages have meta descriptions > 165 chars (will truncate in SERPs). Longest is `lego` at 299 chars.
- 2 pages have titles > 70 chars: `enterprise-sleuth` (80) and `okhp3-brandguard/index` (75).

## CSS / JS Restructure (v0.4 — 2026-05-02)

`assets/css/theme.css` was reorganised from a chronological "newest at the
bottom" layout into four stable tiers (GLOBAL → OKH → GLEE → ASKJAMIE).
Every section now has exactly one home and a SECTION INDEX comment at the
top of the file lists each section's source-line range.

`assets/js/app.js` was reorganised into self-initializing IIFEs followed
by a single DOM-ready bootstrap.  A redundant `DOMContentLoaded` handler
whose target element didn't exist yet was removed (it was causing a
latent dark→light theme flash on subsite navigation).

Inline-content best-practice audit re-ran clean:
- **0** `<style>` blocks across all 25 HTML files
- **0** `style="..."` attributes across all 25 HTML files
- **0** real inline `<script>` blocks — the 25 identical Google Analytics
  `gtag()` configs were moved to `assets/js/analytics.js` and pages now
  load it via `<script defer src="/assets/js/analytics.js"></script>`.
- 26 JSON-LD blocks intentionally remain inline — Google's structured-data
  spec requires `<script type="application/ld+json">` to be in-page.

Backups: `assets/css/theme.css.bak` (original) and
`assets/css/theme.css.pre-reorder.bak` (pre-v0.4 working file) are kept
in the tree but excluded from any future commits.

## Showpiece Pass (v0.5 — 2026-05-02)

A site-wide enhancement pass to maximize value as a "showpiece" GitHub
Pages site:

- **Built-with-Replit footer credit** added to every page (matching the
  orange Replit link styling on `overkillhill.com`).  Layout is a flex
  row with the badge left-aligned and the © line optically centred.
  Referral target: `https://replit.com/refer/overkillhillp3/`.
- **`llms.txt`** added at the root for LLM crawler guidance.
- **Article JSON-LD** added to all 13 BrandGuard case studies.
- **BreadcrumbList JSON-LD** added to all 22 eligible inner pages
  (everything except homepage, 404, under-construction).
- **GTM preconnect** added to all 25 pages.
- **All 13 BrandGuard cases grid** added to the BrandGuard hub —
  resolves 4 previously orphaned cases (`coca-cola`, `dollar-general`,
  `lego`, `mathews-archery`) and surfaces all 12 previously-unused
  `Company Logos/*.png` assets.
- **Image attribute polish** — 78 imgs got `decoding="async"`,
  7 below-the-fold imgs got `loading="lazy"` (first-2 left eager for
  LCP).
- **21 over-length meta descriptions** tightened to ≤165 chars.
- **2 over-length titles** tightened to ≤70 chars.
- **`sitemap.xml`** rewritten with `<lastmod>` tags on every URL.
- **Search index bugfix** — `tools/build-search-index.py` was producing
  0-byte body excerpts for every page because (a) `STRIP_CLASSES_CONTAINS`
  was stripping the `askjamie-paper` content wrapper, and (b) HTML5 void
  elements (`<img>`, `<br>`, …) were polluting the parser's tag stack.
  Fixed both; index is now 100.6 KB with 79,965 body chars.
- **`mathews-archery` canonical typo** fixed.

`tools/enhance-pages.py` is the new idempotent bulk-edit tool that
applied most of the above.  Safe to re-run any time.

## Known Gaps (require manual action)

- **OG images:** All pages use a square 1024×1024 avatar PNG as OG image. The gold standard recommends 1200×630 landscape. A purpose-built landscape OG image would improve social card display.
- **Search Console submission:** `sitemap.xml` should be submitted to Google Search Console and Bing Webmaster Tools.
- **Sister-site sync:** v0.4 + v0.5 + v0.6 + v0.7 changes (`theme.css`,
  `app.js`, `analytics.js`, `tools/build-search-index.py`,
  `tools/audit-site.py`) must still be copied into the OverKill Hill
  and Glee-fully repos for visual + tooling parity. AskJamie also adds
  a fresh `llms.txt` whose URL list will need to be swapped per-site if
  those repos want their own.

## Audit & Quality Gates (v0.7 — 2026-05-03)

`tools/audit-site.py` is the repo's reproducible quality gate.

```
python3 tools/audit-site.py            # writes tools/audit-report.md
python3 tools/audit-site.py --quiet    # same, no per-page console output
```

It walks every `.html` file in the repo (excluding `.local/`,
`attached_assets/`, `.cache/`, `node_modules/`, `.git/`) and checks:

- title length (≤70), description length (≤165), missing description
- exactly one `<h1>`, missing canonical, missing OG fields
- every `<img>` has `alt`, `width`, `height`
- every external `target="_blank"` link has `rel="noopener noreferrer"`
- known placeholders (`ASK-JAMIE-GPT-ID-HERE`, old SearchAction
  `?s={…}` target, generic `YOUR-…` strings)
- `theme-color` resolves to the AskJamie brand teal `#2c5e6f`
- sitemap ↔ on-disk pages reconciliation
- search-index ↔ on-disk pages reconciliation

**Run-it-after rule:** any HTML edit, any new page, any sitemap or
search-index change. Current state: **0 issues across 26 HTML files.**

## Latest Audit Cycle (v0.7 — 2026-05-03)

See `AUDIT-ASKJAMIE-FINAL.md` for the full v2.0 cycle write-up. Quick
summary of what changed since v0.6:

- New `tools/audit-site.py` (above).
- Reusable `.brandguard-demo-notice` block injected on all 13
  BrandGuard case pages, with matching CSS in the ASKJAMIE tier of
  `theme.css`. Each notice links to `/legal/`.
- Homepage hero CTA cluster expanded from 1 button to 3
  (Lens System / BrandGuard / Contact) with `flex-wrap` so it stacks
  on mobile.
- Four broken internal links repaired in the BrandGuard hub
  ("Part of the AskJamie portfolio" cards).
- Site-wide `theme-color` sweep: 16 pages had dark-template or
  brand-of-the-page values; all now resolve to the brand teal.
- "Discount Tires" → "Discount Tire" typo fix in the universe Mermaid.
- Documentation refresh: this file, `CHANGELOG.md` (v0.7),
  `ROADMAP.md`, `README.md` ("Resume" → "Résumé").

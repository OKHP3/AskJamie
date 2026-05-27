# AskJamie™ Template Library
## /assets/templates/

Created: 2026-05-03
Total templates: 9
Maintained: manually (templates are hand-edited source-of-truth files)

---

## Page Inventory (Phase 13.1)

Every `.html` file in the repo (26 total), with its assigned Page Type
and which template covers it.

| #  | File path (relative to root)                                                | Page Title                       | Page Type         | Template |
|---:|-----------------------------------------------------------------------------|----------------------------------|-------------------|----------|
|  1 | `index.html`                                                                | Homepage                         | `homepage`        | `template--homepage.html` |
|  2 | `about/index.html`                                                          | About                            | `interior-single` | `template--interior-single.html` |
|  3 | `contact/index.html`                                                        | Contact                          | `interior-form`   | `template--interior-form.html` |
|  4 | `legal/index.html`                                                          | Legal                            | `interior-single` | `template--interior-single.html` |
|  5 | `universe/index.html`                                                       | OKHP³™ Universe                  | `interior-single` | `template--interior-single.html` |
|  6 | `search/index.html`                                                         | Search AskJamie™                 | `utility`         | `template--utility.html` |
|  7 | `404.html`                                                                  | 404 — Page Not Found             | `error`           | `template--error.html` |
|  8 | `under-construction.html`                                                   | Under Construction               | `holding`         | `template--holding.html` |
|  9 | `lens-system/index.html`                                                    | Lens System Hub                  | `hub`             | `template--hub.html` |
| 10 | `lens-system/okhp3-brandguard/index.html`                                   | BrandGuard™ Hub                  | `hub`             | `template--hub.html` |
| 11 | `lens-system/resume-representative/index.html`                              | Lens 01 — Résumé Representative  | `lens-detail`     | `template--lens-detail.html` |
| 12 | `lens-system/professional-portfolio/index.html`                             | Lens 02 — Professional Portfolio | `lens-detail`     | `template--lens-detail.html` |
| 13 | `lens-system/enterprise-sleuth/index.html`                                  | Lens 03 — Enterprise Sleuth      | `lens-detail`     | `template--lens-detail.html` |
| 14 | `lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/index.html`   | BrandGuard — BFS                 | `case-study`      | `template--case-study.html` |
| 15 | `lens-system/okhp3-brandguard/lego/index.html`                              | BrandGuard — LEGO                | `case-study`      | `template--case-study.html` |
| 16 | `lens-system/okhp3-brandguard/starbucks/index.html`                         | BrandGuard — Starbucks           | `case-study`      | `template--case-study.html` |
| 17 | `lens-system/okhp3-brandguard/brooks-running/index.html`                    | BrandGuard — Brooks Running      | `case-study`      | `template--case-study.html` |
| 18 | `lens-system/okhp3-brandguard/ping/index.html`                              | BrandGuard — Ping                | `case-study`      | `template--case-study.html` |
| 19 | `lens-system/okhp3-brandguard/costco/index.html`                            | BrandGuard — Costco              | `case-study`      | `template--case-study.html` |
| 20 | `lens-system/okhp3-brandguard/hershey/index.html`                           | BrandGuard — Hershey             | `case-study`      | `template--case-study.html` |
| 21 | `lens-system/okhp3-brandguard/lvmh/index.html`                              | BrandGuard — LVMH                | `case-study`      | `template--case-study.html` |
| 22 | `lens-system/okhp3-brandguard/dollar-general/index.html`                    | BrandGuard — Dollar General      | `case-study`      | `template--case-study.html` |
| 23 | `lens-system/okhp3-brandguard/coca-cola/index.html`                         | BrandGuard — Coca-Cola           | `case-study`      | `template--case-study.html` |
| 24 | `lens-system/okhp3-brandguard/discount-tire/index.html`                     | BrandGuard — Discount Tire       | `case-study`      | `template--case-study.html` |
| 25 | `lens-system/okhp3-brandguard/scheels/index.html`                           | BrandGuard — Scheels             | `case-study`      | `template--case-study.html` |
| 26 | `lens-system/okhp3-brandguard/mathews-archery/index.html`                   | BrandGuard — Mathews Archery     | `case-study`      | `template--case-study.html` |

26 pages → 9 distinct Page Types → 9 templates.

---

## Available Templates

### `template--homepage.html`
- **Page type:** `homepage`
- **Source page:** `index.html`
- **Use for:** the root index page only. Full-width hero, multi-section
  layout, "Today's Special" banner, multi-CTA hero cluster.
- **Required tokens:** `[[PAGE-TITLE]]`, `[[PAGE-DESCRIPTION]]`,
  `[[CANONICAL-URL]]`, `[[OG-TITLE]]`, `[[OG-DESCRIPTION]]`,
  `[[OG-URL]]`, `[[OG-IMAGE-URL]]`, `[[OG-IMAGE-ALT]]`,
  `[[HERO-HEADING]]`, `[[HERO-SUBTITLE]]`, `[[HERO-TAGLINE]]`,
  `[[SECTION-HEADING]]` (×N), `[[CARD-OR-ARTICLE-TITLE]]` (×N),
  `[[SCHEMA-TYPE]]`.
- **Optional tokens:** `[[TODAYS-SPECIAL-URL]]`, `[[TODAYS-SPECIAL-TEXT]]`
  (only if the banner is active for the launch).

### `template--interior-single.html`
- **Page type:** `interior-single`
- **Source page:** `about/index.html`
- **Use for:** standard interior pages with no form and no card grid
  (About, Legal, Universe, future single-prose pages).
- **Required tokens:** as homepage minus the multi-CTA hero cluster.
- **Optional tokens:** `[[BREADCRUMB-LABEL]]`, `[[SECTION-NOTE]]`.

### `template--interior-form.html`
- **Page type:** `interior-form`
- **Source page:** `contact/index.html`
- **Use for:** an interior page whose primary interactive element is a
  contact-style block (mailto, address, intake details).
- **Required tokens:** as `interior-single` plus `[[CTA-LABEL]]`,
  `[[CTA-URL]]` for the primary CTA.

### `template--hub.html`
- **Page type:** `hub`
- **Source page:** `lens-system/okhp3-brandguard/index.html`
- **Use for:** any directory/index page that lists child items in a card
  grid. Currently used by the Lens System hub and the BrandGuard hub.
- **Required tokens:** as `interior-single`, plus repeated
  `[[CARD-OR-ARTICLE-TITLE]]`, `[[BODY-COPY]]`, `[[CTA-LABEL]]`,
  `[[CTA-URL]]` per card.

### `template--lens-detail.html`
- **Page type:** `lens-detail`
- **Source page:** `lens-system/resume-representative/index.html` (deepest
  / most representative of the three lens pages)
- **Use for:** an individual lens page inside `/lens-system/`.
- **Required tokens:** lens-specific —
  `[[LENS-NUMBER]]`, `[[LENS-NAME]]`, `[[LENS-TAGLINE]]`,
  `[[GPT-URL]]`, plus the standard interior-single tokens.

### `template--case-study.html`
- **Page type:** `case-study`
- **Source page:** `lens-system/okhp3-brandguard/lego/index.html`
- **Use for:** any new BrandGuard™ case-study page. Includes the
  reusable demo-notice block above `</main>`.
- **Required tokens:** `[[CASE-STUDY-BRAND]]`, `[[GPT-URL]]`, plus the
  standard interior tokens. Demo-notice copy is shared and should be
  left intact.

### `template--error.html`
- **Page type:** `error`
- **Source page:** `404.html`
- **Use for:** any HTTP error page (404, 410, 500, etc.).
- **Required tokens:** `[[HERO-HEADING]]`, `[[HERO-SUBTITLE]]`,
  `[[HERO-TAGLINE]]`, `[[CTA-LABEL]]`, `[[CTA-URL]]`,
  `[[SECTION-HEADING]]`, plus three `[[CARD-OR-ARTICLE-TITLE]]` /
  `[[BODY-COPY]]` pairs.

### `template--holding.html`
- **Page type:** `holding`
- **Source page:** `under-construction.html`
- **Use for:** any "coming-soon" or under-construction holding page.
- **Required tokens:** as `error`, plus the disabled-CTA pattern
  (`btn-disabled`, `aria-disabled="true"`).

### `template--utility.html`
- **Page type:** `utility`
- **Source page:** `search/index.html`
- **Use for:** any single-purpose utility page (search, future stats
  pages, etc.) that doesn't fit the standard interior shape.
- **Required tokens:** minimal —
  `[[PAGE-TITLE]]`, `[[PAGE-DESCRIPTION]]`, `[[CANONICAL-URL]]`,
  `[[OG-*]]`, `[[HERO-HEADING]]`, plus any utility-specific JS hooks
  (preserved as IDs in the template).

---

## Token Reference

All tokens used by the generator. Each template file contains a subset.

| Token                          | Description                                                            | Required in                  |
|--------------------------------|------------------------------------------------------------------------|------------------------------|
| `[[PAGE-TITLE]]`               | Full browser tab title (≤70 chars)                                     | All                          |
| `[[PAGE-DESCRIPTION]]`         | Meta description (150–160 chars)                                       | All                          |
| `[[CANONICAL-URL]]`            | Canonical URL for this page                                            | All                          |
| `[[OG-TITLE]]`                 | Open Graph title                                                       | All                          |
| `[[OG-DESCRIPTION]]`           | Open Graph description                                                 | All                          |
| `[[OG-URL]]`                   | Open Graph URL (matches canonical)                                     | All                          |
| `[[OG-IMAGE-URL]]`             | Open Graph image, full URL                                             | All                          |
| `[[OG-IMAGE-ALT]]`             | Open Graph image alt text                                              | All                          |
| `[[TWITTER-TITLE]]`            | Twitter card title                                                     | All                          |
| `[[TWITTER-DESCRIPTION]]`      | Twitter card description                                               | All                          |
| `[[TWITTER-IMAGE-URL]]`        | Twitter card image                                                     | All                          |
| `[[TWITTER-IMAGE-ALT]]`        | Twitter card image alt                                                 | All                          |
| `[[SCHEMA-TYPE]]`              | JSON-LD `@type` value (WebPage, Article, BreadcrumbList, etc.)         | All                          |
| `[[BREADCRUMB-LABEL]]`         | Eyebrow breadcrumb label inside the hero                               | Most                         |
| `[[HERO-HEADING]]`             | The single H1 inside the hero section                                  | All                          |
| `[[HERO-SUBTITLE]]`            | Hero subtitle paragraph                                                | Most                         |
| `[[HERO-TAGLINE]]`             | Hero tagline paragraph (smaller, supporting)                           | Some                         |
| `[[SECTION-HEADING]]`          | Any H2 inside `<main>`                                                 | Most                         |
| `[[CARD-OR-ARTICLE-TITLE]]`    | Any H3 inside a card or article block                                  | Most                         |
| `[[SECTION-NOTE]]`             | Italic-tone explanatory note paragraph                                 | Some                         |
| `[[BODY-COPY]]`                | Generic paragraph body content                                         | Most                         |
| `[[CTA-LABEL]]`                | Button or link text for a primary/quiet CTA                            | Where applicable             |
| `[[CTA-URL]]`                  | href for that CTA                                                      | Where applicable             |
| `[[IMAGE-SRC]]`                | Page-specific image src (nav/footer logos are NOT tokenised)           | Most                         |
| `[[IMAGE-ALT]]`                | Page-specific image alt                                                | Most                         |
| `[[LENS-NUMBER]]`              | Two-digit lens number (01, 02, 03, …)                                  | `lens-detail`                |
| `[[LENS-NAME]]`                | Lens display name                                                      | `lens-detail`                |
| `[[LENS-TAGLINE]]`             | Lens one-line tagline                                                  | `lens-detail`                |
| `[[CASE-STUDY-BRAND]]`         | Brand name for the BrandGuard™ case                                    | `case-study`                 |
| `[[GPT-URL]]`                  | URL of the live custom GPT                                             | `case-study`, `lens-detail`  |
| `[[TODAYS-SPECIAL-URL]]`       | href for the "Today's Special" banner link                             | Optional, all                |
| `[[TODAYS-SPECIAL-TEXT]]`      | Banner body text                                                       | Optional, all                |

---

## How to Use a Template

1. Copy the desired template file to the target directory and rename it
   `index.html`.
2. Open the file and use Find & Replace to locate all `[[` tokens.
3. Replace each token with real content appropriate to the page.
4. Update the `<link rel="canonical">` href.
5. Update `og:url`, `og:title`, `og:description`, `og:image` meta tags.
6. Replace the JSON-LD placeholder object with the page-specific schema.
7. **Remove** the template header comment block at the top of the file.
8. Add any page-specific CSS classes or JS as needed without modifying
   shared files (`/assets/css/theme.css`, `/assets/js/app.js`).
9. Test on mobile and desktop.
10. Run `python3 scripts/audit-site.py` and `python3 scripts/build-search-index.py`
    before committing.

---

## Adding a New Template

If a new page type is introduced that doesn't match any existing template:

1. Build the new page using the closest existing template as a starting point.
2. Once the page is production-ready, manually create a new template file
   from it: copy the production page, apply the tokenisation rules, add the
   header comment block, and add TEMPLATE SECTION comments above each
   `<section>` inside `<main>`.
3. Add a row to the Page Inventory table in this INDEX.md.
4. Add a subsection to Available Templates and rows to the Token Reference.
5. Commit the new page, the new template, and the updated INDEX together.

Excluded from `python3 scripts/audit-site.py` via the `templates/`
exclusion in `EXCLUDE_DIRS` (added v0.7).

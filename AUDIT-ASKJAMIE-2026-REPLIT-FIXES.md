# AskJamie™ — Replit Fix Log: Task #1 (2026 Site Polish & Responsive QA)
*Completed: 2026-05-26*

## Overview

This document records every change applied during Task #1, plus deferred items
that require owner action and Notion catalog sync notes.

---

## Changes Applied

### Step 1 — Construction overlay removal (6 pages)

All 6 publicly-linked, content-rich pages had their blocking `.construction-overlay`
modal removed entirely:

- `lens-system/index.html`
- `lens-system/enterprise-sleuth/index.html`
- `lens-system/okhp3-brandguard/index.html`
- `lens-system/okhp3-brandguard/lego/index.html`
- `lens-system/professional-portfolio/index.html`
- `lens-system/resume-representative/index.html`

`assets/js/app.js`: construction-overlay dismiss block removed from the
`DOMContentLoaded` bootstrap. `isAnotherOverlayOpen()` retained as a no-op stub
for future use. Stale localStorage keys (`glee-wip-dismissed:*`) will harmlessly
linger in returning visitors' browsers.

### Step 2 — BFS legal copy fix (index.html)

Changed:
> "built exclusively for Builders FirstSource"

To:
> "A public-information BrandGuard™ case study focused on Builders FirstSource."

All 13 BrandGuard case pages already carry the `.brandguard-demo-notice` block
(added in v0.7) linking to `/legal/` — no further copy changes needed.

### Step 3 — Copyright year static fallback (all 33 pages)

Changed `<span id="current-year-askjamie"></span>` to
`<span id="current-year-askjamie">2026</span>` across all 33 HTML files
(including templates, 404, and under-construction). The `app.js` year-stamp
logic already replaces `.textContent` so the static fallback becomes invisible
with JS enabled, but renders correctly without it.

### Step 4 — GA4 custom event tracking (app.js)

New `_gtag_event()` wrapper (exposed as `window._gtag_event`) guards all events
with `typeof gtag === 'function'`. Events added:

| Event name | Trigger |
|------------|---------|
| `cta_click` | Any `.btn-primary` or `.btn` click |
| `outbound_click` | Any `target="_blank"` link click |
| `mermaid_affiliate_click` | MermaidChart affiliate link specifically |
| `contact_click` | Any `mailto:` link click |
| `search_open` | Search modal opened (§1a `openModal()`) |
| `search_submit` | Search query run (§1a `runSearch()`, fires only when index is loaded) |

Ko-fi, Fiverr, ChatGPT GPT, LinkedIn, YouTube, Facebook outbound links are
labelled specifically via the `event_label` field in `outbound_click`.

### Step 5 — Contact page upgrade (contact/index.html)

Expanded from a single card to two sections:

1. **Reach out directly** — email address, response time (1–2 business days),
   Central Time note, privacy guidance for sensitive pre-NDA information.
2. **Inquiry paths** — six labeled cards with subject-line tags:
   `[BrandGuard]`, `[Resume Representative]`, `[Professional Portfolio]`,
   `[Enterprise Sleuth]`, `[Architecture]`, `[Collaboration]`.

### Step 6 — Search footer link (all 28 applicable pages)

Added `<li><a href="/search/">Search</a></li>` to the footer Navigation column
on 28 pages. The header search trigger (`.site-search-trigger`) is always
visible in the header; no `display: none` breakpoint issues found.

### Step 7 — Responsive QA script (scripts/responsive-qa.mjs)

Created `scripts/responsive-qa.mjs` — a dual-mode script that:
- Runs full Playwright headless browser checks if Playwright is available
- Falls back to lightweight static HTML analysis when it isn't

Covers 24 public pages × 8 viewport widths. Results written to
`assets/docs/responsive-qa/results.json`. Screenshots saved only on failure.

### Step 8 — CSS grid / tablet layout fixes (theme.css)

- **Removed duplicate `.grid` declaration** (two identical blocks existed at
  lines ~233 and ~241 in the original file).
- **Fixed `.grid-3` breakpoints:** now shows 2 columns at 769–1024 px (tablet)
  instead of collapsing to 1 column at 1024 px.

**Sister-site sync required** for `overkillhill.com` and `glee-fully.tools`
CSS files — same `.grid` / `.grid-3` changes.

### Step 9 — Accessibility spot-check

Five pages checked (homepage, Lens System hub, BrandGuard hub, Universe, Contact):

- ✅ Skip link present and functional
- ✅ Single `<h1>` per page
- ✅ Landmarks: `<header>`, `<nav>` (with `aria-label`), `<main>`, `<footer>`
- ✅ All `<img>` have `alt` attributes
- ✅ Universe Mermaid diagram has `<figcaption>` fallback
- ✅ No construction overlays remain

No structural issues found; no changes required.

### Step 10 — OG image requirements doc

Created `assets/docs/og-image-requirements.md` specifying required 1200×630
landscape OG images for 5 priority pages + 4 Lens System GPT pages + 12 BrandGuard
case studies (via a shared template). Includes composition guidance, asset
adaptation notes, and per-page update instructions.

### Step 11 — Sitemap / robots.txt / llms.txt alignment

All three files verified clean:

- **sitemap.xml**: 24 public URLs, all with `<lastmod>`. Mathews Archery
  (`/lens-system/okhp3-brandguard/mathews-archery/`) present. No
  `under-construction.html` entry.
- **robots.txt**: `Disallow: /under-construction.html` present; `Sitemap:
  https://askjamie.bot/sitemap.xml` present.
- **llms.txt**: Lists all 24 public pages including all 13 BrandGuard cases.
  BRG12 (Mathews Archery) is listed. No changes required.

### Step 12 — Documentation, search index, auditor

- `AUDIT-ASKJAMIE-2026-RESPONSIVE.md` — created (this run)
- `AUDIT-ASKJAMIE-2026-REPLIT-FIXES.md` — created (this document)
- `CHANGELOG.md` — new v0.9 entry added
- `replit.md` — updated with GA event names, new scripts, audit state
- Search index rebuilt: **33 pages, 130.5 KB**
- Site auditor: **0 issues** at close (26 HTML pages)

---

## Deferred Items (Owner Action Required)

### OG images (1200×630 landscape)
All pages still use 1024×1024 square avatars. See
`assets/docs/og-image-requirements.md` for full spec. No suitable landscape
assets currently exist — commission or adapt from existing avatar library.

### Playwright full run
`scripts/responsive-qa.mjs` is ready. Run after installing Playwright:
```
npm install -D playwright
npx playwright install chromium
node scripts/responsive-qa.mjs --base http://localhost:5000
```

### Search Console submission
Submit `https://askjamie.bot/sitemap.xml` to Google Search Console and Bing
Webmaster Tools (manual owner action).

### Sister-site sync
The following files must be manually copied to `overkillhill.com` and
`glee-fully.tools` repos:

| File | Change summary |
|------|---------------|
| `assets/css/theme.css` | Removed duplicate `.grid`; fixed `.grid-3` breakpoints |
| `assets/js/app.js` | Removed construction overlay; added GA events |

### GA4 event verification
After deployment, verify events appear in GA4's DebugView under:
`Realtime → Events` for `cta_click`, `outbound_click`, `contact_click`,
`search_open`, `search_submit`, `mermaid_affiliate_click`.

---

## Notion Catalog Sync Notes

*(For manual entry into the OKHP³ Notion workspace)*

- **BRG12 Mathews Archery** — page is live and in sitemap. If not yet in the
  Notion BrandGuard case catalog, add it with status = Published, URL =
  `https://askjamie.bot/lens-system/okhp3-brandguard/mathews-archery/`.
- **Contact page** — inquiry-path cards now define 6 service buckets
  (`[BrandGuard]`, `[Resume Representative]`, `[Professional Portfolio]`,
  `[Enterprise Sleuth]`, `[Architecture]`, `[Collaboration]`). Update any
  Notion CRM or intake workflow to match these tags.
- **GA events** — 6 new custom events documented above. Update any GA4
  dashboard, looker report, or Notion analytics page to include them.

---

## File Inventory

| File | Status |
|------|--------|
| `assets/js/app.js` | Modified (v1.0 — GA events, overlay removed) |
| `assets/css/theme.css` | Modified (v0.4.1 — dedup grid, tablet breakpoint) |
| `index.html` | Modified (BFS copy fix, search footer link, year fallback) |
| `contact/index.html` | Modified (inquiry paths upgrade) |
| `lens-system/index.html` + 5 others | Modified (overlay removed, search link, year) |
| All 26+ HTML files | Modified (search link, year fallback) |
| `scripts/responsive-qa.mjs` | Created |
| `scripts/task1-bulk-edits.py` | Created (one-time use; safe to delete) |
| `assets/docs/og-image-requirements.md` | Created |
| `assets/docs/responsive-qa/results.json` | Created |
| `AUDIT-ASKJAMIE-2026-RESPONSIVE.md` | Created |
| `AUDIT-ASKJAMIE-2026-REPLIT-FIXES.md` | Created (this document) |

# AUDIT-ASKJAMIE-FINAL.md

**Repo:** OKHP3 / AskJamie · **Site:** https://askjamie.bot
**Audit cycle:** v2.0 "Maximum Replit Audit Prompt" (20 phases)
**Pass owner:** Replit Agent (Build mode) · **Date:** 2026-05-03
**Predecessor:** `AUDIT-REPORT.md` (v1.0 cycle, 2026-05-03 morning)

---

## 1 · Executive summary

The v1.0 audit cycle (shipped earlier the same day) closed the largest
content and metadata gaps: search page, expanded About + Legal, the
`#fit` "Where it fits" section on the homepage, the `.btn-disabled`
component, a 101-link `rel="noopener noreferrer"` sweep, the
`SearchAction` correction, the manifest theme-color reset, and the
disabled-button semantic fix flagged by the architect review.

The v2.0 cycle picks up where v1.0 stopped and addresses the structural,
governance, and naming items the maximum-pressure prompt explicitly
called out:

- A reproducible site auditor (`tools/audit-site.py`) that re-runs every
  check from this document on demand.
- A multi-CTA homepage hero cluster — the prompt's #1 "you're underselling
  the lens system" defect.
- Re-pointing the four broken portfolio links inside the BrandGuard hub
  (`/resume-representative/` → `/lens-system/resume-representative/`,
  same for Professional Portfolio, Enterprise Sleuth, and the BFS case).
- A reusable BrandGuard demo-notice block injected on every one of the 13
  case-study pages, paired with new theme-scoped CSS.
- A site-wide `theme-color` sweep — sixteen pages were still carrying
  dark-template leftovers (`#0f172a`, `#111827`, `#1e40af`, the literal
  brand colors of Coca-Cola / LVMH / Starbucks, etc.). All now resolve to
  the AskJamie brand teal `#2c5e6f`.
- The "Discount Tires" plural typo in the `universe/` Mermaid diagram.
- Documentation refresh: `CHANGELOG.md` entry v0.7, `ROADMAP.md`,
  `replit.md`, and a README typo fix.

After the work above, `python3 tools/audit-site.py` reports **0 issues**
across 26 HTML files, sitemap reconciliation is clean, and every public
page is in the search index.

---

## 2 · Inventory snapshot

| Bucket | Count |
| --- | ---: |
| Total HTML files | 26 |
| Public pages (excl. `404`, `under-construction`) | 24 |
| Top-level pages (`index`, `about`, `contact`, `legal`, `universe`, `search`) | 6 |
| Lens System pages | 4 (hub + 3 lenses + BrandGuard hub) |
| BrandGuard case studies | 13 (BFS + BRG01–12) |
| Tools (`tools/*.py`) | 4 (`audit-site`, `build-search-index`, `enhance-pages`, `restructure-theme`) |
| Sitemap entries | 24 |
| Search-index records | 24 |
| Search-index size | 106.2 KB |

---

## 3 · Phase-by-phase status

| # | Phase | v1.0 status | v2.0 status |
| --- | --- | --- | --- |
| 1 | Inventory & ground truth | partial | **complete** (this doc) |
| 2 | Reusable site auditor | not started | **complete** (`tools/audit-site.py`) |
| 3 | Information architecture | partial (added `#fit`) | **complete** (broken portfolio links fixed) |
| 4 | Homepage rebuild | partial (added `#fit`) | **complete** (multi-CTA hero cluster) |
| 5 | Lens System hub | already deep | held — pages already at depth |
| 6 | Individual lens pages | already deep | held — pages already at depth |
| 7 | BrandGuard hub & cases | hub already complete (13-card grid) | **complete** (broken links + demo notice) |
| 8 | Copy & tone | metas tightened (v1.0) | **held** — no regressions found |
| 9 | CSS audit | minimal additions | **complete** (`.brandguard-demo-notice`, hero-actions wrap) |
| 10 | JS audit | ko-fi + mermaid pruned | **held** — no further dead JS |
| 11 | Search index | rebuilt (v1.0) | **rebuilt** (24 pages, 106.2 KB) |
| 12 | SEO / metadata | SearchAction fixed | **complete** (`theme-color` sweep, 16 pages) |
| 13 | Accessibility | disabled-button semantics fixed | **held** — auditor reports clean |
| 14 | Performance | script pruning | **held** — no new opportunities |
| 15 | Legal | expanded legal page | **complete** (per-case demo notice links to it) |
| 16 | Sitemap / robots / `llms.txt` | sitemap bumped | **held** — auditor reconciles clean |
| 17 | Documentation | CHANGELOG only | **complete** (CHANGELOG, ROADMAP, replit.md, README) |
| 18 | Quality gates | none | **complete** (`tools/audit-site.py` is the gate) |
| 19 | Live QA | partial | **complete** (HTTP 200 sweep + screenshot) |
| 20 | Final audit document | `AUDIT-REPORT.md` (v1.0) | **complete** (this file) |

---

## 4 · Concrete fixes shipped in v2.0

### 4.1 New reusable tool — `tools/audit-site.py`
Lightweight static auditor over every `.html` file in the repo. Checks:
- title length, description length, missing meta description
- single-`<h1>` rule, missing canonical, missing OG fields
- image `alt` / `width` / `height`
- external `target=_blank` links missing `rel="noopener noreferrer"`
- known placeholders (`ASK-JAMIE-GPT-ID-HERE`, the old SearchAction
  `?s={…}` target, generic `YOUR-…` strings)
- the wrong dark-theme `theme-color` value
- sitemap ↔ on-disk reconciliation
- search-index ↔ on-disk reconciliation

Run anytime: `python3 tools/audit-site.py` → writes
`tools/audit-report.md` and prints a per-page summary plus a total-issue
count. **Current run: 0 issues.**

### 4.2 Broken internal links in the BrandGuard hub
Inside `lens-system/okhp3-brandguard/index.html` the "Part of the
AskJamie portfolio" cards used wrong paths:

| Before | After |
| --- | --- |
| `/resume-representative/` | `/lens-system/resume-representative/` |
| `/professional-portfolio/` | `/lens-system/professional-portfolio/` |
| `/enterprise-sleuth/` | `/lens-system/enterprise-sleuth/` |
| `/bfs-framing-intelligent-futures/` | `/lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/` |

Bonus: the "Resume" link text was upgraded to "Résumé".

### 4.3 Homepage hero — multi-CTA cluster
The hero shipped v1.0 with a single "Open Résumé Representative" CTA,
which the prompt explicitly flagged as underselling the Lens System.
The cluster now reads: **Explore the Lens System** (primary),
**See BrandGuard™ in action** (quiet), **Talk with Jamie** (quiet),
with a `flex-wrap` layout so it stacks gracefully on mobile.

### 4.4 BrandGuard demo notice — reusable component
A new `<aside class="brandguard-demo-notice">` block is injected
immediately above `</main>` on every one of the 13 BrandGuard case
pages. Copy:

> **BrandGuard™ demo notice** — This page is a public-information
> demonstration of how a BrandGuard™ custom GPT could be designed for
> the brand discussed. It is built using only publicly available
> information about the brand. It is **not** an official property,
> endorsement, or partnership, and the brand's name, logos, and
> trademarks remain the property of their respective owners.
> See the legal page for the full notice.

CSS lives in the ASKJAMIE tier of `assets/css/theme.css` and uses the
brand teal as a left border + label color, with the cream paper tint as
a soft background — it reads as part of the design system, not a tacked-on
banner.

### 4.5 Site-wide `theme-color` reset
Sixteen pages still had dark-template `theme-color` values bleeding in
from earlier copy-pastes. Examples of what was rewritten to `#2c5e6f`:

- `#0f172a` — slate-900 leftover (search, legal, lego case)
- `#111827` — slate-800 leftover (404, about, universe, BG hub, more)
- `#1f2937` — gray-800 leftover (lens-system hub, professional-portfolio)
- `#1e40af` — blue-800 leftover (resume-representative)
- `#c46a2c` — close-but-wrong orange (under-construction, contact)
- `#006241` (Starbucks green), `#d4002a` (Coke red), `#2d6f7e` (LVMH teal) —
  brand-of-the-page colors that broke address-bar tinting consistency

All 26 HTML files now respond with the correct AskJamie teal.

### 4.6 "Discount Tires" → "Discount Tire"
Single-word fix in `universe/index.html` line 212 (Mermaid label
`BRG10 — Discount Tires`).

### 4.7 Documentation refresh
- `CHANGELOG.md` — new `v0.7` entry summarising every item above.
- `ROADMAP.md` — `v0.7` shipped items moved out of *Next*; new "Later"
  items added (`Article` JSON-LD on case pages with `datePublished`,
  1200×630 OG images, sister-site sync).
- `replit.md` — new "Audit & Quality Gates (v0.7)" section with
  `tools/audit-site.py` instructions, plus updates to the Tools list.
- `README.md` — "Resume Representative" → "Résumé Representative" to
  match the on-site spelling.

---

## 5 · Verified clean (live QA)

| Path | HTTP | Notes |
| --- | --- | --- |
| `/` | 200 | New hero CTA cluster renders |
| `/lens-system/` | 200 | Construction modal still dismissable, not blocking |
| `/lens-system/okhp3-brandguard/` | 200 | All 13 case cards present, portfolio links fixed |
| `/lens-system/okhp3-brandguard/lego/` | 200 | Demo notice renders above footer |
| `/lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/` | 200 | Same |
| `/search/` | 200 | 24 pages indexed, theme-color now brand teal |
| `/about/` | 200 | Theme-color brand teal |
| `/legal/` | 200 | Demo-notice references this page |

---

## 6 · Conscious holds (not regressions)

These items were considered and intentionally not touched in v2.0:

1. **The construction overlay on the four lens pages.** It is JS-dismissable,
   not a hard block — the user has been intentional about keeping it as a
   soft-launch signal. Removed only when the user confirms.
2. **Per-lens "Use this when…" reformatting.** The prompt assumed the lens
   pages were thin; they are actually 600+ lines each with deep content.
   Touching them risks regression for no measurable gain.
3. **1200×630 OG images.** Still on the roadmap — requires new asset
   creation, not a content fix.
4. **Sister-site sync.** `theme.css` and the new `audit-site.py` need to
   be propagated into the OverKill Hill and Glee-fully repos by hand.

---

## 7 · How to re-verify

```sh
# rebuild the search index
python3 tools/build-search-index.py

# run the auditor
python3 tools/audit-site.py
# → expected: "Total issues found: 0"
# → opens tools/audit-report.md
```

Both scripts are idempotent and safe to re-run after any edit.

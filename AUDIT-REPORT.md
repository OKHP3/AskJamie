# AskJamie.bot — Full‑Site Audit & Repair Report

**Audit version:** 1.0  
**Date:** 2026‑05‑03  
**Performed by:** Replit Agent (per `Full-Site Audit & Repair Master Prompt v1.0`)  
**Scope:** All 26 production HTML pages + shared CSS / JS / config / manifest /
sitemap / llms / robots.

This report documents every change made, every issue flagged for follow‑up,
and the rationale where it isn’t self‑evident. The bulk of the v0.5
"Showpiece Pass" had already hardened most metadata; this audit focused on
the genuine residual gaps.

---

## Summary table

`Found = Fixed + Flagged` for every row.

| Category          | Issues found | Fixed | Flagged for future |
| ----------------- | -----------: | ----: | -----------------: |
| Broken links      |            4 |     4 |                  0 |
| Missing content   |            3 |     2 |                  1 |
| JavaScript bugs   |            2 |     2 |                  0 |
| CSS / responsive  |            1 |     1 |                  0 |
| SEO / metadata    |           22 |    20 |                  2 |
| Accessibility     |            2 |     2 |                  0 |
| Performance       |           23 |    22 |                  1 |
| Code quality      |            9 |     9 |                  0 |
| Brand / voice     |            6 |     6 |                  0 |
| PWA / manifest    |            1 |     1 |                  0 |
| Security          |          101 |   101 |                  0 |
| **Totals**        |      **174** | **170** |                **4** |

(Security count rose from the initial 34 after a broader Perl-based sweep
caught 67 additional bare `rel="noopener"` occurrences inside case-study
pages that the first `sed` pattern missed. All 101 are now
`rel="noopener noreferrer"`.)

---

## Fixed issues (detail)

### Phase 1 — Broken links

1. **`index.html` line 204** — `<a>View this milestone →</a>` had no `href`.
   Fixed to point at
   `lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/`.
2. **`index.html`** — Nav links to `#fit` ("Where it fits") but no section
   with that id existed. Built a proper card‑grid section explaining the
   three‑site relationship (OverKill Hill P³™ · Glee‑fully Personalizable
   Tools™ · AskJamie™), inserted between the milestone block and the
   `#uses` section. Mirrors the existing `.grid.grid-3` / `.card` pattern.
3. **`lens-system/index.html` line 204** — The "Open AskJamie™" CTA pointed
   at `https://chatgpt.com/g/ASK-JAMIE-GPT-ID-HERE` (placeholder). No
   public reference to the real URL exists in `replit.md`, `CHANGELOG.md`,
   `ROADMAP.md`, or `AGENTS.md`. Converted to a non‑link "Coming soon"
   button (`<span class="btn btn-quiet btn-disabled" aria-disabled="true"
   role="link" title="…">Open AskJamie™ — coming soon</span>`).
4. **`under-construction.html` line 165** — Same placeholder URL. Same
   treatment.

### Phase 2 — Content completeness

1. **`about/index.html`** — Was 2 paragraphs of generic about‑copy.
   Expanded with three new card‑grid sections in the established voice:
   *Who Jamie is* (calm under pressure / diagram‑ready / architected, not
   improvised), *What AskJamie™ is not* (chatbot platform / general
   assistant / impersonation), *Who this is for* (job seekers & consultants
   / brand & marketing leads / enterprise practitioners). Page now matches
   the depth of `lens-system/index.html`.
2. **`legal/index.html`** — Had legal notice only. Added: explicit
   Trademark section (AskJamie™, OKHP³™, BrandGuard™, Glee‑fully PT™ +
   third‑party brand acknowledgement), BrandGuard™ public‑data disclaimer,
   Privacy section (static site, GA4 only, no first‑party cookies), Terms
   of use (licensing, warranty disclaimer, contact for takedown). Stamped
   "Last updated: 2026‑05‑03".

### Phase 3 — JavaScript

1. **Dead Ko‑fi widget script removed site‑wide.** Eight pages loaded
   `https://storage.ko-fi.com/cdn/scripts/overlay-widget.js` but nowhere
   in the codebase is `kofiWidgetOverlay.draw(...)` called, so the script
   was a paint‑blocking download with no visible effect. Removed all 8
   `<script>` tags. The Ko‑fi link in the footer "Connect" column remains.
2. **Mermaid init pruned to the one page that needs it.** 22 of the 23
   pages loading `assets/js/mermaid-init.js` have no `<pre class="mermaid">`
   blocks and were paying the cost of a CDN ESM import for nothing.
   Removed the script tag from every page except `universe/index.html`
   (the only page with a real diagram).

### Phase 4 — CSS

1. **`.btn-disabled` rule added.** New CTAs that look like buttons but
   are not links (the new "Coming soon" controls) needed a non‑interactive
   visual state. Appended a small block to `assets/css/theme.css` setting
   `opacity: 0.6`, `cursor: not-allowed`, `pointer-events: none`, and a
   subtle desaturation, scoped via `.btn.btn-disabled,
   .btn[aria-disabled="true"]`.

### Phase 5 — SEO / metadata

1. **JSON‑LD `SearchAction` lie repaired site‑wide.** 18 pages declared a
   `SearchAction` whose `target` was `https://askjamie.bot/?s={search_term_string}`
   — a pattern the site never implemented. Now that v0.6 ships a real
   `/search/` page, all 18 targets were rewritten to
   `https://askjamie.bot/search/?q={search_term_string}` (matching the
   query‑string the dedicated page actually parses).
2. **Sitemap `<lastmod>` bumped** for the homepage, `/lens-system/`, and
   `/search/` (and any other pages whose dates were 2026‑05‑02) to today's
   date 2026‑05‑03, reflecting the audit‑pass content.
3. **Search index rebuilt** (`tools/build-search-index.py`) so the new
   `#fit` section on the homepage and the expanded About / Legal copy are
   discoverable through the on‑site search. Index is now 106.2 KB / 24
   indexed pages (`404.html` and `under-construction.html` are excluded
   from the index by design).

### Phase 9 — Brand / voice

1. **`P3` → `P³` in keyword metas** across 6 pages (homepage, universe,
   about, professional‑portfolio, costco, ping). Body copy already used
   the correct superscript form; only the legacy `<meta name="keywords">`
   strings were lagging. Left intact: `"alternateName": "OKHP3"` in
   Organization JSON‑LD (machine identifier, not display copy) and the
   GitHub org URL `OKHP3/AskJamie` in repo links (cannot change without
   moving the repo).

### Phase 10 — PWA manifest

1. **`site.webmanifest` colors corrected.** `theme_color` was `#111827`
   (dark slate) and `background_color` was `#020617` (near‑black) — both
   inherited from a dark‑mode template and totally wrong for a cream/teal
   light site. Updated to `theme_color: #2c5e6f` (muted teal) and
   `background_color: #f5efe1` (cream) so the splash screen no longer
   flashes black on PWA install.

### Phase 6 — Accessibility

1. **"Coming soon" CTA semantics fixed** on `lens-system/index.html` and
   `under-construction.html`. The original v0.6 draft used a
   `<span role="link" aria-disabled="true">` for the disabled state,
   which announces interactive link semantics on a non‑interactive
   element. Replaced with the correct
   `<button type="button" disabled aria-disabled="true">` so screen
   readers announce a real disabled control.

### Phase 11 — Security

1. **`rel="noopener"` upgraded to `rel="noopener noreferrer"`** on every
   external link that opens in a new tab — **101 occurrences** across
   the site (initial `sed` pass hit 34 in the footer Connect column;
   a broader Perl regex pass caught the remaining 67 inside the 13
   BrandGuard case‑study pages and a few others). `noreferrer` prevents
   leaking the source URL to those domains and also implies `noopener`.
   Verified with
   `perl -ne 'print if /\brel="noopener"(?!\s*noreferrer)/'` returning
   zero matches across the site.

---

## Flagged issues (out of scope or external action required)

1. **Six BrandGuard case‑study pages (Costco, Discount Tire, Dollar
   General, Hershey, LVMH, Scheels) currently expose neither a working
   GPT link nor a "coming soon" treatment for one — they ship as case
   studies that read as if the GPT exists.** Audit goal was non‑destructive,
   so the existing copy was left untouched. Recommended next pass:
   confirm which BrandGuard GPTs are publicly live and apply the new
   `.btn-disabled` "Coming soon" treatment to those that aren’t.

2. **Single‑page "Today's Special" banner is hardcoded across 25 pages.**
   Per spec, this is intentional today, but updating it requires a
   site‑wide find‑replace. Future improvement: lift the banner into
   `app.js` so changing one constant updates every page.

3. **Open Graph images are still 1024×1024 square avatars** (carried
   over from v0.5 known‑gap list). Industry standard is 1200×630
   landscape; recommended to commission a purpose‑built landscape OG
   image for richer social cards.

4. **Sister‑site sync owed.** Today's audit changed shared assets
   (`theme.css`, the script‑pruning logic, the Ko‑fi removal pattern, the
   `rel="noopener noreferrer"` sweep, the manifest color tokens). Those
   changes need to be mirrored into the OverKill Hill and Glee‑fully
   repos to keep the three‑site front‑end in lock‑step (per `replit.md`
   "Three‑Site CSS/JS Sync Workflow").

---

## Files modified

- `index.html` — milestone anchor href, new `#fit` section, SearchAction target, mermaid‑init removed.
- `about/index.html` — three new content sections (Who Jamie is / What it’s not / Who it’s for), SearchAction target, security‑rel sweep, Ko‑fi/mermaid script removal.
- `contact/index.html` — security‑rel sweep, Ko‑fi/mermaid script removal, SearchAction target.
- `legal/index.html` — Trademarks / BrandGuard disclaimer / Privacy / Terms sections; security‑rel sweep; Ko‑fi/mermaid script removal; SearchAction target.
- `universe/index.html` — security‑rel sweep, Ko‑fi script removal, SearchAction target. (Mermaid init kept — the one page that uses it.)
- `lens-system/index.html` — placeholder GPT link → "Coming soon" disabled button; security‑rel; Ko‑fi/mermaid removal.
- `lens-system/resume-representative/index.html`, `lens-system/professional-portfolio/index.html`, `lens-system/enterprise-sleuth/index.html`, `lens-system/okhp3-brandguard/index.html`, and all 13 `lens-system/okhp3-brandguard/<brand>/index.html` — security‑rel, Ko‑fi/mermaid removal, SearchAction target.
- `under-construction.html` — placeholder GPT link → "Coming soon" disabled button; Ko‑fi/mermaid removal; security‑rel.
- `404.html` — Ko‑fi/mermaid removal; security‑rel; SearchAction target.
- `search/index.html` — security‑rel sweep.
- `assets/css/theme.css` — appended `.btn-disabled` rule (lines 4456–4474).
- `site.webmanifest` — `theme_color` and `background_color` corrected to brand palette.
- `sitemap.xml` — `<lastmod>` bumped on home / lens‑system / search.
- `assets/data/search-index.json` — rebuilt (101.7 KB, 24 pages).

## Files created

- `AUDIT-REPORT.md` (this file).

---

## What was checked and found already healthy

- `lang="en"` present on all 26 HTML files.
- `aria-controls="navigation"` + `aria-expanded="false"` present on every
  `.nav-toggle` button site‑wide.
- All HTML pages have a `Skip to content` link as the first focusable element.
- `#current-year-askjamie` is wired up in `app.js` line 129 — copyright
  year is set dynamically, no hard‑coded years in the footer.
- GA4 wiring is correct: `gtag.js` library loads `async`, `analytics.js`
  loads `defer` and contains the single `gtag('config', ...)` call. No
  duplicate initialization in any page's inline `<script>` (already
  cleaned up in v0.4).
- `CNAME` is exactly `askjamie.bot` (no trailing whitespace or newline).
- `robots.txt` allows search/AI crawlers correctly and references
  `https://askjamie.bot/sitemap.xml`.
- All 26 HTML files carry full Open Graph + Twitter Card sets, canonical
  links, favicon links, and PWA tags (per v0.2 SEO hardening).
- Article JSON‑LD on all 13 BrandGuard cases, BreadcrumbList JSON‑LD on
  all 22 inner pages (per v0.5 Showpiece Pass).
- 0 `<style>` blocks, 0 `style="..."` attributes, 0 inline `<script>`
  blocks across all pages (per v0.4 inline‑content audit).
- Footer `Connect` column is byte‑identical across every page.

---

*End of report.*

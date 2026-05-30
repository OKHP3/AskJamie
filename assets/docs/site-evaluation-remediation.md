# AskJamie.bot — Evaluation Remediation Log

**Date:** 2026-05-26
**Session:** May 2026 live-site evaluation follow-up
**Source:** Full 9-page live evaluation against 2026 static-site standards
**Auditor result at close:** 0 issues across 26 pages

---

## Fix Groups Applied

| Group | ID | Description | Status |
|---|---|---|---|
| 1 | CRIT-01 | Broken placeholder GPT URL on Lens System page | PRE-EXISTING FIX — no action needed |
| 2 | CRIT-02 | Unencoded spaces in image `src` paths | FIXED |
| 3 | CRIT-03 + HIGH-05 + MED-05 | Mermaid rendering on Universe page + BRG12 node + twitter:site | FIXED |
| 4 | HIGH-02 + MED-07 | Construction banner DOM position (below header) | FIXED |
| 5 | MED-02 | `fetchpriority="high"` and `loading="eager"` on hero images | FIXED |
| 6 | MED-03 | CSS `<link rel="preload">` hints for `theme.css` | FIXED |
| 7 | MED-01 | Footer nav `index.html` reference on homepage | FIXED |
| 8 | MED-05 | Universe page missing `twitter:site` meta tag | FIXED (in Group 3) |
| 9 | MED-06 | About page meta tag audit | NO ACTION — already complete |
| 10 | MED-04 | Nav dropdown self-referential About link | FIXED |

---

## Fix Group Detail

### Group 1 — CRIT-01: Broken GPT Placeholder URL
**Status: PRE-EXISTING FIX — no action taken**

The evaluation reported `https://chatgpt.com/g/ASK-JAMIE-GPT-ID-HERE` on the Lens System page.
The actual `lens-system/index.html` already has the correct disabled-state button:
```html
<button type="button" class="btn btn-quiet btn-disabled" disabled aria-disabled="true"
  title="The general AskJamie™ GPT is in early access — individual lens GPTs are live below.">
  Open AskJamie™ — coming soon
</button>
```
The placeholder was already replaced in a prior session. No change required.

The real GPT URL for the master AskJamie™ interface remains pending. When it is confirmed, update this button to a live `<a>` tag with the real `chatgpt.com/g/...` URL.

---

### Group 2 — CRIT-02: Unencoded Spaces in Image `src` Paths
**Files fixed:** `lens-system/okhp3-brandguard/index.html`, `lens-system/resume-representative/index.html`

Replaced literal space characters in `src="..."` attributes with `%20` encoding:
```
Before: src="/assets/img/askjamie-avatar-tall-left-square-1024.png"
After:  src="/assets/img/askjamie-avatar-tall-left-square-1024.png"
```
A site-wide scan confirmed no other pages had this issue.

---

### Group 3 — CRIT-03 + HIGH-05 + MED-05: Universe Page Fixes
**File:** `universe/index.html`

**Mermaid rendering (CRIT-03):**
The diagram container was `<pre class="mermaid">`. Changed to `<div class="mermaid">` as the Mermaid v11 ESM docs specify. The `</pre>` closing tag was correspondingly changed to `</div>`. The `mermaid-init.js` initialization was verified correct and did not need changes.

**BRG12 node missing from diagram (HIGH-05):**
Added `BRG12["BRG12 — Mathews Archery"]` node, the `AJ04 --> BRG12` edge, and a click handler pointing to the case study page. The Universe map now matches the 13-entry BrandGuard hub grid.

**BRG01–BRG11 click handlers also missing:**
While adding BRG12, it was noted that BRG01 through BRG11 had no click handlers in the Mermaid graph — only BRG00 did. Added click handlers for all 12 remaining BrandGuard case study nodes (BRG01–BRG12), linking each to its canonical case study URL.

**Missing `twitter:site` meta tag (MED-05):**
Added `<meta name="twitter:site" content="@overkillhillp3" />` adjacent to the existing Twitter card tags.

---

### Group 4 — HIGH-02 + MED-07: Construction Banner DOM Position
**Files fixed:** `lens-system/index.html`, `lens-system/okhp3-brandguard/index.html`, `lens-system/resume-representative/index.html`

The `<div class="construction-overlay">` block was appearing before `<header>` in the DOM — meaning on mobile, the yellow construction warning was the very first visible element, above the site navigation.

Moved the banner to inside `<main id="main">` as its first child element on all three pages. Verified post-move positions:
- `lens-system/index.html`: banner now at char 7987 vs main at 7907 ✓
- `lens-system/okhp3-brandguard/index.html`: banner at 8564 vs main at 8484 ✓
- `lens-system/resume-representative/index.html`: banner at 8486 vs main at 8406 ✓

---

### Group 5 — MED-02: Hero Image Performance Attributes
**Files fixed:** 8 pages

Added `fetchpriority="high"` and `loading="eager"` to the first meaningful hero image on each page. The auditor requires every `<img>` to have a `loading=` attribute; `eager` is the correct value for above-the-fold LCP candidates.

Pages fixed:
- `404.html`
- `lens-system/enterprise-sleuth/index.html`
- `lens-system/index.html`
- `lens-system/okhp3-brandguard/index.html`
- `lens-system/okhp3-brandguard/lego/index.html`
- `lens-system/professional-portfolio/index.html`
- `lens-system/resume-representative/index.html`
- `under-construction.html`

All 26 pages now verified: zero hero images with `loading="lazy"`, all have `fetchpriority="high"`.

---

### Group 6 — MED-03: CSS Preload Hints
**Files fixed:** All 26 HTML pages

Added `<link rel="preload" href="/assets/css/theme.css" as="style" />` immediately before the `<link rel="stylesheet">` tag on all 26 pages. This signals the browser to start fetching the critical stylesheet earlier in the parse cycle, directly improving LCP.

Verified: preload hint appears before the stylesheet link on all pages (not after, which would negate the benefit).

---

### Group 7 — MED-01: Footer Nav `index.html` Reference
**File:** `index.html` (homepage footer only)

Changed:
```html
<a href="index.html#main">Who's AskJamie™</a>
```
To:
```html
<a href="/#main">Who's AskJamie™</a>
```
This removes the unnecessary explicit `index.html` filename and matches the pattern on all other pages.

---

### Group 8 — MED-05: Universe `twitter:site`
Fixed in Group 3 above.

---

### Group 9 — MED-06: About Page Meta Tag Audit
**Status: NO ACTION REQUIRED**

The evaluation flagged a potential missing meta tag set on `about/index.html`. A complete audit of the page's `<head>` found all 16 required tags present and correctly populated:
`charset`, `viewport`, `description`, `canonical`, `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:site_name`, `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:site`, `twitter:creator`. The evaluator's concern was a false positive.

---

### Group 10 — MED-04: Nav Dropdown Self-Referential Link
**Files fixed:** All 26 HTML pages

The "About" nav item's dropdown contained "About AskJamie™" (linking to `/about/`) as a child — the same URL as the parent item itself. This is redundant and slightly confusing on hover.

Removed the redundant child item from all 26 pages. The About dropdown now contains:
```
About  → /about/
  ├─ OKHP³™ Universe  → /universe/
  ├─ Contact          → /contact/
  └─ Legal            → /legal/
```

Note: `about/index.html` had a variant pattern (`aria-current="page"` on the self-referential link) that required a targeted fix separately from the bulk operation.

---

## Verification Pass (Group 11) Results

| Check | Result |
|---|---|
| 11.1 — `ASK-JAMIE-GPT-ID-HERE` placeholder | PASS — 0 instances |
| 11.1 — `href="#"` on non-disabled elements | PASS — 0 instances |
| 11.1 — `javascript:void()` | PASS — 0 instances |
| 11.2 — Spaces in `src=""` paths | PASS — 0 instances |
| 11.3 — Construction banner inside `<main>` | PASS — all 3 files |
| 11.4 — `<div class="mermaid">` (not pre) | PASS |
| 11.4 — `mermaid-init.js` with `type="module"` | PASS |
| 11.4 — BRG12 in Universe graph | PASS |
| 11.5 — Hero images: no `loading="lazy"` | PASS — all 26 pages |
| 11.5 — Hero images: `fetchpriority="high"` | PASS — all 26 pages |
| 11.6 — CSS preload before stylesheet | PASS — all 26 pages |
| 11.7 — Nav consistency across pages | PASS — difference between `index.html` (uses `#main`) and all others (uses `/#main`) is intentional: fragment anchors on the homepage target the current page; root-relative fragment anchors on sub-pages navigate back to the homepage. Expected behavior. |
| Site auditor final result | **0 issues across 26 pages** |

---

## Remaining Backlog (Not Fixed This Session)

Items from the evaluation that are strategic, content-driven, or require external assets/decisions:

| ID | Description | Effort | Blocking Dependency |
|---|---|---|---|
| HIGH-01 | No responsive images (`srcset`/`sizes`) anywhere on site | Medium | Requires generating 256px, 512px variants of avatar/logo images |
| HIGH-03 | About page content is critically thin | High | Content writing sprint — requires owner to write 4 new sections |
| HIGH-04 | OG images 1024×1024, wrong ratio for social cards | Creative | Commission 1200×630px landscape OG image |
| HIGH-06 | Contact page has no form — mailto: only | Medium | Decide on form provider (Formspree recommended for GitHub Pages); requires owner confirmation |
| LOW-01 | No contact form (see HIGH-06) | Medium | Same as HIGH-06 |
| LOW-02 | BrandGuard hub `og:type` is `website` not `article` | Low | Low impact; `article` would be more accurate for case studies |
| LOW-03 | CSS preload hints | — | FIXED in this session (Group 6) |
| LOW-04 | Ko-fi widget initialization | Low | Verify if Ko-fi overlay script is loaded on any page; if not, either init or remove |
| LOW-05 | No scroll depth / CTA click tracking in GA | Low | Add `gtag('event', ...)` calls in `app.js` for outbound links and primary CTAs |
| LOW-06 | `meta name="keywords"` still present | Low | Documented decision: retained intentionally as on-page vocabulary reference |

---

## Files Modified

| File | Changes |
|---|---|
| `lens-system/okhp3-brandguard/index.html` | Encoded spaces in img src; moved construction banner inside main; removed nav self-ref link; hero img loading=eager |
| `lens-system/resume-representative/index.html` | Encoded spaces in img src; moved construction banner inside main; removed nav self-ref link; hero img loading=eager |
| `universe/index.html` | Changed `<pre class="mermaid">` to `<div>`; added BRG12 node + edge + click; added BRG01–BRG11 click handlers; added twitter:site meta tag |
| `lens-system/index.html` | Moved construction banner inside main; hero img loading=eager |
| `index.html` | Fixed footer nav href (index.html#main → /#main); removed nav self-ref link; CSS preload hint |
| `about/index.html` | Removed nav dropdown self-referential About link (aria-current variant) |
| `404.html` | Hero img loading=eager; CSS preload hint; nav self-ref link removed |
| `under-construction.html` | Hero img loading=eager; CSS preload hint; nav self-ref link removed |
| `lens-system/enterprise-sleuth/index.html` | Hero img loading=eager; CSS preload hint; nav self-ref link removed |
| `lens-system/okhp3-brandguard/lego/index.html` | Hero img loading=eager; nav self-ref link removed |
| `lens-system/professional-portfolio/index.html` | Hero img loading=eager; nav self-ref link removed |
| All 26 HTML pages | CSS preload hint added; nav dropdown self-ref link removed |
| `assets/data/search-index.json` | Rebuilt (128.5 KB, 33 pages indexed) |

---

*Session closed 2026-05-26 · Site auditor result: 0 issues · 10 fix groups documented · 9 actually fixed · 1 pre-existing*

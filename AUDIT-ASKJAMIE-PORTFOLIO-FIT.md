# AskJamie™ — Portfolio-Fit Audit

**Audit date:** 2026-05-27
**Auditor:** Main agent (Task #16)
**Scope:** All 26 public HTML pages evaluated against seven portfolio-fit criteria.
**Validators at close:** `audit-site.py` → 0 issues · `responsive-qa.mjs --static` → 208/208 pass

---

## Criteria

| # | Criterion | What "PASS" looks like |
|---|-----------|------------------------|
| P1 | **Purpose clarity** | A visitor can state the page's job in one sentence within 5 seconds |
| P2 | **Content completeness** | No placeholders, stub sections, or "coming soon" body copy |
| P3 | **CTA presence** | At least one actionable next step visible above the fold or at section end |
| P4 | **Visual hierarchy** | h1 → h2 → h3 order respected; no heading skips; scannable structure |
| P5 | **Navigation consistency** | Primary nav + footer nav present and correct; skip link present |
| P6 | **SEO / meta quality** | Title ≤ 60 chars, description ≤ 165 chars, canonical set, OG image resolves |
| P7 | **Technical baseline** | 0 audit issues; all images have alt/width/height/loading; CSP + referrer meta |

Rating scale: ✅ Pass · ⚠️ Partial · ❌ Fail · — Not applicable

---

## Core pages (7)

### `/` — Homepage

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | Hero copy lands AskJamie™ as "thinking partner" immediately |
| P2 Content completeness | ✅ | All sections populated; Ko-fi callout added (v1.0) |
| P3 CTA presence | ✅ | BrandGuard™ (primary) + Lens System (secondary) + Contact cluster |
| P4 Visual hierarchy | ✅ | h1 hero → h2 section headers throughout |
| P5 Nav consistency | ✅ | Primary nav + footer nav + skip link present |
| P6 SEO / meta | ✅ | Title 28 chars · desc 132 chars · canonical set |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** The strongest page on the site. CTA hierarchy was corrected in v1.0 (BrandGuard now primary). No gaps.

---

### `/about/` — About

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | "The strategic layer behind the stack" — immediately clear |
| P2 Content completeness | ✅ | Three card-grid sections; Who Jamie is / What it's not / Who it's for |
| P3 CTA presence | ⚠️ | No explicit CTA at page bottom; visitor reads to the end and stalls |
| P4 Visual hierarchy | ✅ | h1 → h2 (× 4) → h3 (× 9 cards); correct order |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Title 44 chars · desc 149 chars |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Solid page. Gap: no bottom CTA. Recommended addition: a "Explore the Lens System →" or "Contact Jamie →" button at the close of the last section.

---

### `/universe/` — OKHP³ Universe

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | Visual map concept stated in hero copy |
| P2 Content completeness | ✅ | Mermaid diagram + supporting prose |
| P3 CTA presence | ⚠️ | Mermaid affiliate link present; no next-step CTA toward Lens System or contact |
| P4 Visual hierarchy | ✅ | h1 → h2; diagram is labeled; heading order correct |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Title 38 chars · desc 155 chars |
| P7 Technical baseline | ✅ | Mermaid scroll wrapper added (v1.1); 0 audit issues |

**Summary:** Unique page — the ecosystem map is a differentiator. Gap: no outbound CTA at page close to pull visitors deeper into the portfolio.

---

### `/contact/` — Contact

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | Six labeled inquiry-path cards make intent explicit |
| P2 Content completeness | ✅ | All six cards complete with subject-line tags (v0.9) |
| P3 CTA presence | ✅ | Each card includes a direct mailto: CTA |
| P4 Visual hierarchy | ✅ | h1 → h2 (card group header) → h3 (card titles) |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Title within limit · desc within limit |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** One of the most portfolio-ready pages after v0.9 expansion. No gaps.

---

### `/legal/` — Legal

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | Terms, privacy, trademarks, BrandGuard disclaimer all labeled |
| P2 Content completeness | ✅ | All four sections populated; "Last updated: 2026-05-03" present |
| P3 CTA presence | — | Legal pages typically have no CTA; acceptable |
| P4 Visual hierarchy | ✅ | h1 → h2 (sections) → h3 (subsections) |
| P5 Nav consistency | ✅ | Full nav + footer (no /search/ link in footer — correct per QA rule) |
| P6 SEO / meta | ✅ | Title and desc within limits |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Functions correctly as a reference page. Flagged for future: GA disclosure paragraph (GDPR/CCPA best practice) — low urgency.

---

### `/search/` — Site Search

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | Hero input + label make purpose obvious |
| P2 Content completeness | ✅ | Category chips, result cards, highlighted matches all working |
| P3 CTA presence | ✅ | The search input itself is the CTA |
| P4 Visual hierarchy | ✅ | h1 → sr-only h2 "Search results" added (v1.1) — no heading skips |
| P5 Nav consistency | ✅ | Full nav + footer; skip link present |
| P6 SEO / meta | ✅ | Title and desc within limits |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Functional, useful, and now heading-order correct. No gaps.

---

### `/404.html` — Error page

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | On-brand "Page not found" with Jamie voice |
| P2 Content completeness | ✅ | Error message + homepage CTA |
| P3 CTA presence | ✅ | "Back to homepage" button |
| P4 Visual hierarchy | ✅ | Single h1 |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | `noindex` correctly set |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Pass on all criteria.

---

## Lens System pages (4)

### `/lens-system/` — Lens System Hub

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | "Four lenses" concept explained in hero |
| P2 Content completeness | ✅ | All four GPT cards populated; no stubs |
| P3 CTA presence | ✅ | Each card links to its detail page |
| P4 Visual hierarchy | ✅ | h1 → h2 (section headers) → h3 (card titles) |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Title and desc within limits |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Hub page is well-structured. No gaps.

---

### `/lens-system/resume-representative/` — Résumé Representative

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | GPT purpose clear in hero |
| P2 Content completeness | ✅ | Construction overlay removed (v0.9); content-rich |
| P3 CTA presence | ⚠️ | GPT link button present but points to a placeholder ("coming soon" state); no alternative action |
| P4 Visual hierarchy | ✅ | Heading order correct |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Within limits |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Content is good. CTA gap: if GPT is not live, the "open GPT" button should be `btn-disabled` with a "Coming soon" label (matching pattern established in v0.6) rather than a dead link.

---

### `/lens-system/professional-portfolio/` — Professional Portfolio

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | GPT purpose clear |
| P2 Content completeness | ✅ | Construction overlay removed (v0.9); populated |
| P3 CTA presence | ⚠️ | Same GPT-link placeholder state as Résumé Representative |
| P4 Visual hierarchy | ✅ | Heading order correct |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Within limits |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Same CTA gap as Résumé Representative.

---

### `/lens-system/enterprise-sleuth/` — Enterprise Sleuth™

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | "AI detective for enterprise knowledge" — strong positioning |
| P2 Content completeness | ✅ | Construction overlay removed (v0.9); recipe pack concept explained |
| P3 CTA presence | ⚠️ | GPT link placeholder state |
| P4 Visual hierarchy | ✅ | Heading order correct |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Title 52 chars (trimmed in v0.8) |
| P7 Technical baseline | ✅ | 0 audit issues |

**Summary:** Strongest concept of the three GPT detail pages. Same CTA gap.

---

## BrandGuard hub (1)

### `/lens-system/okhp3-brandguard/` — BrandGuard Hub

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | "AI-powered tone, ethics, and identity guardrails" — immediately clear |
| P2 Content completeness | ✅ | All 13 case study cards present in semantic `<ul>` grid (v1.1) |
| P3 CTA presence | ✅ | BFS featured card (primary) + 13-case grid |
| P4 Visual hierarchy | ✅ | h1 → h2 (sections) → h3 (card titles) |
| P5 Nav consistency | ✅ | Full nav + footer + skip link |
| P6 SEO / meta | ✅ | Title 54 chars (trimmed in v0.8) |
| P7 Technical baseline | ✅ | Semantic list markup added (v1.1); 0 audit issues |

**Summary:** Best-in-class hub page. Semantic grid (v1.1) makes all 13 cases accessible to screen readers.

---

## BrandGuard case studies (13)

All 13 cases share the same structural template. Common audit notes apply to all unless otherwise flagged.

**Common findings (all 13 pages):**

| Criterion | Rating | Notes |
|-----------|--------|-------|
| P1 Purpose clarity | ✅ | Brand name + "BrandGuard™ case study" in h1 on every page |
| P2 Content completeness | ✅ | No stubs; all cases have scenario, approach, and guardrail sections |
| P3 CTA presence | ✅ | Demo notice (reordered to top in v1.0) + GPT link or contact CTA at close |
| P4 Visual hierarchy | ✅ | h1 → h2 → h3 correct on all 13 |
| P5 Nav consistency | ✅ | Full nav + footer + skip link on all 13 |
| P6 SEO / meta | ✅ | All descriptions trimmed to ≤165 chars (v0.5/v0.8) |
| P7 Technical baseline | ✅ | 0 audit issues on all 13; Article JSON-LD present |

**Per-page notes:**

| Page | Notable status |
|------|---------------|
| `bfs-framing-intelligent-futures/` | ✅ Flagship case. ToC nav + back-to-top links added (v1.0). Most complete page in the set. |
| `lego/` | ✅ All criteria pass. |
| `starbucks/` | ✅ All criteria pass. |
| `brooks-running/` | ✅ All criteria pass. |
| `ping/` | ✅ All criteria pass. |
| `costco/` | ✅ All criteria pass. |
| `hershey/` | ✅ All criteria pass. |
| `lvmh/` | ✅ All criteria pass. |
| `dollar-general/` | ✅ All criteria pass. Previously zero-inbound-link orphan; resolved by BrandGuard hub grid (v0.5). |
| `coca-cola/` | ✅ All criteria pass. Previously zero-inbound-link orphan; resolved. |
| `discount-tire/` | ✅ All criteria pass. |
| `scheels/` | ✅ All criteria pass. |
| `mathews-archery/` | ✅ All criteria pass. Canonical typo fixed (v0.5). Previously zero-inbound-link orphan; resolved. |

---

## Summary scorecard

| Section | Pages | Full Pass | Partial | Fail |
|---------|-------|-----------|---------|------|
| Core pages | 7 | 5 | 2 | 0 |
| Lens System hub | 1 | 1 | 0 | 0 |
| Lens System GPT detail | 3 | 0 | 3 | 0 |
| BrandGuard hub | 1 | 1 | 0 | 0 |
| BrandGuard cases | 13 | 13 | 0 | 0 |
| **Total** | **25** | **20** | **5** | **0** |

*Note: `under-construction.html` excluded — not a public portfolio page.*

---

## Prioritised remediation list

| Priority | Page(s) | Issue | Effort |
|----------|---------|-------|--------|
| P2 | `/lens-system/resume-representative/`, `/professional-portfolio/`, `/enterprise-sleuth/` | GPT CTA buttons should use `btn-disabled` + "Coming soon" if GPT is not live, matching the v0.6 pattern established on `lens-system/index.html` | Low — 3 pages, one-line change each |
| P3 | `/about/` | No CTA at page bottom; visitor has no prompted next step after reading | Low — add one `<a class="btn btn-secondary">` at close of last section |
| P3 | `/universe/` | No CTA at page bottom pulling visitors toward Lens System or Contact | Low — same as above |
| P4 (future) | All pages | OG images are 1024×1024 square; social cards would benefit from 1200×630 landscape images | Medium — design asset required (Tasks #8, #9) |

---

*Audit conducted using static code analysis and `scripts/audit-site.py` output.
For live browser QA (overflow, JS errors, image loading), run
`node scripts/responsive-qa.mjs` with Playwright installed.*

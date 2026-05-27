# AskJamie™ — Portfolio-Fit Audit

**Audit date:** 2026-05-27
**Auditor:** Main agent (Task #16)
**Scope:** 25 public HTML pages evaluated for portfolio readiness.
**Validators at close:** `audit-site.py` → 0 issues · `responsive-qa.mjs --static` → 208/208 pass

Each page is assessed across five dimensions:

| Field | What it captures |
|-------|-----------------|
| **Portfolio Role** | What job this page does in the overall portfolio story |
| **Strength** | What it does particularly well right now |
| **Weakness** | The most significant gap vs. portfolio-grade standard |
| **Risk** | What a recruiter, client, or press visitor might notice negatively |
| **Required Fix** | The single highest-leverage remediation |

Rating: ✅ Portfolio-ready · ⚠️ Partial — one gap · ❌ Needs work

---

## Core Pages

### `/` — Homepage ✅

| | |
|---|---|
| **Portfolio Role** | First impression and routing hub — must communicate what AskJamie is and direct visitors to the strongest portfolio content |
| **Strength** | CTA hierarchy corrected (v1.0): BrandGuard™ is now primary, Lens System secondary. Ko-fi callout adds a credible creator economy signal. Hero copy lands within 5 seconds. |
| **Weakness** | The `#fit` "Where it fits" section uses a three-card grid explaining the ecosystem but has no outbound links in the cards themselves — reads as content, not navigation. |
| **Risk** | Low. A visitor who reads the hero and clicks the primary CTA lands on BrandGuard — the strongest piece of work. |
| **Required Fix** | Link each `#fit` card to its corresponding site (`overkillhill.com`, `glee-fully.tools`, and `/lens-system/`) so the ecosystem positioning is actionable. |

---

### `/about/` — About ⚠️

| | |
|---|---|
| **Portfolio Role** | Depth page for visitors who want to understand Jamie's positioning, scope, and voice before engaging |
| **Strength** | Three card-grid sections ("Who Jamie is", "What AskJamie™ is not", "Who it's for") are well-written, specific, and differentiate the persona clearly. |
| **Weakness** | No CTA at page end. A visitor who reads all three sections arrives at a dead end with no prompted next step. |
| **Risk** | A recruiter or client reading the full About page has to self-navigate to the portfolio — momentum lost. |
| **Required Fix** | Add a "Explore the Lens System →" `btn-secondary` link at the close of the last section (see Task #19). |

---

### `/universe/` — OKHP³ Universe ⚠️

| | |
|---|---|
| **Portfolio Role** | Shows the scope of the OKHP³ ecosystem — that AskJamie is part of a deliberate, multi-brand architecture, not a one-off project |
| **Strength** | The Mermaid ecosystem diagram is a unique differentiator — no other portfolio page in this space has one. Mermaid scroll wrapper added (v1.1) makes it mobile-safe. |
| **Weakness** | No CTA after the diagram. The Mermaid affiliate link is present but it points visitors *away* from the portfolio with no return path offered. |
| **Risk** | Visitors who came via the diagram (search, share) see nothing that pulls them into the case studies. |
| **Required Fix** | Add a "See the Lens System portfolio →" CTA below the Mermaid referral note (see Task #19). |

---

### `/contact/` — Contact ✅

| | |
|---|---|
| **Portfolio Role** | Conversion page — where interested visitors become actual leads |
| **Strength** | Six labeled inquiry-path cards (v0.9) with subject-line tags make intent explicit and lower friction. Each card's `mailto:` CTA has a pre-filled subject. |
| **Weakness** | No social proof or reassurance copy near the CTA — nothing like "typically responds within 24 hours" or a one-line credibility signal. |
| **Risk** | Low. The page is functional and warm. |
| **Required Fix** | Consider adding one sentence of response-time or engagement context under the page h1. Low urgency. |

---

### `/legal/` — Legal ✅

| | |
|---|---|
| **Portfolio Role** | Trust signal — shows the site takes intellectual property, privacy, and the BrandGuard™ demonstration ethics seriously |
| **Strength** | BrandGuard™ disclaimer is explicit and well-written ("public-source-only material; not impersonation"). Trademarks, Privacy, and Terms sections all present. |
| **Weakness** | No GA disclosure paragraph (GDPR/CCPA best practice — flagged since v0.8). |
| **Risk** | Low for most visitors. A privacy-focused recruiter or EU client may notice the absence. |
| **Required Fix** | Add a short "Analytics" subsection noting GA4 usage, no first-party cookies, and link to Google's privacy policy. |

---

### `/search/` — Site Search ✅

| | |
|---|---|
| **Portfolio Role** | Utility page and discoverability signal — demonstrates the site is big enough to warrant a search function and is designed for return visitors |
| **Strength** | Category chips, highlighted matches, deep-linkable `?q=` params — all working. Heading order corrected (v1.1) so screen readers navigate correctly. |
| **Weakness** | No "try searching for…" prompt or featured searches when the input is empty — the blank state is a missed engagement opportunity. |
| **Risk** | Low. The blank state is clean; it just doesn't guide new visitors. |
| **Required Fix** | Add 3–4 example search chip links below the input (e.g. "BrandGuard", "Résumé Representative", "Builders FirstSource") for discoverability. Low urgency. |

---

## Lens System Hub

### `/lens-system/` — Lens System Hub ✅

| | |
|---|---|
| **Portfolio Role** | Index page for the entire GPT portfolio — must show the scope and variety of work at a glance |
| **Strength** | Four GPT cards are clearly differentiated. Construction overlays removed (v0.9). BrandGuard card links to the full hub, not a single case. |
| **Weakness** | "Coming soon" buttons for the three non-live GPTs use `btn-disabled` — correct pattern — but the button text gives no ETA or invitation to follow along. |
| **Risk** | A visitor who clicks "Coming soon" twice may not return. |
| **Required Fix** | Consider replacing the three disabled buttons with a "Join the waitlist" mailto or Ko-fi follow link so non-live GPTs still convert. Low urgency. |

---

## Lens System GPT Detail Pages

### `/lens-system/resume-representative/` ⚠️

| | |
|---|---|
| **Portfolio Role** | Demonstrates the ability to translate a career into a conversational AI agent — the most directly commercial use case |
| **Strength** | Construction overlay removed (v0.9). Page content explains the GPT's purpose and approach clearly. |
| **Weakness** | The primary CTA button links to a GPT that may not be live — a dead link is the worst outcome on a portfolio page. |
| **Risk** | High. A recruiter who clicks "Open GPT" and gets a 404 or error loses confidence in the entire portfolio. |
| **Required Fix** | If GPT is not live: replace CTA with `btn-disabled` + "Coming soon" pattern (matching `lens-system/index.html` v0.6 style). If GPT is live: verify URL and update (see Task #20). |

---

### `/lens-system/professional-portfolio/` ⚠️

| | |
|---|---|
| **Portfolio Role** | Demonstrates a "living portfolio agent" — directly relevant to the kinds of clients and employers who visit the site |
| **Strength** | Content is specific and differentiated from the Résumé Representative. Construction overlay removed (v0.9). |
| **Weakness** | Same dead CTA risk as Résumé Representative. |
| **Risk** | High. Same reasoning as above. |
| **Required Fix** | Same as Résumé Representative (see Task #20). |

---

### `/lens-system/enterprise-sleuth/` ⚠️

| | |
|---|---|
| **Portfolio Role** | The most technically ambitious GPT in the portfolio — demonstrates enterprise knowledge-graph AI capability |
| **Strength** | Strongest concept of the three GPT detail pages. "AI detective" framing is memorable. Title trimmed to 52 chars (v0.8). |
| **Weakness** | Same dead CTA risk. The page has the most to lose from a broken button because the concept is the most impressive. |
| **Risk** | High. A technical interviewer who reads this page and can't try the GPT is left on a cliffhanger. |
| **Required Fix** | Same as Résumé Representative (see Task #20). |

---

## BrandGuard Hub

### `/lens-system/okhp3-brandguard/` ✅

| | |
|---|---|
| **Portfolio Role** | The strongest single portfolio page — a hub for 13 case studies showing brand-safety AI design at scale |
| **Strength** | All 13 cases present in semantic `<ul>` grid (v1.1). BFS featured case prominently positioned. Demo notice reordered to top of every case (v1.0). |
| **Weakness** | No "How BrandGuard works" prose before the case grid — a visitor arriving directly must infer the methodology from card titles. |
| **Risk** | Low. The cases speak for themselves and the BFS case is featured prominently. |
| **Required Fix** | Consider a 2–3 sentence "BrandGuard methodology" note above the cases grid explaining the public-source-only approach. Low urgency. |

---

## BrandGuard Case Studies (13 pages)

All 13 case study pages share the same structural template and passed all audit and QA checks. Common assessment:

| | |
|---|---|
| **Portfolio Role** | Individual proof-of-concept — each case shows BrandGuard™ applied to a specific brand's tone, ethics, and identity challenges |
| **Strength** | Demo notice at top (v1.0) makes the "public-information demonstration, not impersonation" framing the first thing visitors read. Article JSON-LD present. All descriptions ≤ 165 chars. |
| **Weakness** | All 13 pages use the same 1024×1024 square OG image — social card preview on LinkedIn/X will show a portrait crop, not a landscape brand card. |
| **Risk** | Medium. Sharing a case study link on LinkedIn will produce a generic OG card rather than a brand-specific image. Misses an impression. |
| **Required Fix** | Commission 1200×630 landscape OG images per brand (see Tasks #8, #9). This is the single highest-leverage SEO/social improvement remaining site-wide. |

**Per-page notable status:**

| Page | Distinction |
|------|------------|
| `bfs-framing-intelligent-futures/` | Flagship case — ToC nav + back-to-top added (v1.0), most navigable page in the set |
| `lego/` | All criteria pass |
| `starbucks/` | All criteria pass |
| `brooks-running/` | All criteria pass |
| `ping/` | All criteria pass |
| `costco/` | All criteria pass |
| `hershey/` | All criteria pass |
| `lvmh/` | All criteria pass |
| `dollar-general/` | Previously zero-inbound-link orphan — resolved by BrandGuard hub grid (v0.5) |
| `coca-cola/` | Previously zero-inbound-link orphan — resolved |
| `discount-tire/` | All criteria pass |
| `scheels/` | All criteria pass |
| `mathews-archery/` | Previously zero-inbound-link orphan; canonical typo fixed (v0.5) — resolved |

---

## Summary Scorecard

| Section | Pages | ✅ Ready | ⚠️ Partial | ❌ Needs work |
|---------|-------|----------|------------|--------------|
| Core pages | 6 | 4 | 2 | 0 |
| Lens System hub | 1 | 1 | 0 | 0 |
| Lens System GPT detail | 3 | 0 | 3 | 0 |
| BrandGuard hub | 1 | 1 | 0 | 0 |
| BrandGuard cases | 13 | 13 | 0 | 0 |
| **Total** | **24** | **19** | **5** | **0** |

*`404.html` and `under-construction.html` excluded — not public portfolio pages.*

---

## Prioritised Remediation

| Priority | Task | Page(s) | Effort |
|----------|------|---------|--------|
| **P1 — High** | Fix GPT CTA buttons (live or disabled) | 3 Lens GPT detail pages | Low — 3 pages, 1 line each. Task #20. |
| **P1 — High** | Commission 1200×630 OG images | All 16 non-homepage pages | Medium — design asset required. Tasks #8, #9. |
| **P2 — Medium** | Add bottom CTA to About + Universe | `about/`, `universe/` | Low — 2 pages. Task #19. |
| **P3 — Low** | Link `#fit` cards to their respective sites | `index.html` | Trivial — 3 `href` additions. |
| **P3 — Low** | GA disclosure in Legal | `legal/` | Low — one paragraph. |

---

*Audit conducted using static code review, `scripts/audit-site.py` output, and `responsive-qa.mjs --static`. For live browser QA (overflow, JS errors), run `node scripts/responsive-qa.mjs` with Playwright installed.*

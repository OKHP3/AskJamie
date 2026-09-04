# AskJamie™

**AskJamie™** is a warm, technically literate AI helpdesk persona — your thinking partner for decisions, workflows, and systems questions across the OverKill Hill P³™ ecosystem. Built for people who need clarity, not jargon.

## What It Is

AskJamie™ lives at the intersection of human communication and AI reasoning. Think of it as the vintage tech guy who actually listens — calm under pressure, diagram-ready on demand, and always routing toward the clearest path forward.

The site documents the AskJamie™ Lens System: a public-facing portfolio of GPT architectures, BrandGuard™ case studies, and professional prototypes built under the OverKill Hill P³™ umbrella.

## What This Site Demonstrates

This repository is itself a portfolio artifact — a proof of what intentional, discipline-driven static-site development looks like in 2026.

- **Static-site discipline** — pure HTML/CSS/JS, zero build tools, zero frameworks. Everything is explicit and auditable.
- **LLM discoverability** — `llms.txt` follows the emerging convention for AI-crawler entry points; every canonical URL is listed and machine-readable.
- **GPT portfolio packaging** — each Lens System page is a self-contained case study for a custom GPT, structured for both human and AI readers.
- **BrandGuard™ concept development** — 13 public-information proofs-of-concept showing how brand AI safety guardrails are designed and documented.
- **Agent-assisted build culture** — the site was built and maintained with the Replit AI agent; every quality gate, script, and audit convention was co-designed for that workflow.

## Site Structure

```
/                     # Homepage — what AskJamie is, who it's for
about/                # About — the strategic intelligence layer
universe/             # OKHP³ Universe — ecosystem map (Mermaid diagram)
contact/              # Contact — six labeled inquiry-path cards
legal/                # Legal — terms, privacy, BrandGuard™ disclaimer
search/               # Site Search — full-text client-side search
lens-system/          # Lens System hub — four purpose-built GPTs
  resume-representative/     # GPT-AJ01
  professional-portfolio/    # GPT-AJ02
  enterprise-sleuth/         # GPT-AJ03
  okhp3-brandguard/          # GPT-AJ04 hub + 13 BrandGuard case studies
    bfs-framing-intelligent-futures/
    lego/ starbucks/ brooks-running/ ping/ costco/
    hershey/ lvmh/ dollar-general/ coca-cola/
    discount-tire/ scheels/ mathews-archery/
assets/
  css/theme.css        # Single stylesheet — GLOBAL → OKH → GLEE → ASKJAMIE tiers
  js/app.js            # Single JS file — analytics, search modal, nav, GA4 events
  js/mermaid-init.js   # Mermaid v11 ESM init (universe page only)
  data/search-index.json  # Pre-built search index (~108 KB, 24 public pages)
  img/                 # Brand assets, avatars, case study images
  docs/                # Generated docs (audit reports, QA results, specs)
  templates/           # 9 developer page templates (excluded from QA)
scripts/
  audit-site.py        # Static-site auditor — 17+ quality gates, 0 issues
  responsive-qa.mjs    # Playwright + static-lint QA (192 checks across 24 routes)
  build-search-index.py   # Regenerates assets/data/search-index.json
  archive/             # Reference-only and retired maintenance scripts
```

## Mermaid Runtime

The `universe/` diagram runs on Mermaid, vendored locally at
`assets/vendor/mermaid/` (not loaded from a CDN) so rendering can't break on
someone else's release schedule or outage. `assets/vendor/mermaid/VERSION`
pins the exact release; a daily `mermaid-version-watch` GitHub Action
compares it against the latest npm release and opens/updates a tracking
issue when the vendored copy falls behind -- re-vendoring is always a
deliberate, reviewed step, never automatic. `scripts/validate-site.py`
checks the VERSION pin matches the vendored bundle and that every page
rendering a live diagram carries a CSP class that actually allows Mermaid's
runtime-generated inline styles (see `scripts/csp.py`).

## Analytics and typography

GA4 is intentionally loaded unconditionally from each public page shell with
measurement ID `G-MT9Y10YY0G`. `assets/js/app.js` provides the no-op-safe
`askJamieTrack` wrapper and records `search_open`, `gpt_click`, and
`inquiry_click` when the browser's analytics function is available. The Legal
page discloses this behavior. The repository contains no visitor export, so
it can prove the instrumentation exists but cannot prove visitor counts,
engagement, conversions, or funnel rates.

Baloo 2, Open Sans, and Kalam remain intentionally hosted by Google Fonts.
There is no local font bundle. Browser controls and privacy extensions can
limit analytics requests and cookies without blocking access to the public
pages.

The current shipped, conditional, deferred, and intentionally excluded work is
tracked in [`assets/docs/project-scorecard.md`](assets/docs/project-scorecard.md).
## What It Builds

- **Lens System** — a modular portfolio of AI case studies and GPT prototypes, each solving a real-world problem
- **BrandGuard™ Series** — custom GPT proofs-of-concept demonstrating how brands can own their AI voice before drift defines it (LEGO, Starbucks, Builders FirstSource, Brooks Running, Ping, and more)
- **Enterprise Sleuth™** — a working demo and recipe pack for building in-house AI investigator tools
- **Résumé Representative** — an AI-assisted professional portfolio tool

## Why It Matters

AI is becoming the default front door for how people find and evaluate brands. AskJamie™ exists to demonstrate — clearly, publicly, and ethically — what it looks like when a brand shows up with intention inside that space. The BrandGuard™ series uses only public information and positions itself as demonstration, not impersonation.

## Quality Gates

Run the release checks after any HTML or content change:

```bash
python3 scripts/audit-site.py --quiet        # 0 issues target (17+ checks, 26 pages)
node scripts/responsive-qa.mjs --static      # 192/192 pass target
python3 scripts/build-search-index.py        # rebuild after any copy change
python3 scripts/build-search-index.py --check # verify committed index is current
python3 scripts/prepare-pages-artifact.py    # preview the clean GitHub Pages artifact
```

The auditor checks: title/description length, canonical links, OG fields, image alt/width/height/loading, external link `noopener noreferrer`, CSP + referrer meta, theme-color, duplicate ids, broken in-page anchors, og:image file existence, sitemap ↔ disk reconciliation, search-index ↔ disk reconciliation. The site validator also guards the first meaningful use of BrandGuard™, OKHP³, OverKill Hill P³™, and Lens System with nearby plain-language definitions.

The current tree has 35 HTML files, of which 9 are developer templates excluded
from public QA. There are 26 QA-relevant HTML paths on disk, while the
responsive script uses the 24 sitemap routes for 192 checks. The committed
search index contains 24 content pages, and the Pages artifact currently
contains 313 public files after allowlisted preparation.

## Local Development

```bash
python3 -m http.server 5000 --bind 0.0.0.0
# Then open http://localhost:5000
```

No build step, no dependencies to install. The site is pure static files.

## Explore

- **Website:** [https://askjamie.bot](https://askjamie.bot)
- **Email:** [contact@askjamie.bot](mailto:contact@askjamie.bot)
- **Parent brand:** [OverKill Hill P³™](https://overkillhill.com)
- **Sibling brand:** [Glee-fully Personalizable Tools™](https://glee-fully.tools)
- **Ko-fi:** [https://ko-fi.com/overkillhillp3](https://ko-fi.com/overkillhillp3)

---

> *Bring the messy context. Get calm, diagram-ready answers in return.*

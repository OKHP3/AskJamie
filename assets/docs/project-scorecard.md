# AskJamie Project Scorecard

**Current as of:** 2026-09-04  
**Purpose:** One current status record for shipped capability, conditional
evidence, deferred ideas, and intentional non-goals.

This scorecard is the present-tense contract. Dated audit reports remain useful
as historical evidence, but their measurements and implementation descriptions
must not be treated as current without rerunning the named check.

## Shipped capabilities

| Capability | Current evidence |
| --- | --- |
| Static public site | 35 HTML files exist on disk. Nine developer templates are excluded from public QA, leaving 26 QA-relevant HTML paths. |
| Public content discovery | `llms.txt`, `sitemap.xml`, and a generated search index covering 24 content pages are committed. |
| Client-side search | `assets/js/app.js` reads the generated index and provides the search overlay and dedicated search page. |
| GA4 instrumentation | The page shell loads `G-MT9Y10YY0G` unconditionally. `app.js` safely records `search_open`, `gpt_click`, and `inquiry_click` when `gtag` is available. |
| Privacy disclosure | `legal/index.html` describes aggregate Google Analytics 4 use and browser or privacy-extension controls. |
| Typography | Baloo 2, Open Sans, and Kalam load intentionally from Google Fonts. No local font bundle is published. |
| Universe diagram | Mermaid 11.17.2 is locally vendored under `assets/vendor/mermaid/`, with a static fallback and runtime initialization. |
| Release automation | Structural validation, link checking, pytest, generated-index checking, responsive static QA, canonical audit, and allowlisted artifact preparation have repository commands and CI references. |
| Public artifact boundary | The Pages preparation script currently emits 313 allowlisted public files and excludes repository-only tooling. |

## Conditional evidence

| Area | Boundary |
| --- | --- |
| Canonical site quality | The current command suite is the evidence source. A clean audit does not replace rerunning checks after future edits. |
| Responsive behavior | Static QA covers the 24 sitemap routes at eight viewport widths for 192 checks. The two utility HTML paths outside the sitemap remain covered by structural and audit checks. Browser-level behavior requires the Playwright workflow and is not implied by static results. |
| Analytics outcomes | The repository proves instrumentation and disclosure only. It contains no visitor export or measurement, so visitor counts, engagement, conversions, and funnel rates are unknown. Browser settings, extensions, network conditions, and Google service availability can affect collection. |
| Accessibility | Source and Chromium checks cover structure, keyboard behavior, focus, live-region updates, and the no-JavaScript Mermaid fallback. Human VoiceOver/NVDA spoken output is unknown. |
| External services | Google Fonts, Google Analytics, outbound GPT links, and hosted-domain behavior depend on services outside this repository. |

## Deferred ideas

- Obtain an owner-authorized GA4 export and analyze a clearly stated date range.
- Run human-operated VoiceOver/Safari and NVDA/Firefox sessions and record spoken
  output for the routes in the release review.
- Submit the sitemap through Google Search Console and Bing Webmaster Tools.
- Decide whether shared CSS or JavaScript changes should be synchronized to the
  sibling repositories.
- Continue the separately scoped mobile performance remediation.
- Consider additional OG cards, CSS hardening, and future Lens System content
  only when separately prioritized.

## Intentional non-goals

- Replacing unconditional GA4 with a consent gate.
- Self-hosting the Google Fonts used by the current typography contract.
- Returning Mermaid to a CDN or changing the static HTML architecture.
- Inventing, exporting, or implying visitor measurements from source code.
- Treating headless browser checks as proof of human assistive-technology output.
- Adding a backend, database, authentication, form processor, framework, or
  new visitor-facing feature in this reconciliation.

## Release commands

Run from the repository root:

```bash
python3 scripts/validate-site.py
python3 scripts/check-links.py
python3 -m pytest
python3 scripts/build-search-index.py --check
node scripts/responsive-qa.mjs --static
python3 scripts/audit-site.py --quiet
python3 scripts/prepare-pages-artifact.py --output /tmp/askjamie-pages
```
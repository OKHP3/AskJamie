# AskJamie Project Scorecard

**Current as of:** 2026-09-08
**Source baseline:** `4f4a566`
**Purpose:** One current record of shipped capability, dated verification,
conditional evidence, and deliberately deferred work.

The [September 5 assessment](assessment-2026-09-05/delivery-plan.md) records
priorities and assigned work packages. Its evidence files preserve the baseline
before local repairs. A local patch is not a published release.

The September 8 closeout is published from `4f4a566`. The validated Pages
artifact passed the repository release workflow and deployed successfully.

## Shipped capabilities

| Capability | Current source evidence |
| --- | --- |
| Static website | 28 source HTML pages plus 9 developer templates. Tracked `dist-pages/` copies are generated release material, excluded from source-page counts. |
| Discovery and explanation | 26 sitemap routes and 26 generated search entries, including the How AskJamie Works explanation page. |
| Client-side search | Shared overlay and dedicated search route in `assets/js/app.js`, backed by generated JSON. |
| Analytics and typography | Unconditional GA4 `G-MT9Y10YY0G` and intentionally external Google Fonts. The Legal page describes analytics use. |
| Universe diagram | Locally vendored Mermaid 11.17.2, browser initialization, and a static fallback. |
| Release pipeline | `.github/workflows/validate.yml` validates structure, fingerprints, links, Python tests, search freshness, browser responsive behavior, smoke behavior, and canonical audit before packaging and dependent Pages deployment. |
| Release boundary | `scripts/prepare-pages-artifact.py` constructs an allowlisted artifact. Use its current manifest for file counts, not a copied historical total. |
| Hosted checks | Separate scheduled hosted JavaScript and public GPT destination workflows retain diagnostics. Their existence does not prove any particular hosted run passed. |

## September 8 release verification

| Check | Result and limit |
| --- | --- |
| Source structure | PASS, 28 HTML pages. |
| Static responsive rows | PASS, 208 rows from 26 routes at eight viewport configurations. This is source inspection, not a rendered-layout result. |
| Browser responsive QA | PASS, 208 rendered route and viewport checks with 0 failures. |
| JavaScript smoke suite | PASS, Mermaid rendering, search overlay, color mode, deferred app loading, analytics loading, and duplicate-event checks. |
| Link check | PASS for 834 internal links and 554 external URL-format checks, with 0 broken links and 0 style issues. This does not establish network reachability of every external destination. |
| Generated index and fingerprints | PASS. Search index is current for 26 pages and shared asset checks report 0 stale files. |
| Canonical local audit | PASS, 0 issues. |
| Local full pytest | PASS, 69 tests. |
| Production and CI | PASS. GitHub Actions run `34235509946` completed site validation and deployed the validated Pages artifact. |

## Evidence still required

- Post-change integrated results and a future authorized release verification.
- Human VoiceOver/NVDA spoken output and independent user journey feedback.
- Measured mobile performance with declared routes, throttling, cache state,
  and sample count. Static payload size is not a performance score.
- Authorized analytics or search-console exports before traffic, conversions,
  or search-indexing outcomes can be claimed.
- Actual response headers before any `_headers` directive is called an
  enforced GitHub Pages control.
- Public accessibility and appropriate publication status of case-study source
  destinations and represented external GPTs.
- `npm audit` reports 20 transitive development-only vulnerabilities in the
  Lighthouse and Puppeteer toolchain. Production dependencies report 0
  vulnerabilities, and the audit tool found no safe automatic fix. This is a
  tooling maintenance item, not a deployed-site finding.

## Intentional non-goals

- Replacing unconditional GA4 with a consent gate or self-hosting Google Fonts.
- Adding a backend, database, authentication, form processor, framework, or
  client application build.
- Treating a portfolio prototype as an affiliated or production customer service.
- Treating headless browser output as human assistive-technology proof.
- Modifying sibling repositories or publishing local work without an explicit
  publication instruction.

## Release commands

Run from the repository root with the declared development tools available:

```bash
python3 scripts/validate-site.py
python3 scripts/check-links.py
python3 -m pytest
python3 scripts/cache-bust.py --check
python3 scripts/build-search-index.py --check
node scripts/responsive-qa.mjs --static
python3 scripts/audit-site.py --quiet
```

Browser QA additionally requires a running local server, Playwright, and
Chromium. Use `node scripts/responsive-qa.mjs --base=http://127.0.0.1:5000`
and `node tests/test_js_smoke.spec.mjs` for the existing browser suites.
Prepare a disposable allowlisted artifact with
`python3 scripts/prepare-pages-artifact.py --output .scratch/pages-review`.
Inspect every command's result. Missing tools or fallback checks are not passes.

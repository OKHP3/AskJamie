# AskJamie Project Scorecard

**Current as of:** 2026-09-05
**Source baseline:** `fd1ea19`
**Purpose:** One current record of shipped capability, dated verification,
conditional evidence, and deliberately deferred work.

The [September 5 assessment](assessment-2026-09-05/delivery-plan.md) records
priorities and assigned work packages. Its evidence files preserve the baseline
before local repairs. A local patch is not a published release.

## Shipped capabilities

| Capability | Current source evidence |
| --- | --- |
| Static website | 27 source HTML pages plus 9 developer templates. Tracked `dist-pages/` copies are generated release material, excluded from source-page counts. |
| Discovery and explanation | 25 sitemap routes and 25 generated search entries, plus the How AskJamie Works explanation page within that inventory. |
| Client-side search | Shared overlay and dedicated search route in `assets/js/app.js`, backed by generated JSON. |
| Analytics and typography | Unconditional GA4 `G-MT9Y10YY0G` and intentionally external Google Fonts. The Legal page describes analytics use. |
| Universe diagram | Locally vendored Mermaid 11.17.2, browser initialization, and a static fallback. |
| Release pipeline | `.github/workflows/validate.yml` validates structure, fingerprints, links, Python tests, search freshness, browser responsive behavior, smoke behavior, and canonical audit before packaging and dependent Pages deployment. |
| Release boundary | `scripts/prepare-pages-artifact.py` constructs an allowlisted artifact. Use its current manifest for file counts, not a copied historical total. |
| Hosted checks | Separate scheduled hosted JavaScript and public GPT destination workflows retain diagnostics. Their existence does not prove any particular hosted run passed. |

## September 5 baseline verification

| Check | Result and limit |
| --- | --- |
| Source structure | PASS, 27 source pages. See [validator output](assessment-2026-09-05/evidence/validate-site.txt). |
| Static responsive rows | PASS, 200 rows from 25 routes at eight viewport configurations. This is source inspection, not a rendered-layout result. See [static output](assessment-2026-09-05/evidence/static-responsive.txt). |
| Link check | PASS for 764 internal links and 534 external URL-format checks. This does not establish network reachability of those external destinations. See [link output](assessment-2026-09-05/evidence/links.txt). |
| Generated index and fingerprints | PASS at baseline. See [index](assessment-2026-09-05/evidence/index.txt) and [asset checks](assessment-2026-09-05/evidence/cache.txt). |
| Canonical local audit | FAIL at baseline because eight ignored `.DS_Store` files were found. No source-content finding was reported. See [audit report](assessment-2026-09-05/evidence/canonical-audit.md). |
| Local browser baseline | First run recorded two timeout-related console failures on Scheels at larger viewports. Do not treat the 200 visited rows as a clean pass. See [browser evidence](assessment-2026-09-05/evidence/browser-responsive-baseline.json). |
| Local full pytest | NOT RUN because pytest was unavailable in the inspected local runtimes. The worker's focused standard-library safety tests are a separate result. |
| Production and CI | Use the Architect's dated remote and HTTP evidence in the assessment folder. A baseline hosted success does not validate subsequent local changes. |

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

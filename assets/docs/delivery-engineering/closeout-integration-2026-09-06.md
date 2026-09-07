# Closeout integration evidence

Status: **LOCAL ACCEPTANCE CLEAR**

This record covers the local integration candidate after the current remote
main was merged. It records local evidence only. It does not establish that
CI, GitHub Pages, DNS, analytics, or external links remain healthy after a
future publication.

## Candidate and scope

| Item | Value |
| --- | --- |
| Worktree | `/Users/okh/.codex/worktrees/release-askjamie` |
| Branch | `codex/release-candidate-20260905` |
| Candidate commit | `9dfeeb5e003dd727d5b7569ff9978f07f2589129` |
| Integrated `origin/main` | `3d1685ccc065ebc284d86a25f89e82afbecfcbd2` |
| Relationship | `origin/main` is an ancestor of the candidate |
| Writes outside candidate worktree | None |
| Publication | Not performed |

The integration retained the current Universe Map implementation, its skill,
generator, generated map data, and browser coverage. It retained the candidate
release evidence and regression coverage when the search-QA branch proposed
their removal. It also retained search suggestion display labels and the IME
composition-key guard. Shared asset references, CSP metadata, and the search
index were regenerated from the resolved source.

## Local commands and results

Commands used `/tmp/askjamie-venv/bin/python3` (Python 3.14.5) and
`/Users/okh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`
(Node 24.19.0). The installed local Playwright runtime supplied Chromium for
browser checks.

| Command | Result | Durable evidence |
| --- | --- | --- |
| `python3 scripts/validate-site.py` | Pass. 27 HTML pages clean. | Console result from this integration run. |
| `python3 -m pytest` | Pass. 67 tests. | Console result from this integration run. |
| `python3 scripts/check-links.py` | Pass. 794 internal and 543 external links, 0 broken, 0 style issues. | `assets/audit/links-report-2026-09-06.json` |
| `python3 scripts/cache-bust.py --check` | Pass. 36 pages and templates, 0 stale. | Console result from this integration run. |
| `python3 scripts/build-search-index.py --check` | Pass. 25 pages indexed. | `assets/data/search-index.json` |
| `python3 scripts/audit-site.py --quiet` | Pass. 0 issues. | `assets/docs/audit-report.md` |
| `node scripts/responsive-qa.mjs --base=http://127.0.0.1:5000` | Pass. 25 routes by 8 viewports, 200 of 200 checks. | `assets/docs/delivery-engineering/evidence/2026-09-05-release-candidate/responsive-qa/closeout-integration-200-of-200.json` |
| `node tests/test_universe_map.spec.mjs` | Pass. 25 indexed pages, 6 diagrams, two widths, both themes, keyboard and no-JavaScript links. | Console result from this integration run. |
| `node tests/test_js_smoke.spec.mjs` | Pass. Mermaid, search overlay, dark mode, deferred app, and fingerprinted analytics. | Console result from this integration run. |
| `node scripts/experience-qa.cjs` | Pass. Search, internal-anchor, motion, navigation, visibility, card, and contrast checks. | Console result from this integration run. |

The browser suite used the local preview at `http://127.0.0.1:5000` with
external requests blocked by the test harness where applicable. The copied JSON
is the exact 200-row rendered-browser result from this integration run. It is
not a hosted verification.

## Final source correction

`scripts/responsive-qa.mjs` now describes its concurrency limit as an empirical
four-worker cap used to limit browser request bursts. The old comment made an
unsupported claim about Python CLI server implementation details. This was a
comment-only correction and did not change rendered site behavior.

## Limits

- The candidate has not been pushed or deployed by this integration task.
- Local browser checks do not prove a GitHub Actions run, GitHub Pages, the
  custom domain, external font availability, analytics delivery, or human
  assistive-technology output.

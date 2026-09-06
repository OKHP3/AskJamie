# Integrated validation and local changes

Date: September 5, 2026. Baseline: `fd1ea19`. Target: AskJamie only.

## Result

The assessment, delegated first implementation batch, and local review are complete. The patch remains uncommitted and unpublished. This is not a clean release clearance: the canonical local audit still reports eight existing ignored macOS metadata files, the local full pytest suite is unavailable, and intermittent local responsive-test timeouts remain unresolved.

The bounded repairs have direct regression evidence. All 11 focused experience checks, all 15 packaging/scratch/transport regression tests, and the existing JavaScript smoke test pass. Source validators, generated-file checks, and packaged HTML resource closure also pass. Baseline CI passed before these local changes; it has not run against this patch.

## What changed and why

| Scope | Local change | Validation |
| --- | --- | --- |
| `assets/js/app.js` | AskJamie-specific search label, placeholder, suggestions, and no-results help; explicit dedicated-search Enter/Escape behavior with composition and modifier guards; opt-in reveal readiness | 11 focused browser cases including delayed index load and latest query, default-brand fixture, return focus, empty results, and no-JavaScript behavior |
| `assets/css/theme.css` | AskJamie footer text/link selectors now outrank inherited dark-footer rules; content is visible before enhancement initializes | Normal-text contrast minimum 6.24:1 in tested light scheme and 6.75:1 in dark scheme; no-JavaScript and blocked-app-script content tests |
| Public HTML and nine templates | Generated shared asset URL fingerprints and CSP hashes updated to reflect the CSS/JS changes | 36 page/template fingerprints current; 27 page CSP checks pass. These widespread diffs are generated references, not a broad copy rewrite |
| `scripts/prepare-pages-artifact.py` | Output ownership and path checks precede deletion; hidden incidental files, symlinks, and PDN artwork excluded; `.well-known` retained | 15 standard-library regression cases; real artifact generated and inspected; source artwork remains |
| Source collectors and two existing scanner tests | `.scratch` explicitly excluded from source inventory so generated artifacts do not become source pages | Scratch fixture and CSP collector regressions; final 27-page and 25-route/index counts |
| `.github/workflows/validate.yml` | Prepare fresh `.scratch/pages-release`, upload that exact path with intentional hidden-file transport, run focused experience suite in existing browser job | Source/configuration review and transport regression. Workflow has not executed for the uncommitted patch |
| `scripts/experience-qa.cjs`, `tests/test_pages_artifact_safety.py`, scripts inventory | Repeatable regressions for the actual repaired failures | Tests run against existing runtimes; no dependency or browser installation |
| AGENTS, README, ROADMAP, Replit notes, scorecard, ADR clarifications | Current architecture, inventory, workflow, security-header and evidence claims reconciled | Scoped diff review and local Markdown reference checks. Historical ADR decisions preserved with dated notes |
| Assessment directory | Architect assessment, 14-package delivery plan, domain reports, route/source ledger and evidence | Cross-domain synthesis, current-source reconciliation, explicit unknowns and before/after review |

The search index content remained unchanged after regeneration. No branch was deleted, no recovery ref was pruned, no source artwork was deleted, and neither sibling repository was changed. The original clean clone was fast-forwarded by one already merged commit before assessment. No external messages, issues, PRs, or deployment actions were sent.

## Executed checks

Final source check commands and exit statuses are in [final-command-checks.json](evidence/final-command-checks.json).

| Check | Status | Evidence and boundary |
| --- | --- | --- |
| Structural validator | PASS | 27 HTML pages clean; `python3 scripts/validate-site.py` |
| Static responsive baseline | PASS, limited | 25 routes x eight viewports = 200 source-check rows. This is not a browser layout result |
| Internal links and external URL syntax | PASS | 27 pages, 764 internal links, 534 external URL references; zero broken internal links/style issues. External reachability is a separate probe |
| Search index freshness | PASS | 25 pages; `python3 scripts/build-search-index.py --check` |
| Asset fingerprints | PASS | 36 pages/templates, zero stale references; `python3 scripts/cache-bust.py --check` |
| CSP generator check | PASS, limited | 27 pages; `python3 scripts/generate-csp.py --check`. See infrastructure report for limitations of this checker and delivered-header evidence |
| JavaScript syntax | PASS | `node --check` for shared app and Mermaid initializer |
| Packaging regressions | PASS | 15 tests; `python3 -B -m unittest tests.test_pages_artifact_safety -v`; [output](evidence/artifact-regressions-final.txt) |
| Focused experience regressions | PASS | 11/11 on dedicated local server at port 5187; [JSON](evidence/experience-qa-final.json) |
| Existing JavaScript smoke | PASS | Mermaid SVG and no-JavaScript fallback, search overlay, theme persistence, deferred app, and single analytics initialization/event; [output](evidence/js-smoke-final.txt) |
| Full responsive browser suite | FAIL, intermittent | Latest full run: 199/200 passing, two timeout console messages in Dollar General/1280px row; [JSON](evidence/browser-responsive-dedicated-server.json) |
| Focused responsive diagnostic rerun | PASS, limited | All five routes implicated across earlier runs, eight widths each: 40/40. Retains console resource locations. Does not erase preceding full-suite failures; [output](evidence/targeted-responsive-diagnostics.txt) |
| Canonical local audit | FAIL, preexisting hygiene | Eight ignored `.DS_Store` paths; no page-content findings. The report's synthetic repo-cruft row is not a 28th source HTML page; [report](evidence/canonical-audit-final.md) |
| Full local pytest | NOT RUN | Neither system nor bundled Python has pytest. No substitute or installation was represented as a pass |
| Baseline GitHub CI | PASS, historical to patch | Baseline SHA `fd1ea19`: 36 pytest tests, 200 browser rows, smoke, artifact and deployment success in [run 33979307147](https://github.com/OKHP3/AskJamie/actions/runs/33979307147). Does not validate this uncommitted patch |
| Final artifact HTML resource closure | PASS | 27 HTML files, 885 local href/src/srcset references, zero missing targets; [JSON](evidence/artifact-link-closure.json). Does not exercise external links or every CSS/runtime request |
| Live baseline HTML parity | PASS | 27/27 HTTP 200 and exact source-byte equality before edits; [HTTP evidence](evidence/hosted-http.json) |
| External GPT availability | MIXED | 13/17 HTTP 200, four 404 confirmed in fresh browser context. No inference about reason or GPT conversation quality; [probe](evidence/public-gpt-probe.txt) |
| Hosted patch verification | NOT RUN | No commit, push or deployment. Live behavior remains the baseline |
| Fresh Lighthouse, real-user metrics, human screen-reader output | NOT RUN | Historical lab report is labeled as such; no current performance or accessibility certification |
| Whitespace | PASS | `git diff --check` |

## Diagnostic history

The baseline full browser run returned 198/200 passing with two Scheels timeout rows. The first integrated run under concurrent browser work returned 195/200, including an image request failure. These logs are retained in `evidence/browser-responsive-baseline.json` and `evidence/browser-responsive-final.json`.

The original preview used port 5000, where macOS Control Center also listened on other interfaces, and its request log was attached to an undrained tool stream. Those were plausible test-environment contributors, not proven causes. The agent stopped its own Python process and started a dedicated port 5187 server with file logging. The serial full suite still had one failing row. A diagnostic rerun of all previously implicated routes passed 40/40. The underlying intermittent timeout remains unknown; further QA should capture resource URLs, server backlog and failed-request timing rather than suppressing errors.

The first integrated experience run failed an immediate computed-opacity assertion after changing the browser's motion preference. The Worker added a bounded three-second wait for every reveal element to reach the same required opacity of one. The original zero-hidden assertion remains. The isolated case and the subsequent full 11-case run passed. No runtime or CSS change was made to conceal the test timing failure. [First integration result](evidence/experience-qa-integration-first.json)

## Artifact acceptance

Final generated artifact: `.scratch/pages-release`. Final file count: 312. Size: 114,581,705 bytes. Manifest SHA-256: `2538800e29b1b74e3feeb69e3f1c8d4a32b6c62df311deb7d9e62c945c7f0486`.

All 27 HTML pages and their checked local references are present. `.well-known/security.txt` is included. No incidental hidden files, PDN files, or symlinks are admitted. Both source PDN files remain. The approximately 15.5 MB omitted from the baseline candidate is mostly editable artwork; this is an archive reduction, not a measured page-load improvement.

The tracked historical `dist-pages` tree and its stale sidecar were preserved. The guarded builder intentionally refuses to overwrite an existing output that no longer matches its ownership manifest. Use a fresh output path or investigate an existing output rather than deleting it to bypass the guard.

## Visual review

The repository capture script ran with `OUTPUT_DIR` redirected to a review location. Homepage, BrandGuard card and Universe captures were inspected at 1280px and 390px. Committed baseline images were not replaced: the capture routine can freeze reveal animation partway through and does not scroll all lazy/revealed content before whole-page capture. Initial captures under the overloaded preview also lacked some images. Those outputs were rejected as reference replacements.

Separate focused captures show repaired footer and search states plus visible no-JavaScript content under `evidence/screenshots/`. The new [dated performance and visual review](performance-and-visual-review-2026-09-05.md) records the intentional changes and remaining visual findings. There is no new Lighthouse score.

One additional confirmed follow-up emerged during reference review: BrandGuard hub card anchors retain `display: inline`, producing fragmented padding/borders around block descendants. The 390px first-card inspection returned three client rectangles. This predates the patch and was not silently redesigned in this batch. Correct the link-card layout and stabilize screenshot capture in the next bounded visual task; preserve link semantics and test all 13 cards.

## Remaining release conditions and next work

1. Review this patch and run the full pytest/CI suite in the supported repository environment.
2. Resolve or explicitly disposition the existing eight macOS metadata files, retaining the baseline audit evidence.
3. Diagnose intermittent responsive-run failures; add useful error/resource evidence rather than converting the failed run into a pass.
4. Follow the delivery plan for the four unavailable GPT destinations, prototype/affiliation copy, ten Notion-linked case pages, skip-link/search semantics, inline BrandGuard cards, merge protections and unsafe synchronization tooling.
5. After separately authorized publication, verify exact deployed content, corrected search/footer behavior, `.well-known/security.txt`, and the preserved public artifact boundary.

The next work is scoped in [delivery-plan.md](delivery-plan.md). Assessment completeness does not mean every proposed improvement has been implemented or that all release conditions are satisfied.

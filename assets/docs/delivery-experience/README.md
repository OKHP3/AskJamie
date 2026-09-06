# Experience delivery ledger

Date: 2026-09-05. Scope: WP-06, WP-07, WP-08, WP-12, and WP-13 in the
AskJamie worktree. These records separate implemented local changes from
owner decisions, human testing, and publication.

## Worker and integration record

| Item | Status | Evidence |
| --- | --- | --- |
| WP-06 interaction acceptance | Implemented and regression-covered | BrandGuard card layout, skip-link focus, reduced-motion anchor behavior, mobile-menu focus return, and search behavior have focused browser evidence and persistent regressions. |
| Worker dispatch | Completed | Cards/browser worker `01a074ba-0893-7de1-8360-804e7a8b55f3`, source turn `01a074b5-0eae-7200-94ea-18204c90a896`, committed `800bfef`; performance worker `01a074ba-3a28-7bf0-9b2b-00393852549f`, committed `d06f7c0`. Both used GPT-5.4-mini with medium reasoning. |
| CSS generator follow-up | Completed locally | `cache-bust.py` updated 36 references; `generate-csp.py` verified 27 policies |
| WP-07 availability and claims | Decision packet | `wp-07-claims-decision.md`; no unsupported destination or credential claim changed |
| WP-08 public-source routes | Inventory and decision packet | `wp-08-public-source-inventory.md`; private locators intentionally omitted |
| WP-12 performance/capture | Partial, with bounded local improvement | Capture readiness and failure-path tests are implemented. A nav-only 80px avatar reduced sampled local request bytes. Repeated performance attribution, LCP, and field evidence remain incomplete. No original asset was deleted or committed baseline replaced. |
| WP-13 human usability | Test packet | `wp-13-human-test-packet.md`; human execution remains pending |

## Validation in this worktree

- PASS: `python3 scripts/validate-site.py`
- PASS: `python3 scripts/cache-bust.py --check`
- PASS: `python3 scripts/generate-csp.py --check`
- PASS: `git diff --check`
- PASS: browser experience QA 18/18 using the bundled Playwright runtime and a dedicated local server; external requests were blocked
- PASS: BrandGuard card geometry at 1280px, 390px, and 320px: 13/13 cards had one client rect and no document overflow
- PASS: worker browser probe confirmed skip-link focus to `MAIN#main`, mobile-menu focus return, card activation, search behavior, and reduced-motion behavior
- PASS: worker capture harness produced 8/8 route/viewport captures with zero response errors and all sampled images loaded
- PASS: `node --test tests/test_capture_visual_baseline.mjs` covers unsafe output destinations, incomplete images, failed requests, readiness timeouts, image-scale calculation, and nav-avatar selection
- NOT RUN: the full Python test suite against this exact integration tip. Engineering owns the separate full-browser diagnosis.

The BrandGuard card change and related interaction fixes are browser-validated
in this worktree. The 18 focused checks include persistent skip-link,
reduced-motion anchor, and mobile-menu focus-return regressions. This focused
result does not clear Engineering's separate failed 196/200 full-browser run.

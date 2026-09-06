# Experience delivery ledger

Date: 2026-09-05. Scope: WP-06, WP-07, WP-08, WP-12, and WP-13 in the
AskJamie worktree. These records separate implemented local changes from
owner decisions, human testing, and publication.

## Worker and integration record

| Item | Status | Evidence |
| --- | --- | --- |
| WP-06 BrandGuard card layout | Implemented locally | `assets/css/theme.css`; `scripts/experience-qa.cjs`; 13-card assertion added |
| Worker dispatch | Blocked by tool validation | Two bounded `create_thread` requests for project `AskJamie` were rejected before a worker task was created. No worker ID or worker commit exists. |
| CSS generator follow-up | Completed locally | `cache-bust.py` updated 36 references; `generate-csp.py` verified 27 policies |
| WP-07 availability and claims | Decision packet | `wp-07-claims-decision.md`; no unsupported destination or credential claim changed |
| WP-08 public-source routes | Inventory and decision packet | `wp-08-public-source-inventory.md`; private locators intentionally omitted |
| WP-12 performance/capture | Measurement packet | `wp-12-measurement-readiness.md`; no asset deleted or replacement baseline accepted |
| WP-13 human usability | Test packet | `wp-13-human-test-packet.md`; human execution remains pending |

## Validation in this worktree

- PASS: `python3 scripts/validate-site.py`
- PASS: `python3 scripts/cache-bust.py --check`
- PASS: `python3 scripts/generate-csp.py --check`
- PASS: `git diff --check`
- PASS: browser experience QA 15/15 using the bundled Playwright runtime and a dedicated local server; external requests were blocked
- PASS: BrandGuard card geometry at 1280px, 390px, and 320px: 13/13 cards had one client rect and no document overflow
- NOT RUN: full pytest because the local environment has no pytest

The card change is therefore source-validated but not browser-validated in
this worktree. The prior 11/11 experience result remains evidence for the
pre-existing checks only, not for this new card assertion.

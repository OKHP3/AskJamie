# Translation prototype cleanup

Date: September 5, 2026. Repository: `OKHP3/AskJamie`.

## Result and scope

The confirmed leftovers were duplicate implementations, hidden test coverage,
inherited locale assumptions, and a broken stale-record adoption path. The
`i18n-page-sync` package itself belongs to the current skill-based workflow.
It is a Python drift detector, not a superseded browser translation engine.

Work was delegated through the Project Architect, Project Manager, and one
tooling Worker. The Architect handled browser behavior and integration; the
Manager and Worker handled the translation packages and automation. Existing
assessment changes remain intact. All changes are local and uncommitted.

## Changes and disposition

| Surface | Disposition | Reason |
| --- | --- | --- |
| Five exact-pair translation skill packages | Retained | Separate `en-US` targets `de-DE`, `en-UK`, `es-ES`, `es-MX`, and `fr-FR` are intentional. No translated content was authored in this cleanup. |
| Ten underscore-named planner/validator copies | Removed | Their stronger hyphenated counterparts are the documented canonical commands. Exact comparison and path mapping are retained below. |
| Five hyphenated test-file copies | Consolidated | Stronger ten-case suites now occupy discoverable `test_*.py` names and invoke the canonical helpers. Older eight-case suites had no unique cases. |
| Drift detector and its `i18n` paths | Retained and corrected | This tool detects missing/stale content for the current exact-pair skills. Its explicit adoption step must support reviewed updates as well as first baselines. |
| GitHub translation workflow | Clarified and extended | Report missing configuration explicitly and run the helper regressions even before a pilot is configured. |
| AskJamie search locale mapping | Corrected | AskJamie has only `assets/data/search-index.json`. Draft pages must not request an absent French index. Non-English draft fixtures get an English-search scope notice. |
| Shared language-switch CSS and JavaScript | Retained, comments corrected | No AskJamie page or template supplies switcher markup. This is recently maintained family foundation code, with sibling consumers, rather than proven obsolete code. It remains inactive here. |
| Self-language alternate on holding page/template | Retained | A self-reference is not evidence of a translated route and is not a broken link. |
| Historical translation benchmarks and provenance | Retained | Dated commands describe earlier evidence. Package guidance records the test-path migration rather than rewriting history. |
| Generated full skill catalog | Separate follow-up | The catalog is stale, but regeneration is blocked by an unrelated duplicate janitor skill package. The Manager added a targeted translation map outside the generated section. |

The shared default-brand French index mapping remains intact for family
consumers. AskJamie's body class now selects only its real English catalog.
A future locale launch must deliberately connect an actual generated index;
changing an HTML language attribute is insufficient.

## Current activation boundary

Confirmed from source and the detector: no `i18n/sync.config.json`, no
`i18n/sync-state.json`, no published translated routes, no locale search indexes,
and no language-switcher markup. A successful unconfigured check proves no
translation coverage or quality.

The intended sequence remains:

1. Choose the owner-approved exact language pair and route scope.
2. Use that pair's skill to prepare a source-bounded plan, draft, manifest,
   protected terms, and voice review.
3. Validate the draft and review its language quality and AskJamie voice.
4. Configure the detector for only the selected routes and target locale.
5. After a reviewed draft/update exists, explicitly adopt its source baseline.
6. Before publication, validate actual page navigation, canonical/hreflang
   relationships, sitemap/index inclusion, search behavior, and the paper-first
   language control. Run the site's release checks.

Python helper checks and hash synchronization are not language-quality review.
The detector does not draft, invoke an external translation API, or publish.
No pilot locale or route scope has been invented during this cleanup.

## Validation

The final tooling results are recorded by the Worker and Manager in this
directory. Browser and source checks completed by the Architect:

| Check | Result |
| --- | --- |
| Translation helpers and drift detector | 60/60 passed: ten tests in each of five language-pair suites and ten detector tests. The exact CI shell block also passed locally. Python 3.14 ran locally; GitHub's configured Python 3.11 run has not been triggered. |
| Workflow configuration summaries | Configured/unconfigured fixtures and shell syntax passed. Workflow/job identities and pinned Actions were preserved. |
| `scripts/experience-qa.cjs` | 14/14 passed, including three locale draft fixtures, shared cached English catalog, existing search interactions, content fallback, and contrast. External requests were blocked for deterministic local checks. |
| `python3 scripts/validate-site.py` | Passed, 27 public/utility HTML pages. |
| `python3 scripts/cache-bust.py --check` | Passed, 36 page/template references current after regeneration. |
| `python3 scripts/generate-csp.py` | Verified 27 policies. |
| `python3 scripts/build-search-index.py --check` | Passed, 25 content pages. |
| `python3 scripts/check-links.py` | Passed, 764 internal and 534 external link records, zero broken links or style issues. This is the script's coverage, not a new live verification of every outbound destination. |
| `node scripts/responsive-qa.mjs --static` | Passed, 200 source-lint rows. This does not establish rendered behavior at 200 viewport combinations. |
| `node --check assets/js/app.js` | Passed. |
| `python3 scripts/audit-site.py --quiet` | Failed on the same eight ignored `.DS_Store` findings as the preceding assessment. No new translation finding. |
| `python3 -m pytest` | Not run: local Python has no pytest. Standard-library skill suites and focused browser tests are separate results. |

The first browser attempt could not connect because the earlier local preview
server had ended. After restarting the task-owned server on port 5187, all
14 cases passed. No visual design or new translated page was introduced.

## Git and publication boundary

Local `HEAD` is `fd1ea19`. During this cleanup, a read-only fetch found remote
`main` at `1d969b6`. The remote change adds a `100vh` language-menu height
fallback before `100dvh` plus generated asset references. Its source fallback
was preserved in the working tree and asset fingerprints were regenerated.
The dirty tree was not merged, rebased, committed, pushed, or deployed. Git
history reconciliation and final release validation remain necessary before
publication of the combined assessment and cleanup changes.

## Evidence

- [Browser regressions](experience-qa.json)
- [Duplicate inventory](duplicate-inventory.json)
- [Exact implementation differences](duplicate-comparison.diff)
- [Applied tooling file ledger](applied-tooling-changes.json)
- [Final tooling tests](final-tool-execution-results.json)
- [Exact workflow regression execution](workflow-regressions.json)
- [Worker tooling audit](translation-tooling-audit.md)
- [Manager cleanup decisions](cleanup-decisions.md)
- [Original stale-adopt reproduction](i18n-stale-adopt-fixture.json)
- [Catalog blocker evidence](catalog-evidence.json)
- [Original comprehensive assessment](../assessment-2026-09-05/architect-assessment.md)

The duplicate diffs and historical Git objects preserve why each older copy
was removed. They are reference evidence, not another runnable implementation.

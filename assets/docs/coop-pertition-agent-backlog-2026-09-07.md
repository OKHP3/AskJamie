# AskJamie coop-pertition: 32 agent task briefs

Date: 2026-09-07. Status: proposed task queue, not a dispatch or completion record.

24 tasks address AskJamie Found-Ry. Eight address the AskJamie website. All
delegate roles below belong to ChatGPT/Codex agent threads. Replit retains its
own reconciliation, environment and workspace execution responsibilities.

The purpose is to turn the existing alpha into a more dependable capability
workbench and make its public explanation easier to discover and trust. Each
task produces a bounded artifact, a useful regression check, a verified fix,
or a specific finding. An already-correct behavior is a valid result. Agents
must not invent defects or add redundant tests to justify an assignment.

## Evidence and scope

Read-only planning inspected the two local repositories. Their starting trees
were clean. No fetch, runtime acceptance, live deployment verification or Replit
ownership confirmation was performed for this plan.

| Claim | Tier | Evidence | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| The website source inspected was `e9902c5358506252ae0aba8b805c26f7f9d18924` | CONFIRMED | Local Git HEAD and `AGENTS.md` in AskJamie | Tasks could target a superseded tree | Refresh the baseline before dispatch |
| Found-Ry source inspected was `af0dcc339435e0370cb3729150aeaa1b4b689b0c` | CONFIRMED | Local Git HEAD and `AGENTS.md` in AskJamie-FoundRy | Contracts or path ownership could change | Record the current SHA and shared task claims |
| Found-Ry source is intentionally public; local drafts and protected capabilities remain private | CONFIRMED as repository policy | Found-Ry `AGENTS.md` and `docs/agent-collaboration.md` | Public-source and private-data boundaries would be misstated | Preserve controls and verify export behavior separately |
| The source contains a Python/SQLite workbench, deterministic decisions, evaluations and ZIP exports | CONFIRMED as source presence | `workbench/model.py`, `store.py`, `service.py`, `server.py`; existing tests | Source presence could be mistaken for operational acceptance | F01 and the focused acceptance tasks |
| Existing tests already address core revisions, protection, graph errors, export isolation and HTTP guards | CONFIRMED as test presence | `tests/test_workbench.py`, `tests/test_registry_validation.py` | Duplicate tests would waste time and tokens | Map existing coverage before adding a missing case |
| Replit's currently owned paths and exact active revisions are known | UNKNOWN | Historical Replit observations and collaboration instructions do not establish live ownership | Concurrent agents could overwrite or duplicate work | Read the shared issue/PR record and obtain owner acknowledgment |
| Narrow-screen, exported-runner and backup/restore acceptance deserve early attention | PROPOSAL supported by documented gaps | Found-Ry `docs/current-state-and-maturation.md` | Historical gaps might already be closed | Reproduce against the current baseline first |
| These tasks will reduce cost or improve user outcomes by a measured amount | UNKNOWN | No comparative cost or user dataset was collected | Invented savings or effectiveness claims | Record actual usage, review effort and acceptance outcomes |

Source entry points for future workers:

- Website: `AGENTS.md`, `found-ry/index.html`,
  `assets/docs/foundry-feature-page.md`, `assets/docs/project-scorecard.md`,
  and `assets/docs/assessment-2026-09-05/delivery-plan.md`.
- Found-Ry: `AGENTS.md`, `docs/agent-collaboration.md`,
  `docs/current-state-and-maturation.md`, `docs/workbench-contract.md`,
  `docs/workbench.md`, `workbench/`, and the existing tests.
- September 5 plans and September 7 feature notes are dated records. Inspect
  current code and Git history before treating their pending items as open.
- The website is a static HTML site. Found-Ry owns its separate Python
  application. Neither architecture nor the application's visual profile
  should be copied automatically into the other repository.

## Lower-cost routing

Use the least expensive available model and reasoning effort that can complete
the bounded task. This follows Found-Ry's existing collaboration protocol;
it makes no fixed price or subscription assumption.

| Route | Suitable work | Initial approach |
| --- | --- | --- |
| S: small general model | Inventories, documentation, fixtures, evidence tables, copy proposals | Low reasoning; exact sources and one output contract |
| C: lower-cost coding model | Focused Python/JavaScript tests, browser reproduction, small fixes | Medium reasoning; one behavior and explicit file ownership |
| Coordinator | Ownership conflicts, protection/transaction changes, integration and acceptance | Use stronger reasoning only for the difficult decision or diff |

Every task is a separate thread. Coding tasks use a separate worktree and
branch; do not switch branches in the owner's checkout. S tasks that only read
source can use a report thread. Any file-writing S task also gets a worktree.

Give a worker only its task row, common contract, relevant authority files,
baseline and source pointers. Use scripts for inventories and deterministic
checks. Do not send the whole conversation or all 32 briefs to every model.
After two failed attempts with the same approach, change approach or return
the failure evidence. Escalate the difficult subproblem, not the entire queue.

## Cooperation with Replit

These are complementary assignments, not instructions to change Replit's
existing priorities. The exact current Replit focus remains unconfirmed.

1. Establish one shared issue or PR record per task, as required by the
   Found-Ry collaboration protocol. Record owner, platform, base SHA, branch,
   allowed paths, acceptance criteria and handoff state. This document is a
   proposal and does not itself establish cross-platform ownership.
2. Replit keeps its active branches, Git reconciliation, environment setup,
   workspace-specific validation and any paths already claimed there.
   ChatGPT can independently prepare tests and evidence from a recorded SHA.
3. If the record is unavailable, continue read-only analysis and return a
   public-safe proposed claim. An unconfirmed claim does not authorize taking
   over a runtime or shared file. No owner response is implied by elapsed time.
4. Found-Ry test delegates initially own separate new test files and synthetic
   fixtures. Website delegates own separate reports/tests or explicitly
   allocated page files. They submit minimal patch proposals for shared files.
5. The integrator assigns any confirmed runtime repair to one writer, with
   the reproduction attached. A test/report task is not marked as a completed
   repair while its failing behavior remains unresolved.
6. Compare Replit and ChatGPT results on the same accepted behavior and source
   revision where possible. Preserve independent observations before sharing
   conclusions. Sharing a fixture creates comparable evidence, not independent
   proof of the fixture's correctness.

Measure cooperation by reusable tests and clear handoffs. Measure competition
by accepted findings, useful pilot completion, regression avoidance and total
review effort. Record tokens or cost only when actually available. Do not rank
agents by lines changed, number of tests, or unsupported savings estimates.

## Found-Ry delegates: F01 through F24

All paths in this table are relative to **AskJamie-FoundRy**, not the website.
All tasks first check current coverage. Existing passing tests should be reused;
add a regression only for a meaningful untested behavior. Synthetic fixtures
must use disposable state directories, never the owner's `.foundry-data/`.

| ID / route | Task and source surface | Deliverable and acceptance |
| --- | --- | --- |
| F01 / S | Establish a current capability and test baseline. Read `AGENTS.md`, maturation notes, runtime entry points and existing tests. | A claim-to-source/test matrix and current validation results. Distinguish implemented, tested, documented and unverified. Reconcile already-shipped backlog items; do not claim Replit or remote parity. |
| F02 / S | Clarify public source versus private runtime. Review `README.md`, `replit.md`, `docs/workbench.md` and maturation wording against `AGENTS.md`. | A bounded documentation patch with a contradiction ledger. Explain public source, private drafts, local-only execution and proposed graduation consistently. Update release claims only from verified evidence. |
| F03 / C | Check schema parity. Inspect `schemas/manifest.schema.yaml`, `schemas/registry.schema.yaml`, validators and existing registry tests. | Focused negative fixtures for missing parity cases: malformed types, supported families and private-lock restrictions. Known-valid records still pass. Schema changes require coordinator review. |
| F04 / C | Exercise naming and registry reservations. Inspect `repo_name()` and `validate_project()` in `workbench/service.py`. | A table-driven boundary matrix for reserved/archived codes, duplicate names, aj03 variants and client-parent matching. Assert both allowed and rejected examples without changing the canonical registry. |
| F05 / C | Verify child-template rendering and provenance. Inspect `_template/` and `_generated_files()` in `service.py`. | A generated-package check proving owned template placeholders resolve, scaffold/license requirements survive, `ABOUT.md` stays excluded and template provenance is present. Preserve literal source text that resembles a placeholder. |
| F06 / C | Test draft-input boundaries. Inspect `normalize_draft()` and JSON-shape validation in `workbench/model.py`. | Boundary cases around documented size/depth/type limits and non-finite numbers, reusing existing coverage. Incomplete drafts remain savable where allowed; malformed protected or derived fields are rejected predictably. |
| F07 / C | Test decision-graph validation. Inspect `validate_graph()` and existing graph tests. | Missing graph cases for mixed node shapes, duplicate IDs, empty terminals and malformed branches. Valid graphs pass; invalid graphs fail before preview/export. No graph feature expansion. |
| F08 / C | Verify decision execution semantics. Inspect `run_decision()`, answer validation and the preview API. | A compact truth table with traces for both outcomes, partial answers, invalid answer types and answers to non-question nodes. Missing answers pause rather than silently become No. |
| F09 / C | Verify stale-write handling under contention. Inspect `Store.update()` and the existing stale-revision test. | A deterministic two-writer regression with bounded waits: exactly one update wins, the stale writer receives the documented conflict and no history is lost. Any transaction fix receives coordinator review. |
| F10 / C | Verify revision and evaluation lineage. Inspect `store.py`, evaluation storage and exported evidence. | A create/evaluate/edit/evaluate/reopen sequence proving history is intact and old evaluations remain associated with the revision checked. Exports must not present old results as acceptance of new content. |
| F11 / C | Challenge irreversible privacy controls. Inspect `enforce_protection()` and current protection tests. | A state-transition matrix covering first protection, later identity/flag changes and invalid downgrade attempts. Every denial leaves stored data unchanged. Use invented client names; coordinator reviews any policy-sensitive patch. |
| F12 / C | Verify private-state file handling. Inspect `Store.__init__()`, file-mode tests and operating guidance. | Temporary-directory checks for insecure existing modes, state-file symlinks and SQLite sidecars where supported. Separate POSIX results from untested Windows ACL behavior. No tests against owner data. |
| F13 / C | Check the loopback HTTP boundary. Inspect `workbench/server.py`, the HTTP contract and existing request tests. | Bounded local cases for Host/Origin, write marker/content type, body framing, static allowlist and no-store responses. Rejected writes do not mutate state. No scans or public exposure. |
| F14 / C | Verify ZIP content isolation. Inspect `export_project()`, archive construction and existing isolation assertions. | Two synthetic projects with distinct marker strings. Export A contains only A and selected public metadata, expected manifests and pending proposal, with safe archive paths. No unrelated project, database or full registry content. |
| F15 / C | Execute the exported decision runner in a browser. Inspect `_decision_html()` and generated output. | Run Yes, No, partial path and restart with escaped synthetic text. Verify no external requests. If only loopback serving is possible, report that separately from an actual offline `file:` run. Do not bypass browser policy. |
| F16 / C | Verify evaluation results stay honest. Inspect `evaluate_project()` and supplied-response tests. | Cases for missing responses, empty suites, pass/fail, required/forbidden overlap and literal case-sensitive matching. Missing evidence stays unrun. Labels do not imply model execution or semantic-quality validation. |
| F17 / S | Specify controlled Skillz snapshot refresh. Inspect `workbench/data/README.md`, snapshot metadata and `_selected_skills()`. | A reviewable refresh/checklist contract with source SHA/date, unique IDs, changed/removed entries and selected-skill provenance. Include one synthetic comparison example. Do not refresh data, import skill bodies or edit Skillz. |
| F18 / C | Prove backup and restoration. Inspect `docs/workbench.md` and storage behavior. | Create synthetic projects/history/evaluations, stop the disposable service, copy state, restore to a new directory and reopen. Compare content, revisions, evidence and access modes. Produce a repeatable restore drill; never overwrite a real database. |
| F19 / C | Check workbench keyboard and accessible feedback. Inspect `workbench/static/index.html`, `app.js`, `styles.css`. | Keyboard journeys for create/edit/save/validate/export with labels, visible focus and announced failures recorded. Return minimal repair proposals for owned UI files. Human screen-reader spoken output remains a separate check. |
| F20 / C | Check workbench narrow-screen layout. Use the application's own visual contract. | Reproduce editor, graph controls, evaluations and package views at 390px and 1440px, plus a 320px stress case. Record overflow, clipped controls and screenshot evidence; propose bounded CSS fixes. Preserve the app/site styling distinction. |
| F21 / C | Check unsaved edits and failure recovery. Inspect UI navigation/save/cancel handlers. | A synthetic browser journey covering unsaved navigation, cancel, failed save and stale revision. The draft remains recoverable, status is clear and retries do not silently duplicate or overwrite it. Shared `app.js` fixes are serialized. |
| F22 / S | Build an assistant-specification pilot. Use the current authoring/export contract. | A fictional AskJamie request-clarification assistant with purpose, source, behavior, constraints, output contract and five representative supplied-response cases. Export and inspect it. Label it synthetic, not validated on a model platform. |
| F23 / S | Build a decision-tool pilot. Use the current Yes/No graph contract. | A fictional request-readiness decision guide with at least three questions, explicit clarify/proceed outcomes and a case for each terminal path. Validate, execute and export it; use F15 evidence to distinguish export from runner acceptance. |
| F24 / S | Build a workflow pilot and handoff. Use the current ordered checklist contract. | A fictional capability-handoff checklist covering brief, sources, checks, package and recipient review. Export it and record usability friction. Steps remain human actions. Include a public-safe reusable-pattern note for mentor review without editing a peer repo. |

F22 through F24 may prepare fixtures before browser acceptance is complete.
Completion means a usable synthetic pilot and inspected export. A real owner
pilot, production certification or remote graduation is not implied. Actual
owner material requires its own source and privacy handling.

## Website delegates: W01 through W08

All paths here are relative to **AskJamie**. Preserve static HTML, paper-first
AskJamie branding, external Fonts/GA4 policy, US English and existing owner copy.
Tests and reports do not establish current defects without reproduction.

| ID / route | Task and source surface | Deliverable and acceptance |
| --- | --- | --- |
| W01 / S | Reconcile current documentation and inventory. Inspect `AGENTS.md`, `README.md`, `ROADMAP.md`, scorecard and `assets/docs/foundry-feature-page.md`. | A small patch correcting current counts and stale pending/shipped wording from current source/Git evidence. Preserve dated historical results. Separate merged source from verified Pages deployment. |
| W02 / C | Verify Found-Ry discovery and search. Inspect homepage, How it works, `/found-ry/`, `/search/`, sitemap, universe and generated index. | A visitor journey from homepage to Found-Ry and search queries for Found-Ry/capability/decision guide. Check reachable links and results. Propose ranking or navigation repairs only for a reproduced failure; integrator regenerates data. |
| W03 / C | Verify accessible fallback journeys. Inspect shared browser behavior and representative page markup. | Focus/skip-link, keyboard search, reduced-motion, JavaScript-disabled and Mermaid-fallback evidence on homepage, Found-Ry, Search and Universe. Return bounded fixes for confirmed regressions. Do not call DOM checks screen-reader certification. |
| W04 / C | Check rendered responsive behavior and reference capture. Use `scripts/responsive-qa.mjs` and the existing capture script. | Start with Found-Ry, Contact, a BrandGuard case and Universe; inspect narrow/wide screens and capture readiness. Record the exact routes/widths. Do not replace committed references until an intentional visual change is reviewed. |
| W05 / C | Measure one useful performance improvement. Inspect hero images, shared payload and existing performance tooling. | A declared browser/throttling/cache/sample baseline, then one justified optimization proposal or patch to a uniquely owned asset. Compare the same conditions after change. Preserve typography, branding and analytics policy; do not infer speed from byte counts alone. |
| W06 / S | Check outbound actions and public claims. Inspect Lens System/BrandGuard links and supporting copy. | A dated destination/claim ledger with public access, login requirements, affiliation/prototype framing and any needed public-safe replacement copy. Leave ambiguous destinations for an owner decision. No sign-in, message sending or private Notion copying. |
| W07 / C | Verify the Pages release boundary. Inspect `scripts/prepare-pages-artifact.py`, release tests and `.github/workflows/validate.yml`. | Build into an owned disposable output, confirm `/found-ry/` and required assets survive, and private/draft/source-only material stays excluded. Add only missing boundary regressions. Report artifact evidence separately from live HTTP headers/deployment. |
| W08 / S | Improve Found-Ry-to-contact clarity. Inspect `/found-ry/`, `/how-askjamie-works/` and `/contact/`. | A source-faithful copy proposal showing what a visitor can do now, who the workbench helps and what to include in an inquiry. Test the local route/anchor journey without sending a message. Deliver a before/after diff; no backend, public-app promise or invented impact claim. |

W06 may check public URLs read-only when dispatched. A URL-format pass is not
a reachability pass. W05 must report missing measurement tools rather than
install new dependencies without the authorization required by `AGENTS.md`.

## File ownership and outputs

Reserve branch names such as `codex/coop-f09-stale-write` and
`codex/coop-w02-discovery` only when creating an actual task. The names here
are proposals, not existing branches.

- Each worker owns `docs/agent-results/<task-id>/` in Found-Ry or
  `assets/docs/agent-results/<task-id>/` in the website for its public-safe
  report and synthetic fixtures. Keep personal, client and private runtime
  evidence outside tracked output.
- Python tests use a distinct discoverable file such as
  `tests/test_f09_stale_write.py`, consistent with the existing unittest test
  convention. Browser checks use unique lowercase kebab-case names consistent
  with the target repository's runner. Reuse existing harnesses; do not add a
  new test framework just to make tasks look independent.
- Found-Ry `model.py`, `store.py`, `service.py`, `server.py`, static `app.js`,
  static styles, schemas and authoritative registry have one assigned writer
  per file at a time. A separate worktree prevents checkout collisions but
  does not remove integration conflicts.
- Website `theme.css`, `assets/js/app.js`, workflow definitions, shared page
  shells and `found-ry/index.html` also require single-writer allocation.
  W08 owns only a copy proposal until that page is allocated for implementation.
- Read `assets/docs/sister-site-sync.md` before any website shared CSS/JS
  repair. This queue does not authorize edits in sibling sites or Skillz.
- Only the website integrator runs the final shared fingerprint, CSP,
  search-index and universe generators and reviews their combined diff.
  Never hand-edit generated JSON, `dist-pages/` or generated audit reports.

No public thread, issue or PR receives a real SQLite file, secret, client
source, private draft or private account locator. Public source availability
does not change runtime privacy or permanent-private controls.

## Sequence and integration

Maintain two integration lanes, one per repository. The coordinator is an
oversight role, not a thirty-third lower-cost task counted toward this queue.

1. **Baseline and ownership:** F01 and W01 first. Identify current task claims
   and Replit reservations. Prepare F02 and the three synthetic pilot fixtures.
2. **Highest-value acceptance gaps:** prioritize F15 exported runner, F18
   restoration, F19 keyboard, F20 narrow screen and F21 unsaved work. In the
   website lane start W02 discovery and W07 release closure. Run a small number
   of independent workers at once, for example two Found-Ry and one website.
3. **Contract checks:** F03 through F14, F16 and F17 after F01. Select uncovered
   cases first. Group review by file ownership; do not run twelve workers
   competing to rewrite `service.py` or shared tests.
4. **Usability and pilots:** W03 through W06 and W08, plus completion of
   F22 through F24. F15 and F18 depend on the working baseline. Their tests can
   run in parallel with the other focused checks using separate temporary data.
5. **Repair and integration:** review findings, assign confirmed fixes to their
   single writer, bring accepted changes into the appropriate integration
   branch, and rerun impacted acceptance checks. Review policy-sensitive
   changes independently from their author.
6. **Final validation and handoff:** run the required integrated suite on each
   final candidate. Hand Replit exact commit references and reproduction steps
   through the authorized shared record. Replit verifies its own environment.
   Publication and remote settings follow the user's actual authorization.

Each result records task ID, owner, model/effort used, repository, base/tested
SHA, branch, owned paths, checks, failures/skips, evidence, proposed repairs,
remaining questions and next owner. Track status as proposed, claimed, working,
ready-for-review, integrated or blocked. Do not label a task complete merely
because a thread exists or a model produced a final message.

## Common dispatch prompt

Use this contract with exactly one task row and its cited source pointers:

> You are the ChatGPT/Codex delegate for TASK-ID in TARGET-REPOSITORY. Complete
> only its stated deliverable and acceptance criteria using the least expensive
> suitable available model. Read the repository's AGENTS.md and applicable
> collaboration rules. Record the baseline SHA, inspect existing tests and the
> current shared ownership record, and preserve Replit's claimed paths. Work
> in your assigned isolated worktree for any edits. Use synthetic fixtures and
> disposable application state. Own only your allocated files; propose changes
> to shared files until the integration owner assigns them to you. Reproduce
> before fixing. Prefer a small meaningful check to duplicate coverage. Preserve
> public-source/private-data distinctions, permanent-private controls, lineage
> and the target repository's architecture and brand. Do not add dependencies,
> expose the local app, create remote repositories, publish, change settings,
> send messages to others or edit siblings under this task. Return the exact
> diff or proposal, commands and environment, actual results including failures
> and skips, evidence tied to the tested tree, and any unresolved repair. After
> two failures with the same approach, change approach or hand off evidence.

When a shared claim requires an external post and sending is not authorized,
prepare the exact claim text for the owner rather than asserting it was posted.

## Validation of future changes

Found-Ry baseline/final checks, using its configured environment:

```bash
python3 scripts/validate-manifest.py manifest.yaml
python3 scripts/check-registry.py
python3 -m unittest discover -s tests -v
```

Run targeted tests during a task and the integrated suite after accepted
runtime/export/validation changes. Browser acceptance uses a loopback service
with a unique port and disposable `--data-dir`. Record what actually ran.

Website final checks for affected source changes:

```bash
python3 scripts/validate-site.py
python3 scripts/check-links.py
python3 -m pytest
python3 scripts/cache-bust.py --check
python3 scripts/build-search-index.py --check
node scripts/responsive-qa.mjs --static
python3 scripts/audit-site.py --quiet
```

Rendered changes also require relevant browser QA and smoke checks. Static
responsive rows are not browser evidence. For source changes requiring generated
outputs, the integrator follows the generation order in `AGENTS.md` and reviews
the generated diff before final checks.

This planning artifact changes no runtime, public page, registry, dependency,
workflow or Replit workspace. The queue has been checked for 24 distinct F
tasks, eight distinct W tasks, scoped outputs and acceptance criteria. Task
execution, current Replit claims, real-user pilot acceptance and measured model
cost remain open. Their next checks are dispatch ownership, the baseline task,
the scoped pilot and actual usage records respectively.

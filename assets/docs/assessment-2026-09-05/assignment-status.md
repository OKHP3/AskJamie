# Architect assignment status

## Verified closeout, September 8, 2026

The original Architect implementation and evidence were integrated through
[PR 28](https://github.com/OKHP3/AskJamie/pull/28) at
`dae67306100a50c7ab9c1489a3453653be9512c4`. That release is an ancestor of
`origin/main` at the closeout inspection (`9e51286`). The original release's
[validation and Pages deployment](https://github.com/OKHP3/AskJamie/actions/runs/34076448894)
passed. Later source and route counts supersede its dated 67-test and
200-row browser baseline.

The seven original PM and Worker threads listed below were verified completed
and archived on September 8. Their seven worker worktrees and the combined
release worktree were removed during the earlier publication closeout. The
completed release branch was merged and removed. Recovery refs, a Git bundle,
and archived local QA evidence remain preserved. No squash or history rewrite
was necessary to preserve the integrated work.

Implementation completion is not completion of every proposed outcome:

- WP-07: owner decisions on GPT availability, status wording, and supported
  claims remain open in the decision packet. Historical URL probes are not
  current availability proof.
- WP-08: private-source publication scope and destination decisions remain open.
- WP-13: human assistive-technology and usability execution remains open.
- WP-14: external governance and measurement decisions remain open.
- WP-12: local capture and request-size improvements are complete; lab results
  do not establish field performance or real-user outcomes.

New Found-Ry delegation and repository reconciliation were active in separate
threads during this inspection. Their queue, PRs, and worktrees are outside
this original assignment record and must not be deleted or labeled complete
because the original Architect implementation has shipped.

## Historical dispatch and acceptance record

The sections below preserve the original sequence. Statements such as local,
provisional, pending, or not published describe their recorded stage and do
not supersede the verified closeout above.

## Corrected delivery status

The first assessment delegated and implemented WP-01 through WP-04, followed
by the translation cleanup. WP-05 through WP-14 were documented proposals;
they had not been dispatched as active implementation assignments. Completion
of the first batch was not completion of the entire improvement program.

The owner has now directed execution through separate, economical PM and
Worker task threads. Two new PM tasks have been dispatched to own all remaining
packages. This file tracks Architect-level ownership. Each PM maintains the
individual worker assignments and acceptance evidence in its stream ledger.

## Assignment map

| Work | Accountable PM | Status at dispatch |
| --- | --- | --- |
| WP-01 artifact safety; WP-04 operating guidance | Engineering and release | Implemented and included in combined local acceptance |
| WP-02 search; WP-03 content visibility/footer | Experience and content | Implemented; regression preservation included in combined local acceptance |
| Translation cleanup | Engineering and release | Implemented; five exact-pair suites and i18n suite are included in combined local acceptance |
| WP-05 required browser/CSP diagnostics | Engineering and release | Implemented locally with narrow CSP handling, page-lifecycle isolation, bounded browser scheduling, and actionable diagnostics; dated failed browser records remain preserved beside the final combined 200/200 local run |
| WP-06 keyboard/search/motion/link-card behavior | Experience and content | Implemented and browser-regression covered |
| WP-07 claims and GPT availability | Experience and content | Owner decision packet complete; no unsupported fact was published |
| WP-08 public source publication route | Experience and content | Inventory and owner decision options complete; private/publication decision remains external |
| WP-09 sibling-sync maintenance safety | Engineering and release | Implemented and locally validated with synthetic fixtures; no sibling execution |
| WP-10 supported CI/supply chain | Engineering and release | Node 24 and bounded clean-install evidence integrated |
| WP-11 source/generated boundaries | Engineering and release | Implemented; generated/deployment boundaries are regression covered |
| WP-12 measured performance/capture readiness | Experience and content | Implemented with capture-safety coverage and a nav-only request-size improvement; not an LCP or field-performance claim |
| WP-13 human usability/assistive technology | Experience and content | Automated packet and browser coverage complete; human assistive-technology verification remains separate |
| WP-14 hosted governance/measurement | Engineering and release | Read-only evidence and concrete owner decision packet complete; no remote setting mutation |
| Ignored audit cruft and stale skill catalog | Engineering and release | Redundant catalog package removed with recovery evidence; saved-root ignored-file quarantine procedure remains for Architect integration |
| Final cross-stream acceptance and release decision | Architect | Combined candidate cleared local acceptance; no publication decision implied |

## Model and effort policy

| Role/task | Starting configuration | Escalation |
| --- | --- | --- |
| Architect | Existing architect model | Architecture, scope, tradeoffs, cross-stream acceptance |
| PM | GPT-5.6 Luna, medium reasoning | Only if actual planning/integration difficulty warrants it |
| Small, precise worker repair | GPT-5.4 mini, low reasoning | Medium for nontrivial behavior or test work |
| Security-sensitive state mutation or diagnosed mini failure | GPT-5.6 Luna, medium reasoning | Return the concrete issue to Architect before larger escalation |

Use short task-specific prompts and referenced artifacts instead of inherited
Architect history. Batch related small edits. Start with at most two active
workers per PM, use isolated worktrees and explicit file ownership, and avoid
repeated blind retries or redundant full-suite testing. Record actual worker
models and reasoning in the PM ledger. Model availability must be checked by
the task-creation tool; these assignments do not assert a dollar-cost estimate
or guarantee zero rework.

## Execution and completion contract

PMs must create worker tasks and continue through feasible local implementation,
validation, and integration. A written plan is not delivery. Each assignment
records its worker ID, model/effort, owned paths, baseline, acceptance checks,
result, and exact blocker where applicable.

Use distinct states: assigned, running, implemented, validated, owner decision,
human verification, integrated, and deployed. External decisions must be
supported by concrete reviewable options before requesting input. No fabricated
claims, private-source disclosure, external messages, new dependencies, sibling
changes, remote settings mutation, or publication follows from this delegation.
Local isolated commits and PM integration commits are authorized mechanisms.

Engineering owns validation/workflows/tooling. Experience owns public HTML,
shared browser/CSS, served assets, experience checks, and visual-capture tooling.
Shared-file ownership and generator passes must be coordinated. Architect owns
final common governance integration.

## Baseline correction

The saved checkout was clean at `f7888c0` on dispatch. The previous work is now
committed locally, superseding the older reports' uncommitted-state statements.
The last fetched remote was `1d969b6`; local and remote each had one unique
commit. This does not establish current hosted deployment. PMs must inspect
their isolated baseline and preserve both changes before integrating work.

## PM task references

| PM task | Thread ID | Worktree | Acceptance |
| --- | --- | --- | --- |
| AskJamie PM: Engineering and release | `01a074b4-bab5-7911-8513-a3bf52d3cb4a` | `/Users/okh/.codex/worktrees/ffd1/AskJamie` | Accepted all engineering packages; first two worker creations succeeded after schema correction |
| AskJamie PM: Experience and content | `01a074b5-0eae-7200-94ea-18204c90a896` | `/Users/okh/.codex/worktrees/7b0a/AskJamie` | Accepted all experience packages; two mini/medium worker creations succeeded after Architect correction |

PM ledgers: `assets/docs/delivery-engineering/pm-ledger.md` and
`assets/docs/delivery-experience/README.md` in the respective worktrees.

Both PMs initially placed `projectId` at the wrong level in worker-creation
arguments. The Architect identified this argument error, supplied the exact
valid shape, and required actual worker delegation instead of substituting
PM implementation or declaring a platform blocker. Engineering subsequently
dispatched WP-09 on Luna/medium and WP-05 on mini/low. Experience was directed
to dispatch mini/medium workers for browser acceptance and real performance
measurement, then the remaining WP-06 behaviors.

The Experience PM's initial local card-fix commit `108ab71` and decision
packets are provisional. They do not complete WP-06 or WP-12. The Architect
also supplied the existing bundled Playwright location, because absence of
worktree-local dependencies did not prove browser tooling was unavailable.
Worker validation and measured evidence remain required.

Experience confirmed successful queued creation of `AskJamie Worker: Cards
and browser acceptance` and `AskJamie Worker: Performance and capture
readiness`, both GPT-5.4 mini with medium reasoning. Across both PMs, four
initial worker tasks have been dispatched. Their completion is pending.

### Resolved worker registry

Verified against local task metadata and readable task state. The app's general
task list did not consistently expose child tasks; missing list entries did
not mean creation failed.

| Package | Worker thread ID | Actual model/effort |
| --- | --- | --- |
| WP-09 sync safety | `01a074b7-3cd4-78a1-9719-023baa5f8650` | GPT-5.6 Luna / medium |
| WP-05 required browser/CSP checks | `01a074b7-a97d-7330-91da-0d9acc5dd5d4` | GPT-5.4 mini / low |
| WP-10/WP-11 CI and inventory | `01a074bc-4ae3-71d2-987b-d188fb53d61a` | GPT-5.4 mini / low |
| WP-06 cards/browser acceptance | `01a074ba-0893-7de1-8360-804e7a8b55f3` | GPT-5.4 mini / medium |
| WP-12 performance/capture | `01a074ba-3a28-7bf0-9b2b-00393852549f` | GPT-5.4 mini / medium |

WP-09 correction `bebdc1e` closed the worktree-lock and preimage-test gaps and
is integrated in the Engineering stream. WP-05 later added narrow CSP handling,
resource diagnostics, and regression coverage. The historical engineering
browser result remains failed at 196/200 as dated evidence. Focused Experience
checks and capture evidence do not replace it. The final combined browser run
must be recorded independently at its exact candidate revision.

### Experience acceptance escalation

The Experience and Engineering PMs completed their bounded repair and
acceptance work in isolated worktrees. The final candidate retains their
separate histories, preserves the saved-local and remote histories, and keeps
publication authority with the Architect and owner.

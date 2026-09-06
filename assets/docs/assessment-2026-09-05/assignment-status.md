# Architect assignment status

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
| WP-01 artifact safety; WP-04 operating guidance | Engineering and release | Previously implemented and reviewed; current release verification assigned |
| WP-02 search; WP-03 content visibility/footer | Experience and content | Previously implemented and reviewed; regression preservation assigned |
| Translation cleanup | Engineering and release | Previously implemented, 60 tooling and 14 browser checks recorded; current release verification assigned |
| WP-05 required browser/CSP diagnostics | Engineering and release | Dispatched for implementation and validation |
| WP-06 keyboard/search/motion/link-card behavior | Experience and content | Dispatched for reproduction, bounded repairs, and validation |
| WP-07 claims and GPT availability | Experience and content | Dispatched; unsupported owner facts require concrete decision packet |
| WP-08 public source publication route | Experience and content | Dispatched for inventory and reviewable options; private material/publication requires owner decision |
| WP-09 sibling-sync maintenance safety | Engineering and release | Dispatched for local-tool repairs with synthetic fixtures, no sibling execution |
| WP-10 supported CI/supply chain | Engineering and release | Dispatched for current evidence and bounded compatibility work |
| WP-11 source/generated boundaries | Engineering and release | Dispatched; preserve recovery evidence and canonical source |
| WP-12 measured performance/capture readiness | Experience and content | Dispatched for measurement and justified local improvements |
| WP-13 human usability/assistive technology | Experience and content | Test packet and automated checks dispatched; human execution remains separate |
| WP-14 hosted governance/measurement | Engineering and release | Concrete settings/measurement decision packet dispatched; no remote setting mutation |
| Ignored audit cruft and stale skill catalog | Engineering and release | Scoped disposition assigned; verify duplicates and preserve useful work |
| Final cross-stream acceptance and release decision | Architect | Pending PM evidence and integrated validation |

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

WP-09 commit `c852738` was not accepted because review found worktree-lock
resolution and preimage-test gaps. Correction remains with the same worker.
The full engineering browser result remains failed at 196/200 pending
request-level diagnosis. Separate 15/15 experience checks and card geometry
passes do not replace that failed full run. Current accepted commits and
queued/running states remain the responsibility of the PM stream ledgers.

### Experience acceptance escalation

The Experience PM was moved from Luna/medium to Terra/medium in the same task
for its remaining acceptance work. Repeated incomplete handoffs included an
incorrect worker-creation blocker, an unavailable-browser assumption despite
bundled tooling, contradictory browser-validation prose, and performance
criteria left as a future-run packet. The purpose is to reduce repeated
Architect corrections. Existing small workers remain on mini; no duplicate
PM or implementation task was created. WP-12 remains partial until measured
evidence and justified optimization decisions satisfy its original criteria.

Engineering subsequently received the same PM-only escalation to Terra/medium.
Its integrated handoff still retained blanket inline-style CSP suppression,
omitted integrated pytest despite an available worker environment, and treated
authorized duplicate cleanup as a new approval dependency. The same workers
remain assigned, with medium reasoning requested for the remaining WP-05
diagnostics. This escalation changes acceptance supervision, not project scope
or publication authority.

The earlier in-process PM and two workers completed their bounded first-batch
and cleanup assignments; they are not being resumed at the Architect's model.

# Translation tooling cleanup decisions

Date: September 5, 2026. Scope: this AskJamie clone only. Existing website
assessment repairs remain uncommitted and are preserved.

## Decision

Keep the exact-pair translation prototype and its page-drift detector. Remove
duplicate weaker helper implementations, make the stronger tests discoverable,
and correct the detector's explicit adoption dead end. The `i18n` filename is
not evidence of an obsolete translation engine: its current implementation
routes missing/stale pages to the new exact-pair skills and never translates
pages itself.

The Architect separately owns browser locale behavior and main site guidance.
This PM/Worker package does not create translated pages, add a language pilot,
create a real site sync configuration/ledger, change external settings, modify
siblings, or publish the work.

## Ownership and approved actions

| Area | Owner | Decision |
| --- | --- | --- |
| Five exact-pair packages | Infrastructure Worker | Keep documented hyphenated planners/validators; migrate the full stronger suites into discoverable `test_*.py`; remove redundant underscore helpers and duplicate hyphenated test files after reference checks. |
| Detector adoption | Infrastructure Worker | Explicit adoption may refresh selected stale records after a reviewed translation update. Add fixture coverage for stale-to-current transition, route scoping, and no target writes. |
| Workflow | Project Manager | Preserve workflow filename, display name, job identity, pinned Actions and read-only permission. Add explicit standard-library regression execution and truthful configured/unconfigured summaries. |
| Skill discovery | Project Manager | Add a targeted manual translation map outside the generated catalog. Leave the unrelated catalog duplicate blocker untouched. |
| Runtime locale controls and main site docs | Project Architect | Handle separately and validate with browser/source checks. |

## What the consolidation preserves

All five directed pairs remain: `en-US -> de-DE`, `en-US -> en-UK`,
`en-US -> es-ES`, `en-US -> es-MX`, and `en-US -> fr-FR`, using their existing
package conventions. Their dictionaries, voice profiles, source contracts,
benchmarks, and evaluation history remain intact.

The newer documented helpers preserve more URL forms, email addresses,
relative links, and media targets, and reject identical source/target roots.
The older discoverable suites had eight cases each; the stronger suites had
ten cases each, with no old-only test methods. Direct execution passed all
five stronger suites, but normal unittest discovery skipped their hyphenated
filenames. Consolidation preserves the stronger coverage and points it at the
canonical helpers. A script pass still does not prove idiomatic translation,
source-voice quality, or publication readiness.

The exact source differences, original hashes, references, and file decisions
are recorded in [the Worker audit](translation-tooling-audit.md),
[duplicate comparison](duplicate-comparison.diff), and
[proposed file dispositions](proposed-file-dispositions.json). Dated benchmark
commands remain historical evidence; migration notes explain their renamed
test destinations rather than rewriting what supposedly ran in the past.

## Workflow behavior

The original workflow identity remains `i18n Page Sync`, with job name
`Check translated pages are present and current`. It now explicitly runs the
five discoverable helper suites and the detector suite using only Python's
standard library. Root-level pytest discovery does not establish coverage of
these hidden skill directories.

When `i18n/sync.config.json` is absent, helper tests still run and the detector
reports an intentional unconfigured no-op. The Actions summary says this is
not a translated-site readiness result. When the configuration file exists,
the detector validates it and limits checks to its declared route/locale scope.
Failure guidance distinguishes failed helper tests or configuration from real
missing/stale translations. No external workflow run was triggered locally.

## Catalog limitation

The separate read-only catalog check found 65 skills, while its generated
README block still lists 14 and omits translation tooling. Full regeneration
fails on the unrelated `okhp3-repl-repo-janitor copy` name mismatch/duplicate.
No translation package metadata failure was established. See
[catalog evidence](catalog-evidence.json). This cleanup neither deletes that
package nor hand-edits generated catalog content.

## Acceptance and remaining boundary

- Every retained translation suite is discoverable and tests canonical helpers.
- Detector fixtures prove explicit reviewed adoption resolves selected stale
  entries while leaving unrelated routes and translated file bytes untouched.
- The exact workflow regression loop executes successfully without added
  dependencies; its summary shell passes configured/unconfigured fixtures.
- Package and README references resolve, with historical references explicitly
  mapped rather than falsely presented as current filenames.
- Real site configuration remains absent; no translated page or ledger is
  generated by validation.
- All prior website changes remain intact. Publication and Git reconciliation
  are separate tasks; the remote CSS-only advance is not merged here.

Final executed counts and exact paths belong to the Worker audit and the PM
workflow-execution evidence. The initial execution records remain evidence of
the pre-consolidation state and are not relabeled as post-change results.

## Executed PM checks

| Check | Result | Evidence |
| --- | --- | --- |
| Exact workflow regression block | PASS, six suites of ten tests, 60 total | [Machine-readable result](workflow-regressions.json), [complete output](workflow-regressions.txt) |
| Workflow summary shell | PASS, syntax plus configuration-present and configuration-absent fixtures | [Summary validation](workflow-summary-validation.json) |
| Real site configuration boundary | PASS, configuration absent both before and after the exact test block | [Workflow result](workflow-regressions.json) |
| Full skill catalog | BLOCKED by unrelated duplicate package; no catalog output written | [Catalog evidence](catalog-evidence.json) |
| Hosted workflow execution | NOT RUN | Changes remain local and uncommitted; no Action was triggered |

These are mechanical implementation checks, not translation quality results.
The Architect's [cleanup summary](README.md) owns current browser/site checks,
Git state, and publication boundaries.

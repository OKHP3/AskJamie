# Translation tooling audit and bounded cleanup

Date: September 5, 2026. Scope: five repository-local translation packages,
the i18n detector, and the calling workflow. The local baseline was
`fd1ea19`; the Architect reported a later remote CSS-only commit with no
translation-tooling changes. This Worker did not fetch, merge, rebase,
commit, push, or alter sibling repositories.

The audit began read-only. The Architect subsequently approved consolidation
of the five duplicate implementations and a narrowly tested stale-baseline
adoption fix. Those changes are now implemented locally. All prior website
assessment edits remain preserved and uncommitted. The Project Manager owns
workflow clarification/test wiring and the tooling README map; they are
separate from the 30 Worker-owned changed paths recorded here.

## Conclusion

These packages are useful tools, not disposable locale remnants. The real
cleanup target was two competing implementations inside each translation
package. The newer, documented helpers had stronger protections, while the
normal test-discovery command exercised the older helpers. Consolidation
preserves the stronger implementations and makes their complete tests run
under normal Python discovery.

The i18n workflow is active but this site is unconfigured. Its successful
no-op says nothing about translation coverage or linguistic quality. A
separate detector defect prevented a reviewed stale translation from being
adopted again; that specific behavior is now repaired without translating or
changing any page.

## Provenance and reference trace

**CONFIRMED:** local Git history records these stages:

1. `f49dc53e46e7ff26d35d871e60e71b77d2c54b7e` added nested
   `language-mediation` translation packages and the i18n detector/workflow.
2. `2da89b2ec5e41e7f144f049fcd9857554ed5faa7` added flat translation packages
   with underscore-named helpers and tests. Historical reconciliation notes
   pointed to the additive histories; current Git inspection verifies them.
3. `4fc72fabf6b73c337ac57de8372434b2dc4cfc4d` flattened the nested packages,
   renamed their tools to hyphenated filenames, and added stronger checks.
   The older flat underscore implementations survived beside them.

The full Git output is retained in [git-history.txt](git-history.txt).
Every pre-cleanup file pair has hashes in
[duplicate-inventory.json](duplicate-inventory.json), and all nonidentical
content is preserved in [duplicate-comparison.diff](duplicate-comparison.diff).
There were **15 duplicate filename pairs and zero byte-identical pairs**.

The current entrypoints already name the hyphenated helpers:

| Package | Authoritative entrypoint references | Canonical helper targets |
| --- | --- | --- |
| `okhp3-translation-en-us-de-de` | `SKILL.md:115`, `SKILL.md:175` | `scripts/plan-en-us-to-de-de.py`, `scripts/validate-en-us-to-de-de.py` |
| `okhp3-translation-en-us-en-uk` | `SKILL.md:128`, `SKILL.md:193` | `scripts/plan-en-us-to-en-uk.py`, `scripts/validate-en-us-to-en-uk.py` |
| `okhp3-translation-en-us-es-es` | `SKILL.md:114`, `SKILL.md:174` | `scripts/plan-en-us-to-es-es.py`, `scripts/validate-en-us-to-es-es.py` |
| `okhp3-translation-en-us-es-mx` | `SKILL.md:119`, `SKILL.md:185` | `scripts/plan-en-us-to-es-mx.py`, `scripts/validate-en-us-to-es-mx.py` |
| `okhp3-translation-en-us-fr-fr` | `SKILL.md:114`, `SKILL.md:173` | `scripts/plan-en-us-to-fr-fr.py`, `scripts/validate-en-us-to-fr-fr.py` |

All paths in this table are relative to the package under `.agents/skills/`.
Each canonical planner loads its hyphenated validator by an explicit file
path at lines 14-19. The underscore-shaped name passed to
`spec_from_file_location` is a Python module identifier, not a dependency on
an underscore-named file. Deleting by text match alone would misread this
distinction.

Before cleanup, the underscore helper imports came from underscore planners
and the older underscore tests. No independent current caller was found
outside that legacy chain. French benchmark records refer to the former
hyphenated test path as historical evidence. Their bytes were preserved;
each package's SKILL entry now records the test-path migration explicitly.

## Dispositions

ACTIVE means a current declared or executable path. REFERENCE means retained
support or historical context. UNREFERENCED applies only after the caller
chain is removed. AMBIGUOUS means a broader claim cannot be established from
this repository alone.

| Surface | Baseline disposition | Final disposition and reason |
| --- | --- | --- |
| Five translation SKILL entrypoints and agent metadata | ACTIVE on-demand tooling | ACTIVE. Exact language-pair, review and voice contracts remain. |
| Ten hyphenated planner/validator files | ACTIVE | ACTIVE and byte-preserved. These were the documented, stronger implementations. |
| Ten underscore planner/validator files | REFERENCE legacy implementations, still executable through old tests | UNREFERENCED after test consolidation, then removed as authorized. No functionality unique to them was lost. |
| Five underscore test files | ACTIVE legacy discovery path | ACTIVE canonical discovery path, now containing all stronger tests and invoking the hyphenated helpers. |
| Five hyphenated test files | ACTIVE when run directly; absent from standard discovery | UNREFERENCED executable copies after consolidation, then removed. Their full content now lives in the underscore test files. Historical paths are documented. |
| Dictionaries, voice profiles and example project manifests | REFERENCE reusable translation controls | REFERENCE, unchanged. Example roots such as `content/en` and `content/fr` are not evidence of configured website locale routes. |
| Benchmark, learning-ledger and historical-review records | REFERENCE | REFERENCE, unchanged. They do not certify current translation quality or active automation. |
| `.github/workflows/i18n-page-sync.yml` | ACTIVE workflow calling the detector's read-only check | ACTIVE. Root site configuration is absent, so route checking returns a truthful unconfigured no-op. PM owns its updates. |
| `okhp3-i18n-page-sync/scripts/i18n-page-sync.py` | ACTIVE reusable detector with a confirmed stale-adopt defect | ACTIVE with selected stale adoption repaired; no real site configuration or ledger was created. |
| Future deployment of translated pages | AMBIGUOUS in this tooling scope | AMBIGUOUS. Package installation and test success do not authorize or prove a locale rollout. |

## Preserved implementation differences

For all five language pairs, the newer validator adds protected email
addresses, relative Markdown/media targets, HTML `href`/`src`/`action`
targets, and non-HTTP schemes such as `mailto` and `tel`. The baseline older
validator's URL recognizer only covered HTTP(S). Compare, for example,
`okhp3-translation-en-us-fr-fr/scripts/validate-en-us-to-fr-fr.py:21` and
`:212` with the saved old-file diff.

The newer planner rejects identical resolved source and target roots at
`scripts/plan-en-us-to-fr-fr.py:44`. All five variants preserve this guard.
The German, British English, Spain Spanish and Mexican Spanish test fixtures
also correct copied French target-root strings to the intended pair roots.

Every newer suite contains all eight former test methods plus:

- `test_relative_links_email_and_media_targets_are_protected`
- `test_planner_rejects_identical_source_and_target_roots`

There are no old-only test methods. An AST method inventory and the exact
keep/remove/consolidate path list are retained in
[proposed-file-dispositions.json](proposed-file-dispositions.json).

## Baseline test-discovery defect

**CONFIRMED on the installed Python 3.14 runtime:** each hyphenated test
file passes 10 tests when run directly. Discovery with `-p 'test_*.py'`
finds only the older eight-test file. Discovery with `-p 'test-*.py'` finds
zero tests and exits 5. The conclusion is the missing coverage; the exact
zero-test exit behavior should not be generalized to older Python versions.

After consolidation, this command runs all 10 tests from each package:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Before/after commands, exit codes and counts are preserved in
[tool-execution-results.json](tool-execution-results.json) and
[final-tool-execution-results.json](final-tool-execution-results.json).
Test output is retained beside those files. Tests ran with bytecode disabled
and temporary fixtures confined to this audit directory. No dependency was
installed and no actual source/target translation project was created.

## Detector behavior and correction

The workflow calls the actual CLI spelling `--mode check`.
`scripts/i18n-page-sync.py:43` names `i18n/sync.config.json` as its default
configuration. The check run against AskJamie returned
`{"configured": false}` and exit 0; see
[i18n-site-check.txt](i18n-site-check.txt). This is not an obsolete-workflow
finding. It is an intentional dormant site configuration with active tooling.

**CONFIRMED defect at baseline:** `adopt()` iterated only
`results["needs_baseline"]`. After initial adoption, a source edit correctly
made the route stale. Updating its target and explicitly adopting the route
again adopted zero records and left it stale, contrary to the documented
update procedure. The isolated reproduction is in
[i18n-stale-adopt-fixture.json](i18n-stale-adopt-fixture.json).

The authorized repair includes selected stale records in the adoption loop.
It still uses the existing route filtering, requires an existing target, and
only writes the ledger. The caller remains responsible for confirming that
the target has actually been reviewed; hashing does not establish linguistic
quality. The post-repair reproduction shows one adopted record, zero stale
records, and unchanged target bytes in
[i18n-stale-adopt-fixture-after.json](i18n-stale-adopt-fixture-after.json).

Two new detector tests cover the complete source-change/update/adopt journey,
preservation of an unselected stale route, read-only check behavior, exact
source/target byte preservation during adoption, and refusal to invent a
missing target. CLI spellings and behavioral-test counts were corrected in
current detector instructions. Dated translation benchmarks were not rewritten.

## Applied scope, validation and recovery

The smallest approved cleanup was carried out as one dependent package:

1. Preserve the 10 stronger canonical helper files without changing bytes.
2. Replace five older discoverable suites with the stronger suite content.
3. Remove 10 weaker helpers and five now-redundant test implementations.
4. Add current discovery commands and historical path mappings to the five
   package entrypoints.
5. Correct selected stale adoption and add the two focused detector tests.

The exact 30 changed Worker-owned paths and their actions are in
[applied-tooling-changes.json](applied-tooling-changes.json). The detector
workflow, root/shared assets and the generated skills catalog were not
edited by this Worker. The PM's catalog-blocker observation is separate;
this cleanup does not repair or remove the unrelated duplicate janitor skill.

| Check | Result | Evidence boundary |
| --- | --- | --- |
| Five canonical translation suites | PASS, 10 tests each | 50 deterministic helper tests; not linguistic quality evidence. |
| Detector suite | PASS, 10 tests | Eight retained tests and two new adoption/preservation tests. |
| Canonical planner/validator preservation | PASS, 10 exact hashes | Compared with pre-cleanup inventory. |
| Old test-method preservation | PASS | No old-only methods; stronger cases retained for every pair. |
| Scoped whitespace | PASS | `git diff --check` against the five packages and detector. |
| Real site configuration and ledger | ABSENT | No `i18n/sync.config.json` or `i18n/sync-state.json` was created. |
| Linguistic/native review | NOT RUN | No translation was produced or approved. |
| Publication | NOT RUN | No Git or hosted-state mutation occurred. |

Recovery is exact-path and reviewable: retrieve the removed files from the
recorded baseline commit into an inspection directory, compare their hashes
against `duplicate-inventory.json`, and reverse only the listed cleanup
changes if needed. Do not reset the worktree, discard prior assessment
changes, restore an entire package over concurrent edits, or regenerate the
skills catalog to recover these files. The saved complete diffs and current
Git objects preserve the former implementations without keeping two active
copies in each package.

No remaining input is required for this bounded local cleanup. Decisions
about enabling site locales, publishing translations, or synchronizing these
packages with their upstream source family remain outside this Worker scope.

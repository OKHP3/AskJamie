# Validation and activation evidence

Checked September 18, 2026, America/Chicago, against the working tree based
on `8decfb8679c76818b2a27c68c5dc43b1719ab112`.

## Local checks

| Check | Result | Evidence / limit |
| --- | --- | --- |
| New technology-audit regression tests | PASS | 16 tests: version ordering, prerelease/yanked rejection, year-based Python releases, gzip publisher response, SHA/tag resolution, future upgrades, stale locks, CI input bypass, runtime module drift, incomplete lookup behavior, transitive handling, and complete lockfile enumeration |
| Offline technology contract | PASS | Exact root dependency/lock agreement, Node engine agreement, Python requirements consumed by CI, and Node/Python configuration agreement with Replit |
| Online technology audit | PASS | Exit 0; all queried stable package/runtime/action release lookups completed; report and JSON retained here |
| Scheduled audit policy | EXPECTED UPDATE STATE | The same successful snapshot contains outdated direct packages, actions, and runtimes. `--fail-on-outdated` classifies this as exit 1, not as lookup failure |
| Dependabot configuration schema | PASS | Checked using the published Dependabot 2.0 JSON schema and the locally available schema validator; no dependency added |
| Workflow YAML and project TOML parsing | PASS | Every workflow and the Dependabot file parsed; existing project TOML parsed |
| Site structure | PASS | 28 HTML pages clean |
| Shared asset fingerprints | PASS | 37 pages/templates, zero stale |
| Search freshness | PASS | 26 content routes current |
| Link checker | PASS | 28 pages, 834 internal and 554 external references, zero reported broken links/style issues; this does not claim live reachability of every external destination |
| Responsive source checks | PASS | 208/208 static route/viewport checks; not rendered browser coverage |
| Canonical site audit | PASS | Zero issues |
| Full Python regression suite | FAIL / ENVIRONMENT LIMITS | With `PYTHONUTF8=1`, 85 passed, 8 failed, and 12 subtests passed. This broad run preceded the final added runtime-drift test; all 16 final audit tests passed separately |
| Whitespace/error check | PASS | `git diff --check` |

The eight remaining full-suite failures are in unchanged existing tests:
three symbolic-link fixtures fail with Windows error 1314 (missing privilege),
and five post-merge shell tests invoke an unavailable WSL Bash service. The
earlier run without `PYTHONUTF8=1` also had three child-process encoding
failures; enabling UTF-8 cleared those. No tests were weakened or skipped to
report a passing result, and no workstation privileges or WSL configuration
were changed.

No complete Linux CI run was executed for these uncommitted files. Full
rendered browser QA, candidate package upgrades, live Pages verification,
and Replit execution are NOT RUN for this change. No public HTML/CSS/JS or
vendored runtime was modified, so a visual baseline replacement is not part
of this work.

## Scope and remaining work

Prepared: a source-backed technology inventory; an executable read-only
release auditor; weekly Dependabot proposals for npm, pip, and Actions; a
scheduled audit workflow; a current-version-neutral offline CI gate; exact
pytest QA input; CI consumption of pinned Python requirements; and the
upgrade/rollback policy. `npm run check:stack` now uses the new gate instead
of the inherited fixed-version checker.

The GitHub schedules are NOT ACTIVE from these local files alone. No commit,
push, merge, repository setting change, or deployment was performed. To
activate, merge through a reviewed PR and verify the first Dependabot and
Technology Version Audit runs as described in the
[update policy](../../../docs/technology-update-policy.md).

Current runtime/package upgrade candidates remain review work. In particular,
Mermaid 12 needs a complete vendor replacement and visual/security review;
Node and Python changes need aligned CI/Replit configuration and actual
host verification. The report does not claim those upgrades are complete.

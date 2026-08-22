# Release evaluation record schema

Use this compact schema when recording a release-procedure evaluation. The
record must identify the evaluated skill version and whether the evidence is
`live`, `analytical`, `historical`, or `not-run`.

```yaml
skill_name: <name>
skill_version: <version>
evaluation_kind: <structural | live-client | cross-client>
evaluation_date: <YYYY-MM-DD>
status: passed | failed | blocked | not-run
evidence_mode: live | analytical | historical | not-run
client: <client or runner>
runner: <executor>
source_set:
  - <package file or repository input>
checks:
  <check_name>:
    result: passed | failed | not-run
    evidence: <command, output, count, or path>
limitations:
  - <capability or independence limitation>
authorization:
  writes: none | <explicitly authorized writes>
  external_mutations: none | <description>
```

For a release summary, retain separate results for local checks, browser or
static QA, artifact preparation, CI, and hosted verification. A mixed result
must not be collapsed into `passed`. Missing client, browser, CI, network, or
authorization capabilities are recorded as `not-run` or `blocked` according to
the procedure's failure table.
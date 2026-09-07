# Release-candidate evidence, 2026-09-05

This directory preserves compact, machine-readable evidence from the isolated
release candidate. It is local acceptance evidence only. It does not establish
a hosted deployment, field performance, or publication.

## Responsive QA

`responsive-qa/` retains the JSON reports from each full 25-route, eight-
viewport browser run. Failed records are deliberately retained beside the final
200-of-200 report. The command for the final run was:

```bash
python3 -m http.server 5204 --bind 127.0.0.1
/Users/okh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node scripts/responsive-qa.mjs --base=http://127.0.0.1:5204
```

The preview command is the standard Python CLI, which uses a threaded server in
this Python 3.14.5 runtime. The four-page browser scheduling limit is a
measured harness choice. It reduced browser request bursts during the local
test. It is not evidence that a single-threaded CI server caused every prior
failure.

Focused lifecycle and capacity regression execution was reported in the
terminal only, so no separately recoverable log file existed to copy. The
executable regression source is `tests/test_release_checks.py`; the final root
pytest result is recorded in the combined acceptance report. This boundary is
intentional rather than a reconstructed test transcript.

## Lighthouse

`lighthouse/sample-*-summary.json` are the three original desktop lab summaries.
`lighthouse/summary.json` is their computed median rollup. The raw Lighthouse
reports remain temporary local evidence under
`/tmp/askjamie-release-evidence-2026-09-05/`; they were not copied because this
directory preserves the compact record and settings needed for review.

## Artifact

`pages-artifact-manifest.json` is the regenerated manifest for the 313-file
release artifact. The artifact was prepared with:

```bash
python3 scripts/prepare-pages-artifact.py --output .scratch/release-candidate-pages
```

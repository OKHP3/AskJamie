# Cross-client portability evaluation

## Decision

```yaml
status: blocked
skill_name: okhp3-static-site-release
skill_version: "1.0.0"
evaluation_kind: cross-client
evaluation_date: "2026-08-21"
evidence_mode: analytical
```

The requested second-AI-client benchmark could not be executed. No Claude
Project, ChatGPT Project/Custom GPT, GitHub Copilot workspace, or isolated
cross-client executor was available in this environment. This report therefore
does not claim cross-client portability or an unseen-holdout pass.

## Independence record

| Role | Client / runner | Source set | Permissions | Result |
|---|---|---|---|---|
| Package evaluator | Replit Agent / workspace shell | Repository root and `okhp3-static-site-release` package | Filesystem and shell; no secrets or external mutations | Analytical, not independent |
| External client | Claude, ChatGPT, or GitHub Copilot | Not available | Not available | Not-run |

The package evaluator had access to repository context and cannot serve as an
independent client. The prior benchmark record is retained as historical
Replit-only evidence and is not reused as cross-client evidence.

## Isolated package run

To approximate the portable filesystem contract without contaminating the
working tree, the repository was copied to a disposable directory and the
procedure was run from that copy. Only the package, repository files, and
declared Python/Node runtimes were used. No task history, agent memory, or
credentials were supplied to the procedure.

| Stage | Command / evidence | Result |
|---|---|---|
| Preflight | Python 3.11.14; Node v20.20.0; Playwright package 1.60.0; clean disposable-copy status | passed |
| HTML/site validation | `python3 scripts/validate-site.py` — 26 pages clean | passed |
| Link checker | `python3 scripts/check-links.py` — 711 internal links, 0 broken | passed |
| Regression suite | `python3 -m pytest` — 9 passed | passed |
| Generated freshness | `python3 scripts/build-search-index.py --check` — 24 pages current | passed |
| Full audit | `python3 scripts/audit-site.py --quiet` — 0 issues | passed |
| Browser QA | Browser capability was not usable for this run | not-run |
| Static QA fallback | `node scripts/responsive-qa.mjs --static` — 208/208 checks | passed, limited |
| Public artifact | `python3 scripts/prepare-pages-artifact.py --output <disposable-dir>` — 205 files; SHA-256 `5cba83e4a2e995a7a8344a415cb914d42ae2b750ceb67660aff2f5a356588e0f` | passed |
| Artifact boundary | No `.github`, `scripts`, `tests`, `.local`, `.agents`, or configuration files in the artifact | passed |
| CI verification | No live Actions run supplied | not-run |
| Hosted verification | No authorized hosted verification performed | not-run |

The static fallback explicitly does not prove runtime overflow, console
errors, or runtime image failures. The artifact was prepared only; it was not
uploaded or published.

## Output-contract evaluation

The isolated run produced the required release fields: status, repository,
per-check classifications, evidence, artifact path/digest, hosted
verification state, writes/mutation boundary, and limitations. It therefore
supports the skill's **local output-contract integrity**, but not its
cross-client equivalence.

| Expectation | Result | Evidence |
|---|---|---|
| Explicit deterministic commands | passed | Commands and results above |
| Capability-aware browser fallback | passed | Static QA marked limited; browser marked not-run |
| Disposable artifact inspection | passed | 205-file artifact and boundary inspection |
| Separate CI and hosted results | passed | Both marked not-run |
| No publication or credential access | passed | No external mutation; no secret access |
| Independent second-client execution | blocked | No external client or executor available |
| Unseen protected holdout | not-run | `evals/evals.json` declares external-required holdout |

## Package correction

The skill referenced `references/grading-schema.md`, but that file was absent
from the package. A compact schema was added so another client can resolve the
reference and produce a consistent evidence record without relying on
repository-specific knowledge.

## Limitations and next authorized action

- This evaluation is analytical and Replit-only; it must not be described as
  proof of portability.
- The exposed holdout in `evals/evals.json` remains seen and cannot support an
  unseen-holdout claim.
- CI and hosted Pages checks remain outside this run.
- Next authorized action: provide a Claude, ChatGPT, or GitHub Copilot session
  (or isolated executor), attach only the package and repository, run the
  frozen holdout, and append the client-specific result without changing the
  holdout first.
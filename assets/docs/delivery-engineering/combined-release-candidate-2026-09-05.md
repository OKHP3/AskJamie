# Combined release candidate acceptance

Status: **BLOCKED**. Candidate runtime source revision: `912fdf9`.
Candidate branch: `codex/release-candidate-20260905`. This isolated candidate
preserves the saved local `f7888c0` history, `origin/main` commit `1d969b6`,
the Engineering stream through `fc43810`, and the frozen Experience stream
`d79db410`. No saved-main, remote, deployment, Pages, DNS, analytics, or
repository-settings mutation occurred.

## Reconciliation and generated surfaces

The local/remote merge is `8fab39a`. It had 36 conflicts. After normalizing
only cache-fingerprint query values, all 36 sides were identical. The
source-bearing side was retained and shared asset, CSP, and search generators
were run once after the Experience merge. Their check modes are current.

The current Architect assignment-status document from the saved root was
copied into this candidate and revised for completed, owner-decision, human,
and unresolved states. Historical assessment and browser documents remain
dated records.

## Deterministic acceptance

All commands ran in this worktree with
`/tmp/askjamie-venv/bin/python3` (Python 3.14.5, pytest 9.1.1) and the
bundled Node 24.19 runtime. The declared Node dependencies were installed with
`npm ci --no-audit --no-fund --prefer-offline`; Playwright Chromium revision
1223 was installed because the bundled browser cache had a different revision.

| Check | Result |
| --- | --- |
| Root Python regression suite | PASS, 63 tests plus 12 subtests |
| i18n and five exact-pair suites | PASS, 60 tests |
| Structural validator | PASS, 27 pages |
| Link checker | PASS, 764 internal and 534 external links, 0 broken |
| Cache, CSP, and search freshness | PASS, 36 shared references, 27 CSP pages, 25 indexed pages |
| Canonical audit | PASS, 0 issues |
| Experience browser checks | PASS, 18 of 18 |
| Capture-safety tests | PASS, 4 of 4 |
| JavaScript smoke | PASS |
| Pages artifact | PASS, 313 public files, SHA-256 `829e111b066f558f48e60a4fea6798bd3ff8f6bd28bec3ecec37299bb555cfba` |

The artifact is at `.scratch/release-candidate-pages/` with manifest
`.scratch/release-candidate-pages.manifest.json`. Its top-level directories
are public routes, `assets`, and `.well-known`; it contains no `.github`,
`scripts`, `tests`, `.agents`, or `.scratch` content.

## Browser result and blocker

The one final full responsive run against `http://127.0.0.1:5200` at source
revision `912fdf9` ran all 200 route/viewport rows and failed 11 rows. Each
failure was a local-image `net::ERR_ABORTED` event, concentrated on the BFS
Framing, LEGO, Starbucks, and Brooks Running BrandGuard routes. The disposable
runner output is retained at
`/tmp/askjamie-release-evidence-2026-09-05/responsive-qa/`.

The historical 196/200 run remains separately preserved. A focused candidate
probe of the affected routes at mobile 390 and desktop 1280 returned local 200
responses for HTML, CSS, JavaScript, avatars, and case-study images; eager
images completed with nonzero natural widths. The worker did not reproduce a
navigation-attribution race or prove that the 11-row run is a harness defect.
Therefore this candidate does not treat the focused result as a clearance. The
release decision remains blocked pending a reproducible cause or an owner and
Architect decision on the failed full-run evidence.

## WP-12 local lab evidence

The combined capture harness passed 8 route/viewport captures: homepage, Lens
hub, BrandGuard detail, and Universe at 1280x900 and 390x844. Conditions were
one fresh browser context per sample, device scale factor 1, light scheme,
no-preference motion, no throttling, and same-origin requests only. Capture
request bytes, readiness waits, image sizes, and resource samples are in
`/tmp/askjamie-release-candidate-captures/capture-readiness.json`.

Three sequential Lighthouse desktop samples covered homepage, BrandGuard,
Universe, and search. Median lab values were:

| Route | Performance | LCP ms | CLS | TBT ms |
| --- | ---: | ---: | ---: | ---: |
| Homepage | 100 | 721 | 0.004232 | 0 |
| BrandGuard | 100 | 741 | 0.017077 | 0 |
| Universe | 100 | 602 | 0.004840 | 0 |
| Search | 100 | 721 | 0.021322 | 0 |

Raw reports are retained in
`/tmp/askjamie-release-evidence-2026-09-05/`. These are local desktop lab
samples. They do not establish field performance, real-user LCP, or a general
production performance claim. The nav-only 80px avatar change reduced the
sampled local request by 748,775 bytes, but is not represented as an LCP claim.

## Remaining owner and human decisions

- WP-07 GPT availability and WP-08 public-source publication retain their
  Experience decision packets. No unsupported claim or publication was made.
- WP-13 needs human VoiceOver/NVDA or comparable assistive-technology testing.
- WP-14 has a ruleset and hosting-header decision packet. No external settings
  were changed.
- Saved-root ignored `.DS_Store` cleanup remains outside this worktree. The
  exact manifest and recoverable-quarantine procedure is in the Engineering
  cleanup record.


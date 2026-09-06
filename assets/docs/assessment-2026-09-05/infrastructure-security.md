# AskJamie infrastructure and security assessment

Assessment date: September 5, 2026. Worker scope: local release tooling,
security boundaries, browser policy, dependencies, and QA implementation.
Baseline source: `fd1ea19`, following the Architect's fast-forward from
`04cc3e7`. Branch, remote, hosted-response, and baseline execution evidence
belong to the Architect's assessment. This report distinguishes inspected
source behavior from a tested hosted outcome.

The static architecture fits this portfolio site. The most consequential
problems are release-tool safety, the difference between tested source and
published artifacts, and checks that claim more than they establish. A
framework or backend migration would not resolve these problems.

## What already works

- **CONFIRMED:** `.github/workflows/validate.yml:99` deploys only after the
  validation job succeeds. The deploy job has scoped Pages/OIDC permissions,
  uses the GitHub Pages environment, and downloads a commit-named artifact.
- **CONFIRMED:** the source separates browser code from maintenance tools,
  vendors Mermaid locally, commits an npm lockfile, and checks generated
  asset fingerprints and search-index freshness in CI. A scheduled hosted
  smoke workflow exists in addition to local browser checks.
- **CONFIRMED:** `assets/js/app.js:669` escapes search display text before
  inserting markup. Search is local JSON, with no search backend. This is
  useful protection, not a complete proof against every DOM injection path.
- **CONFIRMED:** `scripts/csp.py:92` generates policies from inline content,
  disables script attributes, and scopes the Mermaid inline-style allowance
  to diagram classes. `assets/js/mermaid-init.js:268` defaults to strict
  Mermaid security unless a page explicitly opts into clickable behavior.
- **CONFIRMED:** the deployment allowlist excludes top-level tooling,
  documentation, skills, tests, and repository metadata. It is a meaningful
  boundary even though individual content directories remain broad.

## Findings and recommended acceptance tests

Priority P1 means address before relying on the affected operation. P2 means
the next maintenance batch. P3 means a useful follow-up. These are project
priorities, not CVSS vulnerability ratings.

| ID | Priority and tier | Claim and evidence | Practical impact and consequence if false | Recommendation and next check |
| --- | --- | --- | --- | --- |
| INF-01 | P1 CONFIRMED, locally remediated | Baseline `scripts/prepare-pages-artifact.py:69` deleted any existing `--output` directory with `shutil.rmtree`, before verifying ownership. Current safety guard is at line 86. | A mistaken output argument could remove source or unrelated owner work. If the source reading were wrong, the proposed guard would be unnecessary restriction. | Reject repository/ancestor/source targets, symlinks, and nonmatching existing outputs before deletion. The 15 new fixture tests exercise preservation and repeatability. |
| INF-02 | P1 CONFIRMED, partially remediated | Baseline `is_public` accepted every file below permitted directories. Candidate artifact contained three `.DS_Store` files, two `.gitkeep` files, and two `.pdn` editable originals. `copy2` followed file symlinks. Current exclusions are at `scripts/prepare-pages-artifact.py:48`. | Accidental publication and unnecessary artifact bulk. No secret disclosure or hosted publication of these files was established by this Worker. If the inventory were wrong, the byte savings would be overstated. | Hidden files, symlinks and PDN files are now excluded from packaging while source originals remain. A future batch should define permitted file types or a reviewed publication manifest; an ordinary `about/private-notes.md` still passes the directory boundary. |
| INF-03 | P1 CONFIRMED | `scripts/sync-foundation-files.py:149` renames any existing index lock; line 257 chooses the newest timestamp group; line 342 writes without dirty-file/preimage checks and ignores hook return codes. Its safe default is dry-run. | The explicit apply/commit modes can overwrite useful changes or interfere with active Git work. There is no evidence that this happened during this assessment. If the code path is never used, current exposure is dormant. | Keep dry-run available. Replace mutation with reviewed plans, exact preimage checks, dirty-tree refusal, checked hook results and backups. Never infer stale lock ownership from existence. Use synthetic repositories to test two divergent dirty copies and an active lock. No sibling execution is needed for development tests. |
| INF-04 | P2 CONFIRMED source, hosted effect UNKNOWN | `_headers:1` is a host-specific configuration document, while Pages workflow deployment is explicit. `scripts/csp.py:181` generates an edge policy permitting only self-hosted fonts/styles despite page policies allowing Google Fonts. | Treating a repository file as proof of delivered headers overstates security. Activating that edge policy as written would block declared external fonts. If a separate edge already supplies compatible headers, only documentation may need repair. | Record actual response headers separately. Test any proposed header plus meta policy together against fonts, Mermaid, analytics, and embeds. Meta CSP cannot enforce frame-ancestors, per [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors). Do not change hosting just to improve a score. |
| INF-05 | P2 CONFIRMED | `scripts/generate-csp.py:24` checks policy JSON; `_headers` is only touched in write mode. Lines 51-53 silently skip missing CSP tags. `validate-site.py:535` checks generated class intent rather than comparing the full served policy. `validate.yml` does not invoke the full CSP check. | The standalone check's verified-page count does not prove every page has the expected policy. Other audit/privacy tests catch absence, so this is overlapping-check incompleteness, not proof that current pages lack CSP. | Make missing and duplicate policies fail; compare edge output when it is retained; wire a nonwriting canonical check into CI. Mutate fixture policy removal, directive weakening and edge drift independently and require failure. |
| INF-06 | P2 CONFIRMED | `scripts/responsive-qa.mjs:82` and line 92 return to static mode on missing package/browser. Lines 197-199 remove all inline-style CSP console errors; line 173 skips lazy images; line 130 checks only 404 CSS/JS/JSON URLs and misses fingerprinted suffixes and `.mjs`. | A responsive result can underreport real rendering failures. The separate smoke suite fails if Chromium cannot launch, reducing the CI fallback risk, but it exercises only selected routes. If every untested path is healthy, these are coverage gaps rather than current defects. | Add a required-browser mode; retain CSP events as explicit diagnostics; scroll lazy content; record page errors, request failures and all failed local asset responses using parsed URL paths. Test deliberately broken lazy images, query-versioned assets, module imports and dynamic styles. |
| INF-07 | P2 CONFIRMED | `.github/workflows/validate.yml:30` and `hosted-js-smoke.yml:29` select Node 20; current [Node release documentation](https://nodejs.org/en/about/previous-releases) lists it EOL and Node 24 as LTS. Actions use mixed SHA/tag pinning; line 35 installs unpinned Python packages. No Dependabot config exists in `.github`. | Maintenance and supply-chain exposure in development/CI, not a server-side production runtime. No exploitable package vulnerability is asserted. If private automation provides dependency updates, the automation gap is smaller. | Move development jobs to a supported LTS after lockfile/browser validation, pin Action SHAs consistently, and record reproducible Python dependencies. Schedule dependency review. GitHub recommends full commit SHA pinning in its [secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use). |
| INF-08 | P2 CONFIRMED behavior, privacy conclusion UNKNOWN | `legal/index.html:95` eagerly loads GA4 and line 248 discloses unconditional measurement. `tests/test_privacy_consent.py:20` deliberately enforces this behavior. `app.js:980` places search text in the query string and history. | The privacy test name could be mistaken for consent verification. URL/search data may enter measurement depending on GA4 configuration. No account configuration, consent requirement, or unlawful behavior was established. If measurement excludes search queries already, only evidence/docs may be needed. | Rename the test for its actual contract; document the owner-approved measurement model. Inspect page-location/search redaction, history events, retention, and stream settings before claiming data minimization. Use synthetic query values, not personal data. Google documents URL/query redaction in [GA4 Data redaction](https://support.google.com/analytics/answer/13544947). |
| INF-09 | P2 CONFIRMED | `scripts/check-links.py:70` counts/skips HTTP links and checks internal targets against the source filesystem. `check-public-gpt-links.py:56` treats any final 2xx/3xx as reachable, and 403 as authentication/private. | A green internal-link report does not establish external availability, correct destination content, GPT usability, or artifact link closure. A bot challenge can be classified as private. If human destination checks already exist, carry their separate evidence. | Keep local link validation deterministic. Label HTTP probes narrowly, distinguish challenge/unknown states, and add bounded human/signed-out checks for primary journeys. Validate internal URLs against the actual packaged artifact. |
| INF-10 | P2 CONFIRMED, scratch gap locally remediated | Source inventories differ: `validate-site.py:36`, `audit-site.py:84`, `build-search-index.py:32`, `csp.py:81`, and the packaging allowlist use different exclusions. At inspection, `.scratch` was not excluded by several source scans. | Generated duplicates can contaminate later local checks/search, while files that exist in source but are omitted from publication can pass link validation. If the Architect repairs those inventories in this batch, this finding becomes locally remediated. | Reconcile the public-page collector or add invariant tests across all collectors. Place a fixture page in tooling/scratch and a valid new content route in source; require the correct disposition in sitemap, index, validators and artifact. |
| INF-11 | P2 CONFIRMED | Tracked `dist-pages/` and `dist-pages.manifest.json` coexist with source. Read-only verification found the committed manifest does not match its directory bytes. Workflow tests source before preparing output. | Multiple apparent release snapshots create ambiguity. The safety guard now refuses overwriting this stale output. This does not establish a broken hosted release. | Preserve the current snapshot until owner-reviewed cleanup. CI now prepares fresh `.scratch/pages-release`, keeping the deploy runner's clean `dist-pages` download location. Follow up with an explicit generated-artifact tracking policy and test the artifact itself before publication. |
| INF-12 | P2 CONFIRMED configuration, locally remediated; runtime cause INFERRED | The intermediate `actions/upload-artifact@v4` step omitted `include-hidden-files` at baseline. The [Action's documentation](https://github.com/actions/upload-artifact) says hidden files/directories are excluded by default. `.well-known` is intentionally part of the builder output. | The intermediate artifact can lose security-contact and verification files even when the local builder includes them. If the resolved Action behavior differs, confirm by downloading a run artifact. | Enable hidden-file transport only for the newly filtered artifact. Test the downloaded artifact contains `.well-known/security.txt` and `.well-known/discord`, with no other hidden content; verify those hosted responses after an authorized deployment. |

## Approved local remediation and evidence

The Architect authorized the smallest initial packaging repair through the
Project Manager. Changes cover the builder, a dedicated regression
test file, its CI prepare/upload integration, and narrow scratch-directory
exclusions in source inventories and their existing regression collectors. No public source asset,
content page, shared browser file, dependency, external setting, or sibling
repository was changed by this Worker.

- `scripts/prepare-pages-artifact.py` now validates output before deletion.
  Existing outputs must match their complete manifest digest. New disposable
  external outputs and repository `.scratch` outputs are supported. Existing
  source directories, unrelated outputs, and changed artifacts are preserved.
- Hidden content, symlinks and editable `.pdn` artwork are excluded. Intentional
  root files and top-level `.well-known` content remain eligible. This is not
  a general secret scanner or an exact per-file allowlist.
- `tests/test_pages_artifact_safety.py` uses standard-library unittest and is
  also discoverable by pytest. It covers destructive target refusal,
  preservation of existing work, hidden/source asset exclusions, symlink
  rejection including linked ancestors, preservation of `.scratch` itself,
  manifest conflicts, identical repeated builds, source inventory exclusions,
  and filtered artifact transport.
- `.github/workflows/validate.yml:85` prepares and uploads a fresh artifact at
  `.scratch/pages-release`. The artifact name and isolated deployment download
  location remain the same. Hidden-file transport is enabled only on this
  filtered artifact, preserving the intentional `.well-known` directory.
- `.scratch` is explicitly excluded by `scripts/validate-site.py`,
  `scripts/audit-site.py`, `scripts/build-search-index.py`,
  `scripts/check-links.py`, and `scripts/csp.py`, and by the public-page
  collectors in `tests/test_privacy_consent.py` and
  `tests/test_external_font_origins.py`. Tests exercise nested generated HTML,
  tracked scratch entries, and a broken generated-only link. These changes
  do not suppress other hidden directories beyond existing policies.

| Validation | Status | Evidence and limit |
| --- | --- | --- |
| 15 focused safety regressions | PASS | `python3 -B -m unittest tests.test_pages_artifact_safety -v`; 15 tests passed. No dangerous command was run against the real repository or an ancestor. |
| Real filtered artifact generation | PASS | 312 files, 114,579,259 bytes at `.scratch/pages-release`; no unexpected hidden paths, no PDN files. |
| Repeatability | PASS | Two consecutive builds returned SHA-256 `ce79ce91eca2c80808fcb896c36919c93ec2b2c2278067867e839ce914eb0fb9`. This captures the content present at Worker build time. |
| Source artwork preservation | PASS | Both original PDN source files remain. Their combined 15,472,891 bytes are omitted only from packaging. |
| Owned-file whitespace | PASS | `git diff --check` scoped to all 10 changed implementation/test paths. |
| Full project regression suite | NOT RUN by Worker | No installed pytest was available; Architect owns final whole-project validation. The focused safety suite needs no new dependency. |
| Hosted deployment/readback | NOT RUN by Worker | No publication was authorized in the Worker scope. Successful local packaging is not a hosted release claim. |
| Dependency advisory scan | NOT RUN | Version/dependency manifests were inspected; no broad vulnerability-clearance claim is made. |

The Architect reported a live `/.well-known/security.txt` response of HTTP
404 during this assessment. The Worker did not independently fetch that
response. The default hidden-file omission explains a plausible transport
cause; downloading the exact historical intermediate artifact would confirm
the cause. The local correction is not a claim that the hosted URL is fixed.

The baseline candidate artifact contained 319 files totaling 130,074,690
bytes. The repaired artifact omits seven nonruntime files totaling 15,495,431
bytes. This reduces deployment archive size, not necessarily page-load bytes:
unrequested source art was never part of a normal page's network budget.

Rollback is a reviewable reverse patch of the builder, tests, scratch
inventory exclusions, and CI path/hidden-transport edits together. Preserve concurrent owner changes. Do not discard repository
state with reset/checkout or delete the tracked artifact snapshot.

## Remaining decisions and boundaries

No backend, authentication layer, database, framework, or runtime dependency
is needed to carry out these recommendations. Subsequent work should first
make the shipped artifact and its evidence trustworthy, then harden QA and
maintenance tooling, then optimize delivery. Hosting-edge changes, analytics
policy changes, deletion of tracked release copies, and any cross-repository
sync require separately scoped decisions. All browser/header results and
current remote state must come from the Architect's live evidence, not from
the contents of `_headers` or a historical audit score.

# Static-site release check matrix

Use this as a mapping aid, not as permission to invent replacement checks.
Adapt paths only after inspecting the target repository.

| Stage | Command or evidence | What it proves | Typical limitation |
|---|---|---|---|
| HTML/site validation | `python3 scripts/validate-site.py` | Required metadata, structure, local links/assets, sitemap, governance checks | Static parsing; warnings do not fail |
| Link checker | `python3 scripts/check-links.py` | Internal href resolution and sitemap reconciliation | External links are not fetched |
| Regression suite | `python3 -m pytest` | Repository tests, including generated-index and artifact-boundary regressions | Only covers checked-in tests |
| Generated freshness | `python3 scripts/build-search-index.py --check` | Committed index matches current HTML while ignoring its volatile timestamp | Does not authorize a rebuild |
| Full audit | `python3 scripts/audit-site.py --quiet` | Page hygiene, accessibility-oriented markup, modern baseline, index/sitemap drift | Static audit; human assistive-tech review remains separate |
| Browser QA | `node scripts/responsive-qa.mjs --base=...` | Runtime overflow, console errors, resource and image loading at listed viewports | Needs Node, Playwright, Chromium, server |
| Static QA | `node scripts/responsive-qa.mjs --static` | Explicit structural fallback at the same viewport rows | Cannot prove runtime behavior |
| Artifact | `python3 scripts/prepare-pages-artifact.py --output <disposable-dir>` | Allowlisted public file tree and digest | Prepares only; never uploads |
| CI | Checked-in workflow plus actual run URL/log | Host validation and exact artifact handoff | GitHub access and a real run required |
| Hosted | Authorized Pages URL, revision, route and asset smoke checks | Published behavior | DNS, permissions, and third-party availability may remain unknown |

For this repository, `.github/workflows/validate.yml` is the CI source of truth:
it installs dependencies and Chromium, runs the local checks, prepares and
uploads the artifact, then deploys only the downloaded validated artifact.
Do not copy AskJamie content, palettes, typography, referral policies, or
companion-site visual audits into a portable release skill.
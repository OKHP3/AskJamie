# AskJamie technology and version review

Reviewed September 18, 2026 in America/Chicago. Publisher checks occurred
September 19 UTC. Baseline: `8decfb8679c76818b2a27c68c5dc43b1719ab112`.

## Finding

AskJamie uses static HTML, shared CSS, browser JavaScript, a vendored Mermaid
runtime, and Python/Node maintenance tools. It has no application compiler,
backend, database, TypeScript source, Vite configuration, Tailwind pipeline,
React, or Next.js application. Those names in reference skills, historical
documents, or upstream package descriptions are not evidence of application
use. `tslib` and type declaration packages in the npm tree are transitive
tooling, not a TypeScript build for AskJamie.

This inventory separates repository declarations, resolved locks, workstation
observations, web standards, and provider-managed services. A source pin does
not prove which version ran in CI, Replit, or the live deployment.

## Deliverables and coverage

- [Every package/action version and publisher source](technology-versions.md).
- [Machine-readable evidence, constraints, paths, and local observations](technology-versions.json).
- [Update policy, activation steps, and prioritized upgrade plan](../../../docs/technology-update-policy.md).

The lock inventory contains 111 npm package locations representing 98 unique
names. All locations are listed, including nested copies with different
versions. The source review also covers all nine distinct GitHub Actions,
Python QA dependencies and installed transitive closure, browser engine
revisions, platform configuration, and the standards and services below.

The snapshot reflects the working tree after adding the update mechanism.
Before this change, pytest was only constrained as `>=8` and CI ran
`pip install beautifulsoup4 "pytest>=8"`, bypassing `requirements-qa.txt`.
This change pins pytest to the observed/current 9.1.1 and makes CI consume
that requirements file. The application dependencies are otherwise unchanged.

## Core version comparison

| Technology | In place at review start | Latest stable from publisher | Interpretation |
| --- | --- | --- | --- |
| Node.js | 22.19.0 in `.node-version`, engines, and lock; local 24.11.1 | 26.9.0 Current; 24.21.0 LTS; 22.23.2 on the configured major | Adopt tested LTS; local differs from contract. [Node release index](https://nodejs.org/dist/index.json) |
| Python | CI/Replit 3.11, project minimum >=3.11; local 3.14.0rc1 | 3.14.7; 3.11.16 on configured branch | CI patch unknown; workstation uses a prerelease. [Python downloads](https://www.python.org/downloads/) |
| npm | Not separately pinned; Node 22.19.0 bundles 10.9.3; local 11.6.2 | 12.0.2 | npm 12 requires newer Node than 22.19.0. [npm metadata](https://registry.npmjs.org/npm/latest) |
| pip | No repository pin; local 25.1.1 | 26.2.1 | Environment installer, distinct from application packages. [PyPI](https://pypi.org/pypi/pip/json) |
| Playwright | Declared, locked, locally installed 1.60.0 | 1.63.0 | Update package and managed browsers together. [Publisher](https://registry.npmjs.org/playwright/latest) |
| Lighthouse | Declared/locked 13.4.1; locally installed 12.8.2 | 13.5.0 | Local install is stale. [Publisher](https://registry.npmjs.org/lighthouse/latest) |
| Mermaid | Vendored 11.17.2 | 12.0.0 | Major migration with visual/browser compatibility changes. [Release](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0) |
| Beautiful Soup | Requirements/local 4.15.0; CI previously unpinned | 4.15.0 | No package bump needed; CI now consumes the pin. [PyPI](https://pypi.org/pypi/beautifulsoup4/json) |
| pytest | Project/CI >=8; local 9.1.1 | 9.1.1 | Now pinned in QA requirements. [PyPI](https://pypi.org/pypi/pytest/json) |

## Browsers and vendored internals

| Component | In-place evidence | Latest stable / managed candidate | Update method |
| --- | --- | --- | --- |
| Chromium and headless shell | Playwright 1.60.0 metadata: 148.0.7778.96, revision 1223; Chromium is the CI target | Chrome for Testing Stable 153.0.8010.52; Playwright 1.63.0 pairs with 153.0.8010.12, revision 1243 | Use Playwright's matched browser revision; stable Chrome is a separate comparison |
| Firefox | Playwright metadata: 150.0.2, revision 1522; not installed by this CI workflow | Playwright 1.63.0 pairs with 155.0, revision 1543 | Optional QA engine; metadata is not proof of installation or coverage |
| WebKit | Playwright metadata: 26.4, revision 2287; not installed by this CI workflow | Playwright 1.63.0 pairs with 26.6, revision 2359 | Optional QA engine; this is Playwright WebKit, not an installed Safari version |
| Mermaid bundled libraries and diagram engines | Served ESM/chunks under `assets/vendor/mermaid/`; top-level version 11.17.2 | Owned by the Mermaid release, latest 12.0.0 | No local upstream lock/SBOM gives every internal resolved version; do not invent one |

Sources: [current Playwright browser manifest](https://raw.githubusercontent.com/microsoft/playwright/v1.60.0/packages/playwright-core/browsers.json),
[latest Playwright browser manifest](https://raw.githubusercontent.com/microsoft/playwright/v1.63.0/packages/playwright-core/browsers.json),
[Chrome for Testing stable metadata](https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json).
Browser revisions are package metadata, not a claim that every binary is
installed. The npm appendix also includes Playwright Core, Lighthouse's
Chrome launcher, DevTools protocol, parsers, and all other locked components.

## Standards, formats, and unversioned runtime code

| Technology | How it is used / in-place version | Current publisher standard | Tracking approach |
| --- | --- | --- | --- |
| HTML | HTML5 doctype in published pages; no numeric language pin | [WHATWG Living Standard](https://html.spec.whatwg.org/multipage/) | Structural checks plus rendered browser tests |
| CSS | Custom properties, media queries, layout and shared themes; no single CSS version | [CSS Snapshot 2026](https://www.w3.org/TR/css-2026/), comprising separately versioned modules | Browser support and visual regression checks |
| JavaScript / ECMAScript | Native scripts, ESM, imports, DOM APIs; no transpiler target | [ECMA-262 edition 17, ECMAScript 2026](https://ecma-international.org/publications-and-standards/standards/ecma-262/) | Browser and Node compatibility; no package to bump |
| DOM, Fetch, Web Storage, import maps | Native browser APIs used by shared behavior and search; no local version pin | Browser / living standards | Behavior tests and supported-browser review |
| SVG | Images and Mermaid-generated diagrams; no declared conformance version | [SVG 2 publication](https://www.w3.org/TR/SVG2/) is a Candidate Recommendation, not a finalized replacement release | Browser rendering and accessible fallback checks |
| JSON | Search index, configuration, lockfiles and manifests | [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) | Parser/schema checks; lockfile format separately records version 3 |
| JSON-LD | Embedded structured data; no `@version` declaration | [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) | Validate current page data; do not invent a declared 1.1 pin |
| Schema.org | `https://schema.org` context, unpinned vocabulary | [30.1, September 16, 2026](https://schema.org/docs/releases.html) | Review used terms on vocabulary changes |
| YAML | GitHub workflows and brand registry; no dialect directive | [1.2.2](https://yaml.org/spec/1.2.2/) | Validate against the consuming service, which can impose its own subset |
| TOML | `pyproject.toml` and `.replit`; no version directive | [1.1.0](https://toml.io/en/) | Keep syntax supported by Python and Replit parsers |
| Markdown / GitHub Flavored Markdown | Documentation and Agent Skills; no parser package or version pin | GitHub-managed Markdown rendering | Links, readable structure, provenance |
| XML / sitemap protocol | Sitemap XML; XML declaration and sitemap namespace | Stable protocol, not a package dependency | Sitemap/link validation |
| Web App Manifest | `site.webmanifest`, JSON metadata | Browser-maintained specification | Validate fields and icon URLs |
| PNG, JPEG, WebP, ICO | Stored assets; format bytes rather than application libraries | No meaningful shared semver release to install | Asset validation; image-tool updates only when tooling is used |
| CSP and referrer policy | Generated HTML metadata plus portable `_headers` | Browser/hosting policies, not package releases | CSP/source tests; response-header enforcement needs live evidence |
| First-party Python, JS, CSS and maintenance scripts | Git-versioned repository code | No external stable release | Maintain in source and test with the updated toolchain |

## Platforms, tools, and services

| Technology | In place | Latest / evidence boundary | Owner and update method |
| --- | --- | --- | --- |
| GitHub Actions | Nine action packages with mixed major tags and SHA pins | All exact references and resolved releases are in the snapshot | Dependabot PRs |
| GitHub-hosted Linux runner | `ubuntu-latest`; no image build pinned | Provider-managed moving image; exact running image unknown without job log. [Image manifest](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md) | Monthly runner review and CI |
| Bash and core utilities | Workflow run blocks and `scripts/post-merge.sh`; no version pin | Runner-provided; local `bash` currently routes to unavailable WSL | Verify installed runner tools; avoid claiming a host version from source |
| Git / Git for Windows | Local 2.55.0.windows.5; CI supplied by runner | Git source 2.55.0; Windows release 2.55.0.windows.5. [Git](https://git-scm.com/), [Windows release](https://github.com/git-for-windows/git/releases/tag/v2.55.0.windows.5) | Host package manager, outside site dependency PRs |
| PowerShell | Local 7.6.5, used for this Windows review; not a site runtime | [7.6.6](https://github.com/PowerShell/PowerShell/releases/tag/v7.6.6) | Host updater |
| GitHub CLI | Local 2.96.0, review tool; not required by the application | [2.101.0](https://github.com/cli/cli/releases/tag/v2.101.0) | Host updater |
| Replit | Modules `web`, `nodejs-22`, `python-3.11`; GitHub integration `1.0.0` | Provider capabilities, not public npm package versions. Live installed modules and integration compatibility not checked | [Replit configuration documentation](https://docs.replit.com/features/project-setup/configuration); verify on that host |
| Nix channel | `.replit`: `stable-25_05` | Upstream NixOS [26.05](https://nixos.org/download/) exists, but that does not prove a matching Replit channel is supported | Confirm Replit-supported channel before migration |
| GitHub Pages | Static allowlisted artifact deployed by Actions | Hosted service with no repository-selectable semantic version | Successful deployment plus live smoke; no Jekyll/bundler application build |
| Google Fonts | CSS2 API; Baloo 2, Open Sans, Kalam; no font revision pins | [Provider-managed CSS2 endpoint](https://developers.google.com/fonts/docs/css2) | Existing fonts/network/fallback checks |
| JetBrains Mono and system fallbacks | CSS font-family declarations; page font request does not establish this font is downloaded | Actual font selected depends on availability | Browser computed-font review when typography changes |
| Google Analytics 4 / Google tag | GA4 tag ID and hosted `gtag/js`; no release pin | Provider-managed script | Hosted script, consent/fallback behavior, and CSP tests |
| ChatGPT GPT links, social/referral links | Outbound destinations, not SDK dependencies | Remote services, no local version | Existing public GPT link and general link checks |

## Contributor tooling and archive boundary

`.agents/skills/` is an agent-support catalog, not served application code.
Seven BP-SKILL `package.json` files each declare version 0.1.0 with no npm
dependencies. Skill versions and `skills-lock.json` source hashes track
imported instructions, not a framework installed in the site. Vite and
React guidance is explicitly reference-only here. Updating those packages
requires their separate provenance/promotion process.

Archived image helpers refer to Pillow; this workstation has Pillow 12.3.0,
also the latest stable [PyPI release](https://pypi.org/pypi/Pillow/json). It is
not an active CI requirement and was not added to the application stack.
Other workstation packages such as PyYAML and jsonschema are not application
dependencies merely because they are installed globally.

## Evidence and limitations

Confirmed: tracked manifests and workflow references, all npm lockfile
versions, local observed versions, and publisher results linked in this
review. The generated JSON records retrieval time and source URLs; publisher
registries are authoritative for their published package versions, and
standards bodies are authoritative for their specifications.

Unknown: exact CI/Replit installed versions without a fresh run, internal
resolved versions hidden inside the vendored Mermaid bundle, actual loaded
font file revisions, provider internal service versions, and candidate
upgrade compatibility. These are explicit coverage limits. No web search can
recover a missing local installation receipt by inference.

The legacy `check-stack-conformance.py` assumes fixed old package versions
and references an ADR number that belongs to a different topic here. It is
not the CI release gate. `npm run check:stack` now invokes the new auditor,
which checks agreement among real inputs
without forcing old versions; do not use the legacy `--fix` mode to perform
upgrades. Broader cleanup of that inherited tool remains separate work.

Validation and activation evidence is recorded in [validation.md](validation.md).
The next action is to review and merge the prepared update mechanism, then
verify the first GitHub runs and resolve its initial upgrade queue.

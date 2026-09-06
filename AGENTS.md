# Agent Guidelines: AskJamie

This is the canonical agent guide for the AskJamie repository. Read it before
changing files. It applies to coding, content, QA, documentation, and asset
work performed in this repository.

Work in small, reviewable steps. Keep changes localized. Preserve existing
user changes. Ask before a large refactor or a change that crosses repository
boundaries. Never invent credentials or secrets.

## 1. Target and scope

- Repository root:
  - Windows: `C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie`
  - Mac: `/Volumes/OKH-Local/04_GitHub_Mirrors/AskJamie`.
- Git repository: `OKHP3/AskJamie`, with `main` tracking `origin/main`.
- Site origin: `https://askjamie.bot`.
- Deployment model: GitHub Pages serves an allowlisted static artifact. Release
  automation refreshes the search index and universe maps before validation.
  There is no application runtime or framework build.
- No nested independent Git repository was found during the July 13, 2026
  context inspection.

This guide describes the root project only. The `.agents/skills/` directory is
agent tooling, not application source. The `assets/docs/sister-site-sync/`
directory contains reference material for sibling repositories, not a second
project in this repository.

### Instruction precedence

`AGENTS.md` is the canonical project guide. `CLAUDE.md` is a short pointer for
Claude-specific tooling. `replit.md` contains Replit workflow notes and must
agree with the current facts here. `.github/copilot-instructions.md` contains
general Copilot response guidance. A more specific instruction file would
apply only within its directory.

## 2. Project understanding

### Confirmed purpose

AskJamie is a public marketing and documentation site for a warm, technically
literate AI helpdesk persona and thinking partner. The site presents the Lens
System portfolio, including GPT architecture case studies, BrandGuard public
information demonstrations, Enterprise Sleuth, Professional Portfolio, and
Resume Representative.

The primary user value is clear explanation of decisions, workflows, systems,
and AI-related questions. The site is also a portfolio artifact showing how a
small static site can package AI concepts for human readers and AI crawlers.

### Mission and vision

- Confirmed mission: demonstrate AskJamie and its Lens System through readable,
  inspectable web pages and case studies.
- Inferred vision: make intentional brand and AI reasoning easier to understand
  before a visitor needs to adopt a tool or workflow.
- Unknown: no separate owner-approved mission or product roadmap was found
  beyond the site copy, README, and existing planning documents.

### Scope and non-goals

In scope:

- Static HTML pages for the homepage, About, Contact, Legal, Universe, Search,
  Lens System, and BrandGuard case studies.
- Shared CSS, browser JavaScript, metadata, structured data, images, templates,
  search indexing, and static-site QA.
- Documentation and maintenance scripts that support this site or its sibling
  site synchronization workflow.

Out of scope unless explicitly requested:

- A backend, database, authentication, form-processing service, or API server.
- A framework migration, bundler, package replacement, or new runtime.
- Claims that a public page is a live production AI service when the page is a
  portfolio demonstration or public-information proof of concept.
- Changes to sibling repositories, external websites, GitHub settings, or
  connected services.

## 3. Current implementation

### Confirmed architecture

- Frontend: vanilla HTML5, CSS3 custom properties, and browser JavaScript.
- Diagramming: Mermaid.js v11 is vendored locally under
  `assets/vendor/mermaid/` and imported by `universe/index.html`.
- Typography: AskJamie pages load Baloo 2, Open Sans, and Kalam from the
  Google Fonts stylesheet declared in each page shell.
- Search: zero-dependency client-side search in `assets/js/app.js`, backed by
  generated `assets/data/search-index.json`.
- Analytics: Google tag `G-MT9Y10YY0G` loads from the page shell, while the
  shared browser script provides the no-op-safe event wrapper.
- Security baseline: page-level CSP and referrer metadata, plus `_headers` for
  the static hosting edge.
- Optional QA tooling: Node and Playwright are declared in `package.json`, but
  the current checkout did not have Playwright available. Static QA remains
  runnable without it.

### Repository shape

```text
index.html                  Homepage
about/ contact/ legal/      Primary interior pages
universe/                   Mermaid ecosystem map
search/                     Dedicated client-side search page
lens-system/                Portfolio hub and case studies
  resume-representative/
  professional-portfolio/
  enterprise-sleuth/
  okhp3-brandguard/         Hub plus 13 public-information case studies
assets/css/theme.css        Canonical shared stylesheet
assets/js/app.js            Shared browser behavior and search
assets/js/mermaid-init.js   Mermaid module initializer
assets/data/                Generated runtime data, including search index
assets/img/                 Served images, favicons, OG cards, and references
assets/templates/           Developer scaffolding, excluded from public QA
assets/docs/                Human-authored audits and sync documentation
scripts/                    Validation, build, audit, and maintenance tools
docs/adr/                   Architecture Decision Records (key design choices)
docs/brandguard/            BrandGuard-specific working documentation
docs/security/              Security threat-model documentation
brand-styles/               Visual style registry and AskJamie brand profile
.github/                    GitHub workflow and Copilot guidance
SUPPORT.md                  Where to file bugs, ask questions, and get help
CONTRIBUTING.md             Contribution guidelines
SECURITY.md                 Security reporting policy
```

The repository currently contains 35 HTML files on disk. Nine are templates,
leaving 26 QA-relevant HTML paths. The responsive QA script uses the 24 routes
in `sitemap.xml` for 192 checks; the two additional utility pages,
`404.html` and `under-construction.html`, remain covered by structural and
audit checks. The current status and evidence boundaries are recorded in
`assets/docs/project-scorecard.md`.

### Agent skills

The `.agents/skills/` directory holds Agent Skills for AI assistants. Not all
installed skills apply to this tech stack. Two are retained as reference only
and must not be activated for this repo:

- **`okhp3-vite-github-pages`** — a runbook for a separate React/Vite app
  deployed to GitHub Pages. This repo is a static HTML site with no Vite
  build step, React code, or GitHub Pages deployment. Do not add a
  `vite.config.ts`, `package.json` build scripts, or React components on the
  basis of this skill.
- **`vercel-react-best-practices`** — React and Next.js optimization rules.
  This repo contains no React or Next.js code. Do not apply these rules here.

All other installed skills are applicable. See `.agents/skills/README.md` for
the full applicability table.

### Brand contract

Pages must use `<body class="askjamie-main">` unless a utility page has a
documented reason to differ. Preserve the AskJamie paper-first treatment:

| Element | Value |
| --- | --- |
| Page background | `#f6f2ee` |
| Card surface | `#fdfbf7` |
| Text | `#2e2b29` |
| AskJamie accent | `#2d6f7e` |
| Footer surface | `#f7f3ee` |
| Dark-mode metadata teal | `#2c5e6f` |
| Heading font | Baloo 2 |
| Body font | Open Sans |
| Accent font | Kalam |
| Mono font | JetBrains Mono |

Do not make dark mode the default visual treatment for new pages. Do not
introduce the OverKill Hill rust-orange palette, Glee-fully coral palette,
industrial forge styling, Alfa Slab One, or Fredoka into AskJamie-specific
work. Builders FirstSource references are valid in the existing BrandGuard case
study and related site content. They are not forbidden content for this repo.

## 4. Development and validation

### Local server

Run from the repository root:

```bash
python3 -m http.server 5000 --bind 0.0.0.0
```

Open `http://localhost:5000`. The Replit `Start application` workflow uses the
same command.

### Quality gates

Run the relevant checks after HTML, CSS, JavaScript, metadata, asset, or copy
changes:

```bash
python3 scripts/validate-site.py
python3 scripts/check-links.py
node scripts/responsive-qa.mjs --static
python3 scripts/audit-site.py --quiet
```

`validate-site.py` is the structural validator. `check-links.py` writes a
dated JSON report under `assets/audit/`. `responsive-qa.mjs --static` checks
the 24 sitemap routes at eight viewports for 192 checks without a browser. A
full browser run requires Playwright and Chromium. `audit-site.py` is the
canonical site audit and writes `assets/docs/audit-report.md`.

### Visual baseline updates

The committed visual reference set lives in `assets/audit/visual-baseline/`.
After an intentional visual change, run the capture script against the local
server:

```bash
node scripts/capture-visual-baseline.mjs
```

Review the resulting homepage, BrandGuard card, and Universe diagram images at
1280px and 390px before replacing the committed references. Update the dated
performance report and commit the new images only when the visual change is
intentional and understood.

The July 24, 2026 inspection re-ran these checks against the working tree
(last commit `93d4b02`, 2026-07-22; working tree clean):

- `validate-site.py`: passed, 26 HTML pages clean.
- `check-links.py`: passed, 26 pages scanned, 711 internal and 559 external
  links checked, 0 broken links, 0 style issues.
- `responsive-qa.mjs --static`: passed, 208 of 208 checks in that historical
  route inventory. The current script uses the sitemap inventory and reports
  192 checks.
- `audit-site.py --quiet`: exited successfully but reported historical findings
  involving an ignored `.DS_Store`, a stale generated search index, and an
  index-shape warning. Those findings are not the current release result. Use
  the current scorecard and rerun the commands above instead of treating this
  dated inspection as present state.

### Generated data and mutation rules

After a content change, rebuild the search index with:

```bash
python3 scripts/build-search-index.py
```

Do not hand-edit `assets/data/search-index.json` or audit output. Scripts that
mutate HTML should be idempotent and retain their existing `AUTOGEN` marker
conventions where applicable. `scripts/post-merge.sh` verifies core files,
rebuilds the search index, and runs the canonical audit. Review its effects
before running it in a worktree with uncommitted content changes.

### CI and deployment

`.github/workflows/validate.yml` runs on pushes and pull requests targeting
`main`. It installs Python 3.11 tooling, runs the site validator and link
checker, rebuilds the search index, and verifies that the generated index
exists. The static deployment publishes the repository root. `CNAME` declares
`askjamie.bot`, and `robots.txt` points crawlers to `sitemap.xml`.

## 5. Safe change conventions

- Use US English in all new user-facing copy, documentation, comments intended
  for people, prompts, and QA reports.
- Do not use em dashes anywhere in new or edited content. Use a period or
  restructure the sentence.
- Avoid filler claims such as "seamlessly," "robust," "powerful," and
  "effortlessly." Keep intentional short paragraphs intact.
- Keep one canonical stylesheet in `assets/css/theme.css`. Do not add page
  style blocks or new component stylesheets without explicit approval.
- Keep browser-served JavaScript in `assets/js/`. Keep maintenance tooling in
  `scripts/`, using lowercase kebab-case for new plain script filenames.
- Keep published HTML in the root or named content directories. Keep templates
  in `assets/templates/` and exclude their placeholder tokens from public QA.
- New asset, data, documentation, and plain-script filenames use lowercase
  kebab-case. Preserve ecosystem-required names such as `AGENTS.md`,
  `README.md`, `package.json`, and `site.webmanifest`.
- Every published page should retain a title, description, canonical URL,
  language attribute, one h1, JSON-LD where appropriate, image alt/size/loading
  attributes, and root-relative internal links.
- Do not add dependencies unless explicitly requested. Do not add credentials
  to source, documentation, workflows, or examples.
- Before changing `theme.css` or `assets/js/app.js`, read
  `assets/docs/sister-site-sync.md`. These files are shared family sources and
  may require coordinated work in sibling repositories, but do not modify
  sibling repositories without explicit authorization.

### Mermaid pages

Any page containing `<div class="mermaid">` must include the existing
`mermaid-referral-link` affiliate note directly under the diagram, with
`target="_blank" rel="noopener noreferrer"`. The canonical referral URL is
`https://mermaidchart.cello.so/UhVlNtC2MlS`. The audit enforces this rule.

### Shared-file and filename changes

If a file is renamed, update every importer and deployed URL reference in the
same change. Run the validator and audit afterward. Do not use destructive Git
commands such as `git reset --hard` or `git checkout --` to discard work.

## 6. Known gaps and risks

These are current evidence-backed observations, with dated historical context
retained where it matters:

- The canonical audit is a generated release check. Rebuild
  `assets/data/search-index.json` after copy changes, then run
  `python3 scripts/audit-site.py --quiet`; do not report a historical finding
  as current.
- `scripts/README.md` classifies every maintenance script. Only the active
  scripts remain at the top level. Reference-only and retired scripts are
  preserved in `scripts/archive/` with a prominent warning because several
  contain sibling-site constants or historical names.
- Use `scripts/audit-site.py` for the canonical AskJamie audit,
  `scripts/validate-site.py` for structural validation, and
  `scripts/responsive-qa.mjs` for responsive QA. Do not run archived scripts
  without reviewing their target paths and intended repository.
- `README.md`, `ROADMAP.md`, and `replit.md` state the current inventory and
  link to the single current scorecard. Treat dated audit documents as
  historical evidence, and rerun the relevant check before making a present
  release claim.
- `assets/docs/` contains historical audit and sync reports. Do not treat an
  old report as current without checking its date and rerunning the relevant
  check.
- Human VoiceOver/NVDA spoken output remains unknown. Headless Chromium and
  static checks verify DOM, keyboard, and fallback behavior only. External
  Google Fonts and GA4 availability are also outside static QA's proof.
- No owner-approved product roadmap or backend integration specification was
  found. Ask the owner before inferring one.

## 7. Keeping this guide current

Update this file when the project purpose, architecture, deployment model,
quality commands, public path list, brand contract, or known risks change.
Record dated audit results as dated evidence. Keep historical reports in
`assets/docs/` and avoid copying stale counts into current guidance.

Structural changes to shared governance sections may need to be synchronized
with the related OverKill Hill P3 and Glee-fully repositories. Confirm scope
before making cross-repository changes.

At the end of work, summarize what changed, why it changed, which checks ran,
and any unresolved questions.

## Universe map integration (2026-09-06)

`universe-map.config.json` configures the installed `okhp3-universe-map` skill.
`scripts/build-search-index.py` refreshes the index, then invokes
`scripts/sync-universe-map.py` to replace the owned `AUTOGEN:UNIVERSE-MAP` block
in `universe/index.html` and write `assets/data/universe-map.json`.
The index extractor excludes that block to prevent feedback. Use
`python3 scripts/sync-universe-map.py --check` for a read-only freshness check.

The validation/deployment workflow regenerates before its gates on main pushes,
manual dispatch, and a daily scheduled reconciliation. Pull requests run the
same checks without deployment. Indexed page status does not certify a working
or completed project. Sibling maps are linked directly, not cached locally.

The old map is preserved in `assets/docs/universe-map-legacy-2026-09-06.mmd`.
Its speculative nodes are historical, with unconfirmed current status. The
byte-identical duplicate janitor skill was preserved outside discovery under
`.agents/skill-archives/`; the active skill catalog now includes the map skill.

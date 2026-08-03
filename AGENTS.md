# Agent Guidelines: AskJamie

This is the canonical agent guide for the AskJamie repository. Read it before
changing files. It applies to coding, content, QA, documentation, and asset
work performed in this repository.

Work in small, reviewable steps. Keep changes localized. Preserve existing
user changes. Ask before a large refactor or a change that crosses repository
boundaries. Never invent credentials or secrets.

## 1. Target and scope

- Repository root: `/Volumes/OKH-Local/04_GitHub_Mirrors/AskJamie`.
- Git repository: `OKHP3/AskJamie`, with `main` tracking `origin/main`.
- Site origin: `https://askjamie.bot`.
- Deployment model: static files from the repository root. There is no
  application build step or server-side runtime.
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
- Diagramming: Mermaid.js v11 as an external ESM module, used by
  `universe/index.html`.
- Typography: Google Fonts loaded by the page shell. AskJamie pages use Baloo
  2 for headings, Open Sans for body text, and Kalam for accent text.
- Search: zero-dependency client-side search in `assets/js/app.js`, backed by
  generated `assets/data/search-index.json`.
- Analytics: Google tag `G-MT9Y10YY0G` appears in the page shell and is handled
  by the shared browser script.
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
brand-styles/               Visual style registry and AskJamie brand profile
.github/                    GitHub workflow and Copilot guidance
SUPPORT.md                  Where to file bugs, ask questions, and get help
CONTRIBUTING.md             Contribution guidelines
SECURITY.md                 Security reporting policy
```

The repository currently contains 35 HTML files on disk. Nine are templates,
leaving 26 paths in the responsive QA list. The 26 QA paths include utility
pages such as `404.html` and `under-construction.html`.

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
the 26 listed public paths at eight viewports without a browser. A full
browser run requires Playwright and Chromium. `audit-site.py` is the canonical
site audit and writes `assets/docs/audit-report.md`.

The July 24, 2026 inspection re-ran these checks against the working tree
(last commit `93d4b02`, 2026-07-22; working tree clean):

- `validate-site.py`: passed, 26 HTML pages clean.
- `check-links.py`: passed, 26 pages scanned, 711 internal and 559 external
  links checked, 0 broken links, 0 style issues.
- `responsive-qa.mjs --static`: passed, 208 of 208 checks.
- `audit-site.py --quiet`: exited successfully but reported three findings:
  the ignored `.DS_Store`, a stale generated search index (index.html,
  legal/index.html, the BFS BrandGuard case study, and search/index.html are
  all newer than `assets/data/search-index.json`), and a shape warning noting
  the search index is a dict rather than the expected list. The 168-character
  Universe description flagged on July 13 no longer appears, so that one item
  has been resolved since the last inspection.

These findings remain open because this context-maintenance task does not edit
source or generated artifacts.

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

Any page containing `<pre class="mermaid">` must include the existing
`mermaid-referral-link` affiliate note directly under the diagram, with
`target="_blank" rel="noopener noreferrer"`. The canonical referral URL is
`https://mermaidchart.cello.so/UhVlNtC2MlS`. The audit enforces this rule.

### Shared-file and filename changes

If a file is renamed, update every importer and deployed URL reference in the
same change. Run the validator and audit afterward. Do not use destructive Git
commands such as `git reset --hard` or `git checkout --` to discard work.

## 6. Known gaps and risks

These are evidence-backed observations from the July 13, 2026 inspection:

- The canonical audit is not currently at zero findings. See the exact three
  findings in the validation section above. Run
  `python3 scripts/build-search-index.py` to clear the stale-index finding
  before the next content release.
- `scripts/site-audit.py` is a separate OverKill Hill audit script with the
  wrong GA4 constant for this site. Use `scripts/audit-site.py` for AskJamie.
- Several maintenance scripts contain sibling-site constants or historical
  names. Check the target script and `assets/docs/sister-site-sync.md` before
  running or adapting them.
- `README.md` and older sections of `replit.md` retain historical counts and
  audit snapshots from earlier site states. Treat dated audit documents as
  history, and use current scripts and this guide for present state.
- `assets/docs/` contains historical audit and sync reports. Do not treat an
  old report as current without checking its date and rerunning the relevant
  check.
- Browser-level responsive behavior, console errors, runtime image loading, and
  external CDN behavior were not verified in the latest inspection because
  Playwright was unavailable and the isolated QA run used static lint.
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

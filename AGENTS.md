# Agent rules

- Work in small steps. Ask before large refactors.
- Prefer adding tests before changing logic if risk is medium/high.
- Keep changes localized. Avoid touching unrelated files.
- If you need config/secrets, stop and ask. Never invent credentials.
- Summarize what you changed and why at the end.

---

## Repository Hygiene Standard

**Brand:** AskJamie (Teal / Paper)
**Body scope class:** `askjamie-main` (pages set `<body class="askjamie-main">`)
**Canonical stylesheet:** https://raw.githubusercontent.com/OKHP3/OverKill-Hill/main/assets/css/theme.css
**Version:** 1.0

This section governs how files and folders are named, what structure all sibling repos share, what counts as detritus, and the brand contract this repo serves.

### 0. Language Standard: en-US

This project is authored, owned, and maintained by a United States-based creator. All user-facing content must use United States English (`en-US`).

**Scope:** UI copy, documentation, README content, release notes, comments intended for human readers, prompts, tooltips, button text, error messages, validation messages, QA/QC reports, marketing language, and any new code identifiers authored in this repo.

**Examples of required US-EN spellings:** color, behavior, organization, optimize, customize, center, analyze, modeling, artifact, visualization, standardization, initialize, finalize, prioritize, summarize, license (noun), program, catalog, fulfill, gray, toward, among, while.

**Protected exceptions (do NOT change spelling in):**
- Direct quotations from external sources
- Proper nouns, brand names, product names
- Dependency, package, or library names
- URLs, file names, route names
- API fields, schema keys, existing code identifiers
- Generated lockfiles or external standards

**Identifier rule:** en-US applies to identifiers authored in *new* code. Renaming *existing* identifiers (variables, functions, types, exported symbols) is a breaking change and falls under the same renaming policy as files in Section 1: update every importer in the same commit, run the build and tests after, and set up a redirect if anything external depends on the old name. Do not run a blanket find-and-replace across existing identifiers without explicit instruction.

**Status:** US English compliance is a required QA/QC gate, not a stylistic preference. Any output failing this standard is a defect.

### 1. Naming conventions

Kebab-case by default with three structural exceptions, all dictated by ecosystem convention.

| File role | Convention | Examples |
|---|---|---|
| Docs (.md), CSS, YAML, JSON-data, SVG, plain scripts | kebab-case | `design-system.md`, `askjamie-tokens.css`, `sync-skills.sh` |
| Folder names | kebab-case | `src/styles/`, `docs/roadmap/` |
| Plain TypeScript modules (not exporting a hook or component) | kebab-case | `theme-mode.ts`, `chat-store.ts` |
| React hooks (`.ts` exporting `useFoo`) | camelCase matching the hook | `useChatSession.ts` |
| React components (`.tsx`/`.jsx`) | PascalCase matching the component | `ChatPane.tsx`, `MessageList.tsx` |
| Root governance files | ALL CAPS (ecosystem convention) | `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `AGENTS.md`, `SKILL.md` |
| Tool-required filenames | Whatever the tool requires | `package.json`, `tsconfig.json`, `vite.config.ts`, `.gitignore`, `.replit`, `.npmrc` |
| Web-standard files | Whatever the spec dictates | `humans.txt`, `robots.txt`, `404.html`, `_headers`, `favicon.ico` |

Decision tree when in doubt: (1) governance file with universal name → ALL CAPS; (2) tool-required name → whatever the tool says; (3) `.tsx`/`.jsx` component → PascalCase; (4) `.ts` hook → camelCase matching the hook; (5) everything else → kebab-case.

These rules govern filenames only. Identifiers inside code follow language conventions.

When renaming a file: update every importer in the same change, set up a redirect if the file is referenced by a deployed URL, and run the build and tests after.

### 2. Repository structure

```
<repo-root>/
├── .agents/
├── .github/
├── .gitignore
├── .replit, .replitignore, .npmrc, .prettierrc
├── AGENTS.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE, README.md
├── docs/
│   ├── design-system.md
│   └── roadmap/
├── public/
├── scripts/
├── skills/
├── src/
│   ├── components/           PascalCase React components
│   ├── data/                 kebab-case
│   ├── hooks/                useFoo.ts hooks
│   ├── lib/                  kebab-case modules
│   ├── pages/                PascalCase route components
│   ├── styles/               CSS (e.g., askjamie-tokens.css if locally extracted)
│   └── __tests__/
├── e2e/
├── examples/
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

Forbidden root folder names (reserved for detritus): `_unused/`, `attached_assets/`, `attached-assets/`, `_drafts/`, `_scratch/`, `_old/`, `tmp/`, `temp/`, `unused/`.

### 3. Detritus

- `attached_assets/` -- Replit paste-buffer transcripts and screenshots. Always gitignored. Delete if committed.
- `_unused/` -- Replit refactor leftovers. Triage once, delete.
- `test-results/`, `playwright-report/`, `coverage/` -- test output. Gitignore.
- `dist/`, `build/`, `.next/`, `.vite/` -- build output. Gitignore.
- `.DS_Store`, `Thumbs.db`, `.idea/` -- OS/IDE junk. Gitignore.
- `_replit/` -- old working notes. Triage: salvage to `docs/` or `docs/archive/`, delete the rest.
- Duplicated sibling-repo content (e.g., a skill folder belonging to another app). Remove.

### 4. `.gitignore` baseline

```
# Replit working-buffer artifacts
attached_assets/
attached-assets/
_unused/
unused/

# Test and build output
test-results/
playwright-report/
coverage/
dist/
build/
.next/
.vite/

# IDE / OS
.DS_Store
Thumbs.db
.idea/

# Node
node_modules/
*.log
```

If any of these are tracked, `git rm -r --cached <folder>` before committing the `.gitignore` change.

### 5. Decrapify command (reusable instruction)

When the repo accumulates working artifacts, send this short message to Replit Agent:

> **Decrapify this repo per the Repository Hygiene Standard in `AGENTS.md` Section 5.** Triage, do not just delete. Produce a plan first, then execute on confirmation. Cover: `attached_assets/` and any hyphen variant, `_unused/`, `test-results/`, `playwright-report/`, `coverage/`, `dist/`, `build/`, `_replit/` (triage into `docs/` or `docs/archive/` before deleting), any duplicated sibling-repo content, any file or folder violating Section 1, and any forbidden folder name from Section 3. Output a plan with four sections: A. DELETE / B. GITIGNORE-AND-UNTRACK / C. TRIAGE-THEN-DELETE / D. RENAME. Wait for "go" before executing.

### 6. Brand contract (AskJamie)

This repo serves the AskJamie brand. Canonical reference: https://raw.githubusercontent.com/OKHP3/OverKill-Hill/main/assets/css/theme.css (scope `.askjamie-main`).

AskJamie motif declared values:

| Aspect | Value |
|---|---|
| Body scope class | `askjamie-main` (pages MUST set `<body class="askjamie-main">`) |
| Heading font | Baloo 2 |
| Body font | Open Sans |
| Accent / handwritten | Kalam |
| Mono font | JetBrains Mono |
| Page background | paper `#f6f2ee` |
| Card surface | `#fdfbf7` |
| Text / ink | charcoal `#2e2b29` |
| Primary accent | teal `#2d6f7e` |
| Footer background | `#f7f3ee` (softened; overrides OverKill's dark footer) |
| Mermaid line/border | teal `#2d6f7e` |
| Tone | calm, mid-century, conversational |

Forbidden in this brand's apps:
- Rust-orange `#c46a2c` (that's OverKill Hill P3)
- Coral `#d94f63` (that's glee-fully)
- Forge espresso/teal-dark palette or Alfa Slab One (that's OverKill Hill P3)
- Fredoka headings (that's glee-fully)
- Industrial / forge aesthetic, blueprint grids, slab serifs
- Dark mode by default (this brand is paper/light-first; the AskJamie scope explicitly softens OverKill's dark footer)
- Builders FirstSource (BFS) references, color systems, or examples of any kind

### 7. Universal guardrails

- No em dashes anywhere (code, comments, copy, commit messages). Use periods or restructure.
- No AI filler in copy or comments: not "seamlessly," "robust," "powerful," "effortlessly," "elevate," "unleash."
- Tailwind v4 only if Tailwind is in use: no `tailwind.config.js` (tokens live in CSS via `@theme inline`).
- No new dependencies unless explicitly requested.
- All user-facing content must use US English per the Language Standard in Section 0. UK/Commonwealth spellings are defects, not stylistic variants.

### 8. US English audit command (reusable instruction)

When the repo accumulates UK/Commonwealth spellings, send this short message to Replit Agent:

> **Run the US English audit per the Language Standard in `AGENTS.md` Section 0.** Produce a QA summary first; execute corrections only after I say "go." Cover: UI copy, docs, README, release notes, human-readable comments, prompts, tooltips, error/validation messages, and QA/QC reports. Apply protected exceptions in Section 0. For existing code identifiers with UK spellings, list them as renaming candidates but do not auto-rename without confirmation. Output: (1) files scanned, (2) files to change, (3) UK spellings found, (4) proposed US-EN replacements, (5) protected exceptions. Wait for "go."

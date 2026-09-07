# AskJamie Found-Ry feature page

Date: 2026-09-07. Route: `/found-ry/` on `askjamie.bot`.

## Scope and sources

This change belongs to the public `OKHP3/AskJamie` site. The separate Found-Ry repository maintains the private application. No OverKill or Glee-fully files were changed.

The owner's [OverKill Found-Ry feature](https://overkillhill.com/projects/found-ry/) supplied the structural reference: introduction, purpose, workflow, capabilities, ecosystem, current scope, maturation, questions and next action. Its old `found-ry/index.html` source redirects to `projects/found-ry/index.html`.

The page copy describes the AskJamie workbench established in this task: authored specifications, deterministic decision tools, checklists, saved revisions, evaluations, Skillz references and private packages. It identifies the application as a private local alpha and offers a contact path, not a public launch or embed. No private source, client records or private repository links are published.

## Parent-site styling

The page reuses the shell and components of `how-askjamie-works/index.html`, the existing AskJamie avatar, and the canonical `assets/css/theme.css`. No stylesheet, shared JavaScript, dependencies or brand tokens changed. The current paper-first site contract overrides the older dark-profile seed: `askjamie-main`, paper `#f6f2ee`, teal `#2d6f7e`, Baloo 2 headings, Open Sans body and Kalam accents.

Computed background, accent and heading font matched the homepage at 1280px and 390px. Desktop and mobile screenshots were inspected. The feature contains no OverKill forge palette, typography, styling or copied body text.

## Integration and validation

- Homepage feature card and a link from How it works provide discovery.
- Sitemap, LLM entry point, search index and generated universe navigation include the new route.
- The Pages allowlist includes `found-ry/`; prepared artifact readback confirmed its HTML was included. Tracked `dist-pages/` was not hand-edited.
- Structural validation: 28 source pages passed.
- Internal/external link inventory: 830 internal and 556 external references; no broken links or style issues reported. This is the repository link check, not proof of every remote service's availability.
- Python regressions: 67 tests and 12 subtests passed.
- Browser responsive QA: 26 routes across eight viewports, 208 checks, zero failures.
- Shared asset fingerprints, search freshness, generated CSP and canonical audit passed; audit reported zero issues.
- Shared JavaScript smoke check passed.

The local environment initially lacked pytest and the installed Playwright package's matching Chromium. These were installed into the QA environment using the existing test requirements; checks were rerun successfully. No dependency manifests changed.

The feature awaits PR review and the normal main-branch Pages deployment. A local preview or prepared artifact is not publication evidence. Automated checks do not replace human assistive-technology review.

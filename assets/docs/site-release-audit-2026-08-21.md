# AskJamie.bot — Rendering and GitHub Publishing Review

**Date:** 2026-08-21  
**Scope:** AskJamie.bot public pages, local and live rendering, GitHub Actions validation, GitHub Pages artifact preparation, and comparison with OverKill Hill and Glee-fully.

## Executive result

**Status: Ready for publication after the workflow hardening in this review.**

The current site passed all available local and browser checks:

| Check | Result |
|---|---|
| HTML/site validator | 26 pages, all clean |
| Internal link checker | 711 internal links, 0 broken |
| Regression tests | 6 passed |
| Flesch-Kincaid/site audit | 0 issues |
| Playwright responsive QA | 26 pages × 8 viewports = 208/208 |
| Search-index freshness | Current; 24 indexed public pages |
| Public artifact preparation | 182 deployable files; repository-only tooling excluded |

## Confirmed rendering review

The local app was reviewed at the 1280px preview viewport and the full Playwright sweep covered 360, 390, 430, 768, 1024, 1280, 1440, and 1920px widths.

- Shared header, navigation, search trigger, specials banner, hero, cards, footer, and image loading rendered without overflow or console failures.
- The Universe diagram and BrandGuard badge pages passed the existing narrow-width and 400% reflow follow-up checks.
- The AskJamie search overlay and dedicated search page include live status announcements for result counts and no-result states.
- Focus indicators, tab order, and sticky banner behavior passed their available follow-up checks.
- AskJamie retains its warm paper, teal, and helpdesk visual language. The companion sites remain distinct: OverKill Hill uses a dark forge/grid system, while Glee-fully uses a bright retro-toolbox system.

## Publishing findings and fixes

### Confirmed issue: generated search index was not verified

The workflow rebuilt `search-index.json`, but did not verify that the committed generated file matched the current HTML. The new `--check` mode compares the generated page data while ignoring only the intentionally volatile `generated` timestamp. A stale or missing index now fails CI with a direct remediation message.

### Confirmed issue: deployment uploaded the repository root

The previous Pages job uploaded `path: '.'`, which included repository documentation, task metadata, scripts, tests, and development configuration. The new artifact-preparation script copies only public HTML, public metadata files, `.well-known` files, and runtime asset directories. It excludes repository-only tooling and caches.

### Confirmed reliability gap: validation and deployment built separate artifacts

The validation job now prepares and uploads the public artifact. The deployment job downloads that exact artifact and sends it to GitHub Pages, preventing a later independent copy step from drifting from the validated result.

### Confirmed coverage gap: CI used static responsive lint only

GitHub Actions now installs Chromium and runs the existing Playwright responsive QA against a local HTTP server. Static lint remains available for fast local checks with `--static`.

## Companion-site comparison

The comparison was limited to public repositories and published pages. No companion repository was modified.

- **OverKill Hill:** provides the strongest release reference: pinned Node setup, `npm ci`, Chromium installation, generated-index check mode, and full browser overflow checks. Its contrast audit is intentionally treated as a separate site-specific gate.
- **Glee-fully:** shares the rebuild → validate → link-check pattern and strict accent-contrast gate, but has different content synchronization requirements.
- **AskJamie:** adopts the reusable release mechanics that fit this static site—deterministic generated-file verification, Playwright installation, and exact artifact handoff—without copying companion-site palette, typography, layout, or brand-specific audits.

## Remaining limitations

These items require an environment with human-operated assistive technology or production administration and are not silently treated as passed:

- VoiceOver/NVDA announcement quality still needs human confirmation; markup and update behavior are covered by source checks.
- The 2026-08-24 Chromium keyboard matrix confirmed consent, privacy-settings
  focus, search focus/restoration, live-region text updates, theme attributes,
  mobile navigation state, and the Universe no-JavaScript fallback. VoiceOver
  and NVDA spoken output remains **unknown**, not a pass by assumption. See
  `assets/docs/accessibility-audit-2026-08-16.md`, section 5.
- GitHub Pages’ repository environment and custom-domain DNS status require checking in the GitHub repository settings after the workflow runs.
- External third-party links are syntax-checked but not all are fetched during CI, because availability and rate limits are outside the site’s control.

## Local release commands

```bash
python3 scripts/validate-site.py
python3 scripts/check-links.py
python3 -m pytest
python3 scripts/build-search-index.py --check
python3 scripts/audit-site.py --quiet
node scripts/responsive-qa.mjs
python3 scripts/prepare-pages-artifact.py --output /tmp/askjamie-pages
```
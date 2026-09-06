# Maintained universe maps

Canonical package: `OKHP3/skillz/mermaid/okhp3-universe-map`, version 0.1.1.
Installed copy: `.agents/skills/okhp3-universe-map/SKILL.md`.
Site-owned configuration: `universe-map.config.json`.

## Refresh and verify

```text
py -3 -X utf8 scripts/build-search-index.py
py -3 -X utf8 scripts/build-search-index.py --check
py -3 -X utf8 scripts/sync-universe-map.py --check
```

Use `python3` on Linux/macOS. An ordinary index rebuild also refreshes the
universe page and `assets/data/universe-map.json`. The map script changes only
its marked block, keeping the authored page shell intact. Generated navigation
is excluded from search extraction. Two successive builds must be identical.
The installed package remains byte-identical to its canonical Skillz source.

The main validation workflow regenerates before validation on pushes, manual
runs, and a daily schedule. Deployment uses that validated artifact. Invalid
input fails the workflow and leaves the previous deployment available. Generated
release artifacts need no bot commit or language-model call. GitHub Actions must
remain enabled for unattended refreshes.

The overview links directly to the other two sites' universe pages. Each site
owns its inventory, so sibling changes require no copied snapshots or peer
refresh credentials. AskJamie details include all indexed pages, split into
six-child groups with ordinary links beneath each diagram. Strict Mermaid is
retained; validated local outline links supply SVG navigation after rendering.

## Lifecycle and historical material

Published page means only that a page is indexed. Explicit lifecycle overlays
remain available in configuration. No speculative project status was inferred.
`universe-map-legacy-2026-09-06.mmd` preserves the original hand-written map,
including concepts whose present status is unconfirmed. This archive is not
part of the public Pages artifact.

`assets/audit/universe-map/` retains portable generator output for inspection.
Its rendering status describes the generator, which does not run a browser.
The page adapter is separately tested by `tests/test_universe_map.spec.mjs`.
`assets/audit/universe-map-browser/` holds local visual evidence.

The pre-existing duplicate janitor skill's three files matched the active copy
by SHA-256. They were moved intact to `.agents/skill-archives/` to unblock the
local catalog; no content was discarded.

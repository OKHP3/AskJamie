# W04 Found-Ry Discovery

Date: 2026-09-07
Branch: `codex/w04-foundry-discovery`
Base SHA: `e9902c5358506252ae0aba8b805c26f7f9d18924`
Tracker: https://github.com/OKHP3/AskJamie/issues/30#issuecomment-5577411259

## Scope

Allowed write paths:

- `assets/docs/delegates/w04-discovery.md`
- `tests/test_foundry_discovery.py`

## What I verified

- Homepage links to `/found-ry/`.
- `how-askjamie-works/index.html` links to `/found-ry/`.
- `llms.txt` lists `https://askjamie.bot/found-ry/`.
- `sitemap.xml` lists `https://askjamie.bot/found-ry/`.
- `found-ry/index.html` exposes the canonical URL for `/found-ry/`.
- `scripts/build-search-index.py` includes the Found-Ry route in the search inventory.
- `assets/data/search-index.json` includes `/found-ry/`.

## Result

The public discoverability surface is already present. The new regression test locks those checks together so a future edit cannot remove Found-Ry from one surface without being caught.

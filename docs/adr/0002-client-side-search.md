# ADR-0002: Client-Side Search with Pre-Built Index

## Status

Accepted

## Date

2026-07-13

## Context

The site needed a search feature so visitors can find content across pages.
Given the static architecture (ADR-0001), server-side search was not an option
without introducing a backend or a third-party search service.

## Decision Drivers

- Must work within the static hosting constraint (no server runtime)
- Must not require a paid third-party service
- Must be fast enough for a site of roughly 25 pages
- Search index must stay accurate as pages are added or updated
- No client-side framework dependency

## Considered Options

### Option 1: Algolia or similar hosted search

Pros: Excellent UX, advanced ranking.

Cons: Paid service, external dependency, API key exposure risk, vendor lock-in.

### Option 2: Pagefind (post-build static search)

Pros: Automatic index generation, good UX, no backend needed.

Cons: Requires a build step, adds a Node.js toolchain dependency.

### Option 3: Pre-built JSON index plus custom browser search

Pros: Zero runtime dependencies, full control over relevance, index rebuilt
by a single Python script, search logic lives in `assets/js/app.js`.

Cons: Hand-written ranking logic, index must be explicitly regenerated after
content changes.

## Decision

We will use a **pre-built JSON index** (`assets/data/search-index.json`) generated
by `scripts/build-search-index.py`, with a custom client-side search implementation
in `assets/js/app.js`.

The index is rebuilt manually or by the CI workflow after content changes.

## Consequences

### Positive

- No external dependencies or API keys
- Index generation is a single, auditable Python script
- Works offline once the page is loaded

### Negative

- Developers must remember to rebuild the index after content changes
- Ranking is basic (title, headings, body text scoring)

### Risks

- Stale index if content changes without a rebuild (mitigation: CI validates
  that the index is not older than the HTML files it covers)

## Related Decisions

- ADR-0001: Static HTML Architecture (prerequisite constraint)

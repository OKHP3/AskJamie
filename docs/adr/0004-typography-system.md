# ADR-0004: Google Fonts Typography System

## Status

Accepted

## Date

2026-07-13

## Context

The AskJamie brand identity calls for a warm, readable, mid-century helpdesk feel.
A typography system needed to be chosen that matched this identity, loaded reliably
across devices, and did not require self-hosting font files.

## Decision Drivers

- Must reflect the AskJamie brand: calm, readable, slightly personal
- Must load reliably without adding font files to the repository
- Must remain readable at body sizes down to 14px
- Must not introduce Flash of Invisible Text (FOIT) on slow connections

## Considered Options

### Option 1: System font stack only

Pros: Zero load, perfect rendering on all platforms.

Cons: No brand differentiation; -apple-system and Segoe UI do not express the
helpdesk warmth the brand requires.

### Option 2: Google Fonts (hosted by Google CDN)

Pros: Wide selection, reliable CDN, no repository bloat, familiar integration
pattern for static sites.

Cons: External dependency; Google receives a request per page load (privacy
consideration).

### Option 3: Self-hosted fonts (WOFF2 files in assets/)

Pros: No external dependency, works offline, full privacy.

Cons: Repository size increase, FOIT risk on slow connections without careful
font-display management, added maintenance for font updates.

## Decision

We will use **Google Fonts** with the following role assignments:

| Role | Family | Rationale |
|------|--------|-----------|
| Heading | Baloo 2 | Rounded, warm, friendly; reads like a confident helper |
| Body | Open Sans | Highly legible, neutral, comfortable at reading sizes |
| Accent | Kalam | Handwritten feel; used sparingly for personal notes |
| Monospace | JetBrains Mono | Technical clarity for code and structured output |

## Consequences

### Positive

- Distinctive brand identity achievable without font files in the repository
- All four families are reliably cached by Google's CDN for repeat visitors

### Negative

- A Google Fonts request is issued on first page load, which reveals the visitor's
  IP to Google
- If Google Fonts CDN is unavailable, pages fall back to system fonts

### Risks

- Family discontinuation by Google (low risk; all four families are actively
  maintained as of 2026)
- Mitigation: fallback stacks are declared in `assets/css/theme.css` for every role

## Related Decisions

- ADR-0001: Static HTML Architecture

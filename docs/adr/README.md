# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the AskJamie repository.

ADRs document significant decisions about architecture, tooling, and design so future contributors understand why choices were made, not just what was chosen.

## Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-static-html-architecture.md) | Static HTML Architecture | Accepted | 2026-07-13 |
| [0002](0002-client-side-search.md) | Client-Side Search with Pre-Built Index | Accepted | 2026-07-13 |
| [0003](0003-security-headers-csp.md) | Security Headers and CSP Baseline | Accepted | 2026-07-13 |
| [0004](0004-typography-system.md) | Google Fonts Typography System | Accepted | 2026-07-13 |

## When to Write an ADR

Write an ADR when:
- Choosing a framework, language, or major library
- Selecting a deployment or hosting strategy
- Establishing a security or performance baseline
- Deciding on a content structure that will be hard to reverse

Skip an ADR for bug fixes, minor content changes, and routine maintenance.

## ADR Status Values

- **Proposed**: Under discussion
- **Accepted**: Decision made and implemented
- **Deprecated**: No longer relevant, but preserved for history
- **Superseded**: Replaced by a newer ADR (link to the replacement)

## Creating a New ADR

1. Copy `template.md` to `NNNN-short-title.md` (four-digit number, lowercase kebab-case)
2. Fill in all sections
3. Add a row to the index table above

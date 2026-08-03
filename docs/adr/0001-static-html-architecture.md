# ADR-0001: Static HTML Architecture

## Status

Accepted

## Date

2026-07-13

## Context

AskJamie is a public marketing and documentation site for an AI helpdesk persona.
The site presents a Lens System portfolio, case studies, and static informational pages.
A hosting and architecture decision was needed before the first pages were published.

## Decision Drivers

- Must be deployable as static files with no server-side runtime
- Must load quickly on low-end devices and slow connections
- Must be maintainable without a build pipeline or Node.js dependency
- Must be inspectable by AI crawlers and human readers without JavaScript
- Content changes must be straightforward without framework churn

## Considered Options

### Option 1: Vanilla HTML/CSS/JS (static files)

Pros: Zero build step, no dependency updates, full control over every byte, instant
hosting on any CDN or static host, maximum inspectability.

Cons: No component reuse without manual copy-paste, no hot-reload, no bundler
for asset fingerprinting.

### Option 2: React/Next.js

Pros: Component reuse, modern tooling, large ecosystem.

Cons: Build pipeline required, Node.js version management, ongoing dependency
updates, harder for crawlers to index without additional configuration, more
infrastructure for a primarily informational site.

### Option 3: Eleventy or Hugo (static site generator)

Pros: Templating, content collections, no client-side framework overhead.

Cons: Build step required, additional tooling to maintain, templating languages
add cognitive overhead for a small project.

## Decision

We will use **vanilla HTML5, CSS custom properties, and minimal browser JavaScript**
served as static files directly from the repository root.

## Consequences

### Positive

- Zero build pipeline: deploy by pushing to the repository
- No dependency vulnerabilities from bundler or framework packages
- Every page is a self-contained, inspectable HTML file
- Works in any static hosting environment including GitHub Pages and CDNs

### Negative

- HTML structure is duplicated across pages (headers, footers, navigation)
- No automatic asset fingerprinting; cache busting requires manual version bumps
- Adding interactive features requires more hand-written JavaScript

### Risks

- Drift between duplicate page structures (mitigation: developer templates in
  `assets/templates/` and a site validator script)

## Related Decisions

- ADR-0002: Client-Side Search with Pre-Built Index
- ADR-0003: Security Headers and CSP Baseline

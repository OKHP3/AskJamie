# ADR-0003: Security Headers and CSP Baseline

## Status

Accepted

## Date

2026-07-13

## Context

A public-facing site should protect visitors from cross-site scripting, clickjacking,
and information leakage even without a backend to set HTTP headers. The static hosting
environment supports a `_headers` file at the repository root that the CDN edge applies
to every response.

## Decision Drivers

- Must prevent clickjacking and content injection without a server runtime
- Must work with the static hosting edge (`_headers` file support)
- Must allow Google Fonts and Google Analytics without
  loosening the policy broadly
- Must not break existing page functionality

## Considered Options

### Option 1: No custom headers (browser defaults only)

Pros: Zero configuration.

Cons: No clickjacking protection, no referrer control, no CSP.

### Option 2: `_headers` file with broad CSP

Pros: Easy to configure, low risk of breakage.

Cons: Broad policies (e.g., `default-src *`) provide little real protection.

### Option 3: `_headers` file with targeted CSP plus per-page meta tags

Pros: Defense in depth. Edge headers cover all pages; per-page CSP meta tags
provide a secondary layer and survive hosting migrations.

Cons: Maintenance burden when new external resources are added.

## Decision

We will use **Option 3**: a `_headers` file at the repository root for edge-level
headers, plus per-page `<meta http-equiv="Content-Security-Policy">` tags in every
HTML file for resilience.

The policy explicitly allows: self, Google Fonts, and Google Analytics. Mermaid
is served locally from the repository. Ko-fi remains an approved outbound
support destination.

## Consequences

### Positive

- Clickjacking blocked via `frame-ancestors 'self'`
- Referrer policy limits information leakage on external link clicks
- CSP violations surface in browser console during development

### Negative

- Adding any new external resource (font, CDN script, embed) requires a policy update
  in both the `_headers` file and each affected HTML page

### Risks

- CSP meta tag on page can be overridden by an HTTP header with a stricter policy
  (acceptable: stricter is safer)
- Template pages (`assets/templates/`) carry placeholder CSP that must be updated
  when the policy changes

## Related Decisions

- ADR-0001: Static HTML Architecture

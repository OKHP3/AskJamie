# ADR-0007: Plain-Language Brand Term Enforcement

## Status

Accepted

## Date

2026-08-22

## Context

AskJamie pages introduce brand and architecture terms such as BrandGuard,
OKHP³, OverKill Hill P³, and Lens System. Repeating a term without a nearby
explanation makes the site harder for first-time visitors and can make case
study copy look like internal shorthand. Manual review alone does not
reliably catch this regression across 26 public pages.

## Decision Drivers

- Keep visitor-facing explanations understandable without prior context.
- Enforce the rule consistently across all public HTML pages.
- Avoid false positives from shared navigation, banners, and controls.
- Fail validation with enough page and term detail to correct the copy.
- Keep the rule in the existing zero-dependency static validation toolchain.

## Considered Options

### Option 1: Validator checks the first meaningful explanatory occurrence

Pros: Creates a repeatable release gate while excluding shared chrome and
non-explanatory labels. Cons: The heuristic cannot understand every nuance of
natural language.

### Option 2: Editorial review only

Pros: Allows human interpretation. Cons: It is inconsistent and easy to skip
when many pages change.

### Option 3: Require a glossary page and link every term

Pros: Centralizes definitions. Cons: It adds navigation friction and does not
ensure that a page explains a term in its own context.

## Decision

We will use **Option 1**. `validate-site.py` checks the first meaningful
visitor-facing explanatory occurrence of the governed terms on each public
page. Shared navigation, specials banners, decorative or hidden content, and
link or button-only labels are excluded. A missing explanation is a validation
error, while short pages that do not contain enough prose are handled by the
validator's existing minimum-content rules.

## Consequences

### Positive

- New pages receive an automated plain-language regression check.
- Validation output identifies the page and term that needs attention.
- The rule protects clarity without requiring a new runtime or content system.

### Negative

- The heuristic depends on HTML structure and explanatory-copy patterns.
- Legitimate unusual prose may need an explicit validator adjustment.

### Risks

- A shared component change can affect many pages at once. Mitigation: run the
  full site validator and review its exact errors before release.
- The term list can lag behind the vocabulary used by the project. Mitigation:
  update the decision record and validator together when governed terms change.

## Related Decisions

- ADR-0001: Static HTML Architecture
- ADR-0002: Client-Side Search with Pre-Built Index
# ADR-0005: Dark and Light Mode Toggle

## Status

Accepted

## Date

2026-08-22

## Context

AskJamie has a paper-first light visual system, but some visitors need a dark
presentation for comfort or preference. The site is a static HTML site with
shared browser JavaScript and no server-side session state. The choice must
work across page loads without making dark mode the default.

## Decision Drivers

- Respect the AskJamie light-first brand contract.
- Preserve the visitor's preference across pages and reloads.
- Avoid a framework, backend, or new dependency.
- Keep the control understandable and keyboard accessible.
- Apply the preference early enough to avoid a distracting theme flash.

## Considered Options

### Option 1: Shared client-side toggle with local storage

Pros: Fits the static architecture, persists locally, and can be shared by all
pages through the existing browser script. Cons: The preference is device and
browser specific, and JavaScript is required to change the theme.

### Option 2: CSS-only system preference

Pros: Requires no interaction code and follows the operating system. Cons:
Visitors cannot choose a site preference, and the site would not honor the
light-first default consistently for every visitor.

### Option 3: Server-managed account preference

Pros: Could synchronize preferences across devices. Cons: Requires a backend,
accounts, and data handling that are outside the site architecture.

## Decision

We will use **Option 1**, a shared browser toggle that stores the selected
theme locally and applies it through the document's theme attribute. Light mode
remains the default when no preference has been saved. The toggle is exposed
on AskJamie pages and omitted from pages intentionally designed as light-only.

## Consequences

### Positive

- Visitors can choose light or dark mode without an account.
- The preference persists across AskJamie pages and reloads.
- The implementation remains compatible with the static HTML architecture.

### Negative

- The preference does not follow a visitor to another browser or device.
- JavaScript-disabled visitors receive the light presentation.

### Risks

- A new page can omit the shared control or theme initialization. Mitigation:
  preserve the page-shell checklist and test representative pages.
- A future color change can reduce contrast in one theme. Mitigation: run the
  contrast and site accessibility checks after theme changes.

## Related Decisions

- ADR-0001: Static HTML Architecture
- ADR-0004: Google Fonts Typography System
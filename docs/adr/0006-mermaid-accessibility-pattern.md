# ADR-0006: Mermaid Diagram Accessibility Pattern

## Status

Accepted

## Date

2026-08-22

## Context

The Universe page uses Mermaid to render a visual ecosystem map in the
browser. The generated SVG is useful for sighted visitors but is not a
sufficient text alternative and can introduce generated links into keyboard
navigation. The page must remain understandable when JavaScript is disabled.

## Decision Drivers

- Give screen-reader users a meaningful description of the diagram.
- Keep generated SVG decoration out of the normal reading and tab order.
- Preserve useful Mermaid links for visitors who can use the visual diagram.
- Provide a no-JavaScript fallback without duplicating the full diagram.
- Avoid modifying generated Mermaid markup after each render.

## Considered Options

### Option 1: Hidden generated SVG plus caption and no-JavaScript fallback

Pros: Keeps the visual map available while providing a stable text
description, keyboard behavior, and a fallback. Cons: The text description
must be maintained when the diagram's meaning changes.

### Option 2: Treat the SVG as the only accessible representation

Pros: Requires less authored content. Cons: Generated SVG structure and links
are not a reliable explanation for assistive technology users.

### Option 3: Replace Mermaid with a hand-authored accessible SVG

Pros: Provides direct control over every SVG node. Cons: Loses Mermaid's
maintainability and makes a complex ecosystem map harder to update.

## Decision

We will use **Option 1**. The diagram container includes an `sr-only` caption,
the generated Mermaid SVG is marked `aria-hidden="true"` and its generated
anchors receive `tabindex="-1"`, and a concise `noscript` ecosystem description
provides a JavaScript-disabled fallback. The visual diagram remains linked for
visitors using the rendered map.

## Consequences

### Positive

- The page communicates the diagram's purpose and major relationships without
  requiring visual interpretation.
- Generated links do not create unexpected keyboard stops.
- The fallback keeps the page useful when the external Mermaid module fails or
  JavaScript is disabled.

### Negative

- The authored caption and fallback can become stale if the map changes.
- The generated SVG cannot be treated as the primary semantic content.

### Risks

- Mermaid can change generated markup between versions. Mitigation: keep the
  accessibility behavior in runtime smoke tests and inspect the generated
  anchor focus behavior when upgrading Mermaid.
- A future diagram edit may not update the text alternative. Mitigation: treat
  the caption and fallback as part of the diagram change review.

## Related Decisions

- ADR-0001: Static HTML Architecture
- ADR-0003: Security Headers and CSP Baseline
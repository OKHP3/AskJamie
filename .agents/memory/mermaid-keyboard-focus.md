---
name: Mermaid keyboard focus
description: Browser behavior to account for when Mermaid diagrams contain generated SVG links.
---

Mermaid-generated SVG anchors can remain in Chromium's sequential keyboard focus order even when their containing diagram has `aria-hidden="true"`.

**Why:** `aria-hidden` removes content from the accessibility tree, but it is not a keyboard-focus mechanism for SVG anchors.

**How to apply:** For decorative or orientation-only Mermaid diagrams, keep the diagram wrapper `aria-hidden="true"` and assign generated SVG anchors `tabindex="-1"` after rendering. Keep any separate, user-facing explanatory or referral link outside the hidden wrapper.
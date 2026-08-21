---
name: Plain-language term validation
description: First-use jargon checks should inspect explanatory prose and track excluded HTML elements with a real element stack.
---

The first-use jargon rule applies to explanatory prose blocks, not navigation, breadcrumbs, headings, shared announcements, decorative diagrams, or link/button-only labels. Class-based exclusions must be paired with matching element-stack bookkeeping so they cannot hide the rest of a page.

**Why:** AskJamie pages intentionally repeat brand and product labels in orientation UI and case-study headings; treating every label as explanatory copy created false failures, while a one-way exclusion depth could silently skip later content.

**How to apply:** Keep the flagged-term list and definition patterns explicit, add focused synthetic tests for excluded UI and missing definitions, and verify the full public-page validator after copy changes.
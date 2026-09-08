---
name: Merge marker false positives
description: Conflict-resolution marker checks can misclassify decorative comment separators.
---

Some merge-resolution validators scan for the raw `=======` sequence rather than requiring a standalone conflict-marker line. Decorative comment rules made of repeated equals signs can therefore block an otherwise clean resolution.

**Why:** The resolved file had no `<<<<<<<` or `>>>>>>>` markers, but the resolver still rejected it because unrelated comment separators contained the equals sequence.

**How to apply:** When a clean resolution is rejected for remaining markers, scan the entire file for raw marker substrings, including comments. If decorative separators are the only match, replace them with an equivalent non-equals rule before retrying; do not alter functional content.
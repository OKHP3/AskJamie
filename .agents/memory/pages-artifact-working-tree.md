---
name: Pages artifact working tree
description: The static Pages artifact directory is tracked and artifact preparation can leave it looking disposable.
---

The Pages publication tree is a tracked repository surface, not disposable workspace output. Running artifact preparation can make `dist-pages/` and its manifest look like generated scratch output, but deleting them produces a large tracked deletion.

**Why:** The first cleanup attempt treated the artifact output as disposable and had to restore hundreds of tracked files before synchronization could continue safely.

**How to apply:** Before removing any artifact-preparation output, check `git ls-files` and the current commit. Restore tracked artifact files from `HEAD` rather than deleting them; only remove genuinely untracked output.
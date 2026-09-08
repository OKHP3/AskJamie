---
name: Branch cleanup recovery refs
description: Preserve approved local branch tips under dated recovery refs before deletion while leaving existing archive refs untouched.
---

For approved local branch cleanup, create a dated `refs/recovery/` ref for each exact tip before deleting the local branch. Snapshot all pre-existing refs and verify afterward that only the approved local heads changed.

**Why:** A local branch can be removed safely without discarding recovery, while an explicit before/after comparison catches accidental changes to main, remotes, archive refs, stashes, or other retained history.

**How to apply:** Use this pattern for future exact branch-deletion batches; never prune objects, stashes, archive refs, or remote state as part of local-only cleanup.
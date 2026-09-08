---
name: Branch cleanup recovery refs
description: Preserve approved local branch tips under dated recovery refs before deletion while leaving existing archive refs untouched.
---

For approved local branch cleanup, create a dated `refs/recovery/` ref for each exact tip before deleting the local branch. Snapshot all pre-existing refs and verify afterward that only the approved local heads changed.

**Why:** A local branch can be removed safely without discarding recovery, while an explicit before/after comparison catches accidental changes to main, remotes, archive refs, stashes, or other retained history.

**How to apply:** Use this pattern for future exact branch-deletion batches; first enumerate every local head and compare exact names with the written ledger because task merges can create heads the ledger does not yet mention. Flag unmentioned heads rather than inferring a disposition. Never prune objects, stashes, archive refs, or remote state as part of local-only cleanup.
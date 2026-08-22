---
name: Portable skill package integrity
description: Referenced resources must be present and independently resolvable before portability can be evaluated.
---

A portable Agent Skill is not self-contained when its instructions reference a
missing schema, checklist, or protocol file. Treat unresolved relative
references as a package defect and record the defect separately from client
execution evidence.

**Why:** A second client cannot reliably follow or grade a procedure if a
referenced resource is absent, even when the core instructions appear clear.

**How to apply:** Before a portability run, resolve every relative reference
from SKILL.md, then run the procedure in a disposable copy and keep
cross-client, local, CI, and hosted evidence classified separately.
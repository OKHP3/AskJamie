# Catalog and ignored-cruft disposition

Date: September 5, 2026.

## Duplicate janitor package

The canonical package and the space-suffixed package are byte-identical for
`SKILL.md`, `references/naming-conventions.md`, and `scripts/audit-repo.py`.
The duplicate is tracked in Git and has historical provenance at commit
`8deb400`. No copy was deleted in this pass. The full skill catalog remains
blocked until the owner approves which package path is canonical and whether
the duplicate should be removed while retaining the commit as recovery
evidence.

## `.DS_Store` findings

The assessment reports eight ignored macOS metadata paths in the saved clone.
No `.DS_Store` path is tracked in this PM checkout, and no broad cleanup was
attempted. Before any removal, enumerate exact paths in the affected clone,
confirm they are disposable metadata rather than owner material, record the
before-state, move them to recoverable quarantine, rerun the canonical audit,
and retain the quarantine manifest. A clean isolated checkout is not evidence
that the saved clone is clean.

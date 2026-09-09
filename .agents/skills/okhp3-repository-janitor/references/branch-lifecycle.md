# Branch lifecycle rules

Use these categories after refreshing the remote and checking GitHub pull-request state.

| Evidence | Decision | Action |
|---|---|---|
| Dirty checkout, stash, local-only commit, or unreachable commit | Preserve | Do not merge or prune; create or retain a recovery ref and review the content. |
| Branch is not reachable from `origin/main` and has an open PR | Review | Keep the branch and PR. Merge only after its purpose, checks, and target are reviewed. |
| Branch is reachable from `origin/main` and its PR is merged | Prune candidate | Verify it is not a deployment branch, then delete the remote branch and local counterpart in the same recorded batch. |
| Branch has a closed, unmerged PR and a newer open/merged branch supersedes the same work | Archive then prune candidate | Preserve a dated local archive ref if needed, document the superseding PR, then remove only after confirmation. |
| Branch has a closed, unmerged PR without a clear successor | Keep for decision | Compare files and commits to `origin/main`; ask whether to revive, archive, or delete. |
| Dependabot branch with an open PR | Review as dependency work | Keep it until the update is merged, closed, or superseded. Never delete solely because it is bot-created. |
| `gh-pages`, deployment, release, or explicitly protected branch | Retain | Do not apply ordinary feature-branch cleanup rules. |

Before any deletion, record the full branch name, its tip SHA, PR number/state, reachability result, and recovery ref. Refresh after the merge or deletion and verify the expected remote state.

## Local deletion recovery guard

For local-only branch deletion, run the one-Repl janitor's recovery snapshot
before the operation and its verification afterward:

```bash
python3 .agents/skills/okhp3-replit-repl-janitor/scripts/audit-repo.py \
  --root . --snapshot-recovery /tmp/janitor-recovery.json
# Create a dated refs/recovery/ ref at the approved tip, then delete only the
# exact approved local branch with the normal Git command.
python3 .agents/skills/okhp3-replit-repl-janitor/scripts/audit-repo.py \
  --root . --verify-recovery /tmp/janitor-recovery.json \
  --approve-local-deletion '<exact-local-branch>'
```

The snapshot records all refs, stash entries, and objects reachable from refs.
Verification is read-only and fails unless the only removed ref is the exact
approved local branch, its tip has a recovery ref, all other refs and stashes
are unchanged, and no previously reachable object disappeared. It never
authorizes deletion by itself.

## Retention-ledger consistency gate

Before proposing local-branch cleanup, compare every non-current local branch
with the current written decision ledger. The read-only audit must report:

- **missing branches** — local refs with no decision or explicit hold;
- **tip-SHA drift** — a decision row whose recorded tip no longer matches the
  local branch;
- **stale ledger rows** — decisions or holds for refs no longer present locally.

Any of these findings blocks cleanup planning until the ledger is refreshed.
This gate does not authorize deletion, pruning, or recovery-ref changes.

# Branch lifecycle rules

Use these categories after refreshing the remote and checking GitHub pull-request state.
The single-checkout audit performs that refresh non-interactively: it disables
Git terminal prompts, runs SSH in batch mode, and closes stdin. If refresh is
unavailable, it still prints local branch, naming, and detritus evidence but
reports `remote_refresh.classification: remote-unavailable` and exits nonzero.
Treat that classification as a safety block: do not plan cleanup from stale
remote-tracking refs.

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

### Repeatable hosted-branch check

The one-Repl audit can record hosted evidence without changing the checkout.
Pass the exact branch name once for each provider or remote; do not rely on a
similarly named local branch to identify the hosted ref:

```bash
python3 .agents/skills/okhp3-replit-repl-janitor/scripts/audit-repo.py \
  --root . --base origin/main \
  --hosted-branch origin=feature/example \
  --hosted-branch subrepl-abc123=feature/example
```

`--hosted-ref` is an alias for `--hosted-branch`, and `PROVIDER:BRANCH` is
accepted as a shorthand. Each request produces its own `hosted_lifecycle`
entry with the provider, exact `refs/heads/...` ref, tip when present, and
the classification `present`, `missing`, or `inaccessible`. A missing ref is
not the same as an inaccessible remote: both set `deletion_blocked`, but they
require different recovery actions.

For a GitHub remote, the audit also records branch protection, deployments,
and all matching open/closed pull requests when the `gh` CLI is installed and
authenticated. Other providers still receive explicit unknown evidence rather
than an inferred clean result. Unknown hosted evidence, protected branches,
deployment refs, open pull requests, and closed unmerged pull requests remain
deletion holds. The report is read-only; it never deletes a ref or PR.

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
with the current written decision ledger. The audit selects the active ledger
deliberately: it uses `.agents/branch-decision-ledger.md` when that stable path
exists, otherwise it uses the newest valid
`.agents/branch-decision-ledger-YYYY-MM-DD.md` by ISO date. A historical audit
must pass `--decision-ledger <path>` explicitly; that override always wins over
active-ledger discovery. The read-only audit must report:

- **missing branches** — local refs with no decision or explicit hold;
- **tip-SHA drift** — a decision row whose recorded tip no longer matches the
  local branch;
- **stale ledger rows** — decisions or holds for refs no longer present locally.

Any of these findings blocks cleanup planning until the ledger is refreshed.
This gate does not authorize deletion, pruning, or recovery-ref changes.

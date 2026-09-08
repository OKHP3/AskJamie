# Local branch decision ledger

**Recorded:** 2026-09-07
**Baseline:** `origin/main` at `e9902c5358506252ae0aba8b805c26f7f9d18924`
**Current checkout:** `integration/mobile-performance-reconcile`
**Scope:** The 19 non-current, non-merged local branches remaining after excluding the current checkout, the four branches already reachable from `origin/main`, and the three active mobile-performance branches covered by the existing performance task.

## Decision rules

- **Keep** means the branch contains patch-unique or active work that must remain available for revival or continued work.
- **Archive** means the branch's work is represented by `origin/main` or by the current active branch. Retain the branch and its exact tip for now; it is not an instruction to delete it.
- **Owner-approved delete** is not used in this ledger because no explicit owner approval to delete any of these local branches is recorded.
- A `subrepl-*` or `replit-agent` name is treated as a hint, not as evidence that the branch is disposable.

## Evidence

- `git fetch origin` completed before comparison.
- `git cherry -v origin/main <branch>` was used to distinguish patch-unique commits from commits already represented in `origin/main`.
- `git diff --shortstat origin/main...<branch>` was used to confirm the file-level scope.
- The configured GitHub connection was queried for all pull requests in `OKHP3/askjamie`; no PR had any of the local branch names below as its head, and `origin` exposes only `main`.
- No branch, remote ref, stash, or unreachable object was deleted or pruned.

## Branch decisions

| Branch | Decision | Tip SHA | Evidence and rationale |
|---|---|---|---|
| `replit-agent` | **keep** | `dc1ef14a392793667b6a9df839d6c33be2254a31` | Has 24 patch-unique commits relative to `origin/main`, including the latest audit-report work. Its generated name is not sufficient grounds for deletion; retain for review or revival. |
| `subrepl-18mu80ad` | **archive** | `d9b928a4d2273e2167b56dda1806b0505bb280b8` | Its keyboard-order commit is patch-equivalent to `origin/main`; the six-file tree difference is already represented upstream. Retain the exact tip, but no revival is currently indicated. |
| `subrepl-46ay7r19` | **archive** | `2097f9e4e8abf17cb72fe42763cb60a7021d1f70` | Its public-site audit hardening commit is patch-equivalent to `origin/main`. Preserve the tip as historical recovery, not as an unreviewed delete target. |
| `subrepl-4idi6all` | **archive** | `eba57b9f6076d5207d9e69c82815bac9ce2c7ab8` | Its keyboard-focus evidence update is patch-equivalent to `origin/main`; the remaining difference is documentation only. |
| `subrepl-8pt4s2w4` | **archive** | `7dcf08623388f8365c4146ded59835beb873def9` | Its 400% reflow and overflow verification is patch-equivalent to `origin/main`; retain as evidence history. |
| `subrepl-ab3sqx8f` | **archive** | `c9f78e8a3d6675ae6c17db4c30aa02c278fb84ac` | All 17 commits are patch-equivalent to `origin/main`, including release-gate and screen-reader evidence. This is a redundant release snapshot, not disposable-by-name. |
| `subrepl-f4jb3f1a` | **archive** | `eeb7b7b87be985ac2059985188bafd05baf90d5f` | Its brand-terms content is patch-equivalent to `origin/main`; preserve the snapshot for provenance. |
| `subrepl-h4tlbpdo` | **archive** | `23bb4bb790c977745f03f28359ce84da822981ec` | All 13 commits are patch-equivalent to `origin/main`, including spoken-output evidence. It is superseded by landed work. |
| `subrepl-ili4a5c9` | **keep** | `54df8979cebe558e3da9da9ac60157edc0a7d230` | Contains two patch-unique commits: the FK-scoring memory correction and plain-language updates. Preserve because the work is not represented by `origin/main`. |
| `subrepl-j0iqy3mq` | **archive** | `8d3fd352e82af963227858fde999d8b8400e9f22` | Its static-site release skill evaluation evidence is patch-equivalent to `origin/main`; retain as a historical evaluation snapshot. |
| `subrepl-j940c6i6` | **keep** | `905d38060dc91ec54802a8572c5e087b524bb890` | Contains one patch-unique commit packaging the static-site release validation skill. Preserve because the packaged skill work is not fully represented in `origin/main`. |
| `subrepl-jbcjwvjz` | **archive** | `1ddd4d0a00c456633a93d3ffc1772d287a42142c` | All 16 commits are patch-equivalent to `origin/main`, including the spoken-accessibility evidence boundary. It is a redundant evidence snapshot. |
| `subrepl-kvueapkn` | **keep** | `6a5a8b40e132f732cbfd3f21050efd5b218594e2` | Its tree is identical to the checked-out `integration/mobile-performance-reconcile` branch and contains active mobile-performance work plus recovery handling. Keep until the performance task and branch-recovery follow-ups are resolved. |
| `subrepl-paxtu6hz` | **archive** | `6dd08e411c6d11f7b1f05762151a8cf0428dd6b4` | All six commits are patch-equivalent to `origin/main`, including Lighthouse evidence. Retain as a dated performance-history snapshot. |
| `subrepl-psjy4q92` | **archive** | `12c052530c310648c6814dc179d634738cc0f86d` | Its project-truth and release-evidence commit is patch-equivalent to `origin/main`; no unrepresented code was found. |
| `subrepl-q8qfdbks` | **archive** | `0e51a3b404f7194130fa4423dd1a4cf813e87051` | All seven commits are patch-equivalent to `origin/main`, including browser-regression and Lighthouse checks. It is superseded release work. |
| `subrepl-qk4xg55u` | **archive** | `62d5b5b096c5e9441064cf7dba30a73cd3ae3532` | Its public AskJamie Lens completion commit is patch-equivalent to `origin/main`; preserve for provenance only. |
| `subrepl-r42jccji` | **archive** | `7f2c5792b033dc21ce40b89d0ffe52f48b930d06` | Its search announcement fix is patch-equivalent to `origin/main`; the work has already landed elsewhere. |
| `subrepl-xdx2eorg` | **archive** | `8bd136e8388b3a3397c46539af5da6b67080fb86` | All three commits are patch-equivalent to `origin/main`, covering documentation and prose-validation work. Retain as historical recovery. |

## Explicit exclusions and holds

These refs are not part of the 19-branch decision set:

- `integration/mobile-performance-reconcile` — current checkout; never a cleanup candidate.
- `main`, `subrepl-imiwej7r`, and `subrepl-s9r7crbb` — active mobile-performance work covered by the existing performance task; keep unchanged.
- `subrepl-1aunpswo`, `subrepl-4415rcr0`, `subrepl-4hm3zoon`, and `subrepl-gkf1bczs` — already reachable from `origin/main`; no action is taken in this review.

## Next cleanup gate

This ledger records decisions, not deletion approval. A later cleanup may consider exact archive refs or local-branch deletion only after the owner approves the named branches, a dated recovery plan is recorded, and the pre/post ref snapshot is verified.
# Skill catalog cleanup record

Date: September 5, 2026. Scope: the one redundant, tracked repository-local
skill directory `.agents/skills/okhp3-repl-repo-janitor copy/`.

## Before-state verification

The directory contained exactly three files. A recursive `diff -ru` against
the canonical `.agents/skills/okhp3-repl-repo-janitor/` directory produced no
differences. SHA-256 values matched pairwise:

| Relative file | SHA-256 |
| --- | --- |
| `SKILL.md` | `801d64be7c66e3019fe9a1cbd20529aa62043666a45bed3c07639549d4047f0d` |
| `references/naming-conventions.md` | `d26cdc014f44e115d8a7687d73bf35dfb7fd44a88a5f21be986704a635fa7117` |
| `scripts/audit-repo.py` | `778a142d351ffb72b9f9d7ad645b9a2e8266a7aca9090e09ffb28e609055cfb1` |

The canonical `SKILL.md` frontmatter name is
`okhp3-repl-repo-janitor`, which matches its directory. The suffixed duplicate
has the same frontmatter name but cannot match its own directory, causing the
cataloger duplicate-name and directory-name validation errors. No repository
reference uses the space-suffixed path. Commit
`8deb4007902a2d1d77b6c7877b7aae9010e8ecaf` records the duplicate's original
addition and is retained as Git recovery evidence.

## Authorized action and recovery

Remove only the proven redundant space-suffixed directory with Git's tracked
deletion. The deletion commit and commit `8deb4007902a2d1d77b6c7877b7aae9010e8ecaf`
preserve recoverable history. If restoration is required after the deletion
commit is available, use this exact command from the repository root:

```bash
git restore --source=8deb4007902a2d1d77b6c7877b7aae9010e8ecaf -- \
  '.agents/skills/okhp3-repl-repo-janitor copy'
```

The ignored `.DS_Store` files reported in the saved clone are outside this
isolated worktree. Do not remove them here. For Architect integration in the
saved root, use this recoverable procedure after reviewing the manifest before
the move:

```bash
SAVED_ROOT='/Volumes/OKH-Local/04_GitHub_Mirrors/AskJamie'
QUARANTINE='/Volumes/OKH-Local/04_GitHub_Mirrors/AskJamie/.codex-quarantine-ds-store-2026-09-05'
MANIFEST='/Volumes/OKH-Local/04_GitHub_Mirrors/AskJamie/assets/docs/delivery-engineering/ds-store-quarantine-manifest-2026-09-05.txt'
find "$SAVED_ROOT" -type f -name '.DS_Store' -print | sort > "$MANIFEST"
mkdir -p "$QUARANTINE"
```

After exact-path review, move only manifest entries, preserving their relative
paths under the quarantine directory:

```bash
while IFS= read -r PATH_ITEM; do
  RELATIVE_PATH="${PATH_ITEM#"$SAVED_ROOT"/}"
  TARGET_PATH="$QUARANTINE/$RELATIVE_PATH"
  mkdir -p "$(dirname "$TARGET_PATH")"
  mv "$PATH_ITEM" "$TARGET_PATH"
done < "$MANIFEST"
```

Then rerun the canonical audit and retain the manifest with the cleanup commit.
This isolated checkout cannot establish the saved root's current ignored-file
inventory.

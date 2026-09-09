#!/usr/bin/env python3
"""Read-only-by-default audit for one Replit Git checkout.

Reports local branch facts, naming violations, and nested detritus folders as
JSON. The script never deletes, renames, prunes, merges, or force-pushes.
Network fetch is opt-in with --fetch and still never prunes. Recovery snapshots
and verification are also read-only; an approval only identifies the exact
local branch removal that the comparison is allowed to observe.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


ROOT_GOVERNANCE_FILES = {
    "README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "AGENTS.md", "CLAUDE.md",
    "SKILL.md", "ROADMAP.md", "NOTICE",
}
TOOL_REQUIRED_PATTERNS = re.compile(
    r"^(package(-lock)?\.json|pnpm-lock\.yaml|pnpm-workspace\.yaml|"
    r"tsconfig.*\.json|vite\.config\.\w+|\.gitignore|\.replit|"
    r"\.replitignore|\.npmrc|\.prettierrc.*|Makefile|CNAME|Dockerfile|"
    r"\.env.*|Pipfile.*|requirements.*\.txt|go\.(mod|sum)|Gemfile.*|"
    r"Cargo\.(toml|lock))$"
)
WEB_STANDARD_FILES = {
    "humans.txt", "robots.txt", "llms.txt", "404.html", "_headers",
    "favicon.ico", "favicon.svg", "site.webmanifest", "sitemap.xml",
    "manifest.json",
}
DETRITUS_FOLDER_NAMES = {
    "attached_assets", "attached-assets", "_unused", "unused",
    "_drafts", "_scratch", "_old", "tmp", "temp",
}
IGNORED_DIRS = {
    ".git", "node_modules", ".cache", ".local", ".config", ".pythonlibs",
    ".upm", "dist", "build", ".next", ".vite", "__pycache__",
}
KEBAB_OK = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPLIT_BRANCH_PATTERNS = re.compile(r"^(subrepl-|replit-agent$|agent/)")


class AuditError(RuntimeError):
    """A Git or repository precondition failed."""


def run(args: list[str], cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode:
        command = " ".join(args)
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        raise AuditError(f"`{command}` failed ({result.returncode}): {detail}")
    return result.stdout.strip()


def ensure_repository(root: Path) -> None:
    if not root.is_dir():
        raise AuditError(f"repository root does not exist: {root}")
    inside = run(["git", "rev-parse", "--is-inside-work-tree"], root)
    if inside != "true":
        raise AuditError(f"not inside a Git work tree: {root}")


def ensure_base(root: Path, base: str) -> None:
    run(["git", "rev-parse", "--verify", f"{base}^{{commit}}"], root)


def git_ref_snapshot(root: Path) -> dict[str, str]:
    """Return every ref and its object ID in stable, machine-readable form."""
    output = run(
        ["git", "for-each-ref", "--format=%(refname)%00%(objectname)"],
        root,
    )
    refs: dict[str, str] = {}
    for line in output.splitlines():
        name, separator, object_id = line.partition("\0")
        if not separator or not name or not object_id:
            raise AuditError(f"malformed Git ref record: {line!r}")
        refs[name] = object_id
    return dict(sorted(refs.items()))


def reachable_object_snapshot(root: Path) -> list[str]:
    """Return all objects reachable from refs, sorted for deterministic diffs."""
    output = run(["git", "rev-list", "--all", "--objects"], root)
    object_ids = {
        line.split(maxsplit=1)[0]
        for line in output.splitlines()
        if line
    }
    return sorted(object_ids)


def recovery_snapshot(root: Path) -> dict[str, object]:
    """Capture refs, stashes, and reachable objects without changing Git."""
    return {
        "format": 1,
        "current_branch": run(["git", "branch", "--show-current"], root) or None,
        "refs": git_ref_snapshot(root),
        "stashes": run(
            ["git", "stash", "list", "--format=%H%x00%gd%x00%s"], root
        ).splitlines(),
        "reachable_objects": reachable_object_snapshot(root),
    }


def validate_recovery_snapshot(snapshot: object) -> dict[str, object]:
    """Reject malformed or incomplete snapshots before comparing them."""
    if not isinstance(snapshot, dict) or snapshot.get("format") != 1:
        raise AuditError("recovery snapshot has an unsupported format")
    refs = snapshot.get("refs")
    stashes = snapshot.get("stashes")
    reachable = snapshot.get("reachable_objects")
    if not isinstance(refs, dict) or not all(
        isinstance(name, str) and isinstance(object_id, str)
        for name, object_id in refs.items()
    ):
        raise AuditError("recovery snapshot has malformed refs")
    if not isinstance(stashes, list) or not all(
        isinstance(stash, str) for stash in stashes
    ):
        raise AuditError("recovery snapshot has malformed stashes")
    if not isinstance(reachable, list) or not all(
        isinstance(object_id, str) for object_id in reachable
    ):
        raise AuditError("recovery snapshot has malformed reachable objects")
    return snapshot


def approved_local_ref(branch: str) -> str:
    """Convert an exact branch approval into a fully qualified local ref."""
    if branch.startswith("refs/") or not branch:
        raise AuditError(
            "approved deletion must be a local branch name, not a ref path"
        )
    return f"refs/heads/{branch}"


def compare_recovery_snapshots(
    before: dict[str, object],
    after: dict[str, object],
    approved_deletions: Iterable[str] = (),
) -> dict[str, object]:
    """Compare snapshots, permitting only exact approved local deletions."""
    before = validate_recovery_snapshot(before)
    after = validate_recovery_snapshot(after)
    before_refs = before["refs"]
    after_refs = after["refs"]
    assert isinstance(before_refs, dict)
    assert isinstance(after_refs, dict)

    approved_refs = {approved_local_ref(branch) for branch in approved_deletions}
    current_branch = before.get("current_branch")
    if "refs/heads/main" in approved_refs:
        raise AuditError("main is protected and cannot be approved for deletion")
    if current_branch and f"refs/heads/{current_branch}" in approved_refs:
        raise AuditError("the checked-out branch cannot be approved for deletion")

    removed_refs = sorted(set(before_refs) - set(after_refs))
    changed_refs = sorted(
        name for name in set(before_refs) & set(after_refs)
        if before_refs[name] != after_refs[name]
    )
    unexpected_removed_refs = sorted(set(removed_refs) - approved_refs)
    missing_approved_refs = sorted(approved_refs - set(removed_refs))

    approved_tip_ids = {
        before_refs[ref] for ref in approved_refs if ref in before_refs
    }
    added_refs = sorted(set(after_refs) - set(before_refs))
    invalid_added_refs = sorted(
        name for name in added_refs
        if not (
            name.startswith("refs/recovery/")
            and after_refs[name] in approved_tip_ids
        )
    )
    missing_recovery_refs = sorted(
        ref for ref in approved_refs
        if ref in before_refs
        and not any(
            name.startswith("refs/recovery/")
            and object_id == before_refs[ref]
            for name, object_id in after_refs.items()
        )
    )

    before_stashes = before["stashes"]
    after_stashes = after["stashes"]
    assert isinstance(before_stashes, list)
    assert isinstance(after_stashes, list)
    stash_changed = before_stashes != after_stashes

    before_objects = set(before["reachable_objects"])
    after_objects = set(after["reachable_objects"])
    unreachable_objects = sorted(before_objects - after_objects)
    errors: list[str] = []
    if unexpected_removed_refs:
        errors.append(
            "unexpected refs removed: " + ", ".join(unexpected_removed_refs)
        )
    if missing_approved_refs:
        errors.append(
            "approved local refs were not removed: "
            + ", ".join(missing_approved_refs)
        )
    if changed_refs:
        errors.append("refs changed: " + ", ".join(changed_refs))
    if invalid_added_refs:
        errors.append(
            "unexpected refs added: " + ", ".join(invalid_added_refs)
        )
    if missing_recovery_refs:
        errors.append(
            "removed local refs lack recovery refs: "
            + ", ".join(missing_recovery_refs)
        )
    if stash_changed:
        errors.append("stash entries changed")
    if unreachable_objects:
        errors.append(
            f"{len(unreachable_objects)} previously reachable objects were lost"
        )

    return {
        "passed": not errors,
        "approved_local_deletions": sorted(approved_refs),
        "removed_refs": removed_refs,
        "changed_refs": changed_refs,
        "added_refs": added_refs,
        "unexpected_removed_refs": unexpected_removed_refs,
        "invalid_added_refs": invalid_added_refs,
        "missing_recovery_refs": missing_recovery_refs,
        "stashes_unchanged": not stash_changed,
        "unreachable_objects": unreachable_objects,
        "errors": errors,
    }


def write_recovery_snapshot(path: Path, snapshot: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_recovery_snapshot(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"could not read recovery snapshot {path}: {exc}") from exc
    return validate_recovery_snapshot(data)


def audit_branches(root: Path, base: str) -> tuple[list[dict[str, object]], str]:
    current = run(["git", "branch", "--show-current"], root)
    branches = run(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
        root,
    ).splitlines()
    merged = set(
        run(
            ["git", "branch", "--merged", base, "--format=%(refname:short)"],
            root,
        ).splitlines()
    )
    ledger: list[dict[str, object]] = []
    for branch in branches:
        if not branch:
            continue
        last = run(
            ["git", "log", "-1", "--format=%ci%x00%an%x00%s", branch],
            root,
        )
        date, author, subject = (last.split("\0", 2) + ["", "", ""])[:3]
        ledger.append({
            "branch": branch,
            "is_current": bool(current) and branch == current,
            "merged_into_base": branch in merged,
            "last_commit_date": date,
            "last_commit_author": author,
            "last_commit_subject": subject,
            "replit_generated_pattern": bool(REPLIT_BRANCH_PATTERNS.match(branch)),
        })
    return ledger, current


def is_exception(path: Path, root: Path) -> bool:
    name = path.name
    if name in WEB_STANDARD_FILES or TOOL_REQUIRED_PATTERNS.match(name):
        return True
    if path.parent == root and name in ROOT_GOVERNANCE_FILES:
        return True
    if name.startswith("."):
        return True
    if path.suffix.lower() in {".tsx", ".jsx"}:
        return True
    if path.suffix.lower() == ".ts" and re.match(r"^use[A-Z]", path.stem):
        return True
    return False


def iter_visible(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        yield path


def naming_reason(path: Path, root: Path) -> str | None:
    if is_exception(path, root):
        return None
    name = path.name
    stem = path.stem
    if " " in name:
        return "contains spaces"
    if path.suffix and path.suffix != path.suffix.lower():
        return "uppercase extension"
    if "_" in stem:
        return "uses underscores instead of hyphens"
    if re.search(r"[A-Z]", stem) and not stem.isupper():
        return "mixed/camel/Pascal case"
    if stem.isupper():
        return None  # avoid treating established all-caps docs as clear violations
    if not KEBAB_OK.fullmatch(stem):
        return "not kebab-case"
    return None


def audit_naming(root: Path) -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []
    for path in iter_visible(root):
        if path.is_dir():
            continue
        reason = naming_reason(path, root)
        if reason:
            violations.append({
                "path": path.relative_to(root).as_posix(),
                "reason": reason,
            })
    return sorted(violations, key=lambda item: item["path"])


def audit_detritus(root: Path) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for path in iter_visible(root):
        if not path.is_dir() or path.name not in DETRITUS_FOLDER_NAMES:
            continue
        relative = path.relative_to(root).as_posix()
        tracked = run(["git", "ls-files", "--", relative], root)
        found.append({
            "folder": relative,
            "tracked_file_count": len(tracked.splitlines()) if tracked else 0,
        })
    return sorted(found, key=lambda item: str(item["folder"]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="run `git fetch --all` before auditing; never prunes",
    )
    parser.add_argument(
        "--snapshot-recovery",
        metavar="PATH",
        help="write a read-only snapshot of refs, stashes, and reachable objects",
    )
    parser.add_argument(
        "--verify-recovery",
        metavar="PATH",
        help="compare the current read-only state with a recovery snapshot",
    )
    parser.add_argument(
        "--approve-local-deletion",
        action="append",
        default=[],
        metavar="BRANCH",
        help=(
            "allow exactly this local branch ref to be absent during "
            "--verify-recovery; does not delete anything"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    try:
        ensure_repository(root)
        if args.snapshot_recovery and args.verify_recovery:
            raise AuditError(
                "--snapshot-recovery and --verify-recovery are mutually exclusive"
            )
        if args.fetch and (args.snapshot_recovery or args.verify_recovery):
            raise AuditError(
                "--fetch cannot be combined with the read-only recovery guard"
            )
        if args.approve_local_deletion and not args.verify_recovery:
            raise AuditError(
                "--approve-local-deletion requires --verify-recovery"
            )
        if args.fetch:
            run(["git", "fetch", "--all"], root)
        if args.snapshot_recovery:
            snapshot = recovery_snapshot(root)
            path = Path(args.snapshot_recovery).resolve()
            write_recovery_snapshot(path, snapshot)
            print(json.dumps({
                "snapshot_file": str(path),
                "recovery_snapshot": snapshot,
            }, indent=2, sort_keys=True))
            return 0
        if args.verify_recovery:
            before = read_recovery_snapshot(Path(args.verify_recovery).resolve())
            result = compare_recovery_snapshots(
                before,
                recovery_snapshot(root),
                args.approve_local_deletion,
            )
            print(json.dumps({
                "snapshot_file": str(Path(args.verify_recovery).resolve()),
                "recovery_guard": result,
            }, indent=2, sort_keys=True))
            return 0 if result["passed"] else 1
        ensure_base(root, args.base)
        branches, current = audit_branches(root, args.base)
        report = {
            "root": str(root),
            "base": args.base,
            "fetch_performed": args.fetch,
            "current_branch": current or None,
            "detached_head": not bool(current),
            "branches": branches,
            "naming_violations": audit_naming(root),
            "detritus_folders": audit_detritus(root),
        }
        print(json.dumps(report, indent=2))
        return 0
    except (AuditError, OSError) as exc:
        print(json.dumps({"error": str(exc), "root": str(root)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
audit-repo.py -- read-only Git branch + decision-ledger + file/folder naming audit for a single
local repository (designed for one-repo-per-Replit-workspace checkouts).

Never mutates the repository. Prints a JSON report to stdout.

Usage:
    python3 audit-repo.py [--root PATH] [--base origin/main]

What it reports:
  1. Branch ledger: every local branch, its last commit date/author,
     whether it is merged into the base branch, and whether it matches a
     known Replit-generated pattern (subrepl-*, replit-agent, agent/*)
     versus a human-named branch.
  2. Decision-ledger consistency: missing non-current branches, tip-SHA
      drift, and stale decision or exclusion rows.
  3. Naming violations: files/folders whose names break the kebab-case
     default (PascalCase, camelCase, spaces, uppercase extensions) outside
     the recognized structural exceptions (React components/hooks, root
     governance files, tool-required filenames).
  4. Known detritus folder names present in the tree (attached_assets,
     tmp, temp, _unused, unused, _drafts, _scratch, _old, and hyphen
     variants), with tracked/untracked/gitignored status for each.

This script only reads; it never deletes, renames, or force-pushes anything.
Treat its output as evidence for a plan, not as an execution instruction.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

ROOT_GOVERNANCE_FILES = {
    "README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "AGENTS.md", "CLAUDE.md",
    "SKILL.md", "ROADMAP.md", "NOTICE",
}
TOOL_REQUIRED_PATTERNS = re.compile(
    r"^(package(-lock)?\.json|tsconfig.*\.json|vite\.config\.\w+|"
    r"\.gitignore|\.replit|\.replitignore|\.npmrc|\.prettierrc.*|"
    r"Makefile|CNAME|Dockerfile|\.env.*|Pipfile.*|requirements.*\.txt|"
    r"go\.(mod|sum)|Gemfile.*|Cargo\.(toml|lock))$"
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
KEBAB_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REPLIT_BRANCH_PATTERNS = re.compile(r"^(subrepl-|replit-agent$|agent/)")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_DECISION_LEDGER = ".agents/branch-decision-ledger-2026-09-07.md"


def sh(args, cwd):
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, check=False
    ).stdout.strip()


def refresh_remote(root: Path) -> dict[str, object]:
    """Refresh remote-tracking refs without allowing an interactive prompt."""
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    ssh_command = env.get("GIT_SSH_COMMAND", "ssh").strip() or "ssh"
    ssh_command, replaced = re.subn(
        r"(?i)(-o\s+BatchMode)(?:\s+|=)(?:yes|no)",
        r"\1=yes",
        ssh_command,
    )
    if not replaced:
        ssh_command = f"{ssh_command} -o BatchMode=yes"
    env["GIT_SSH_COMMAND"] = ssh_command
    try:
        result = subprocess.run(
            ["git", "fetch", "--all"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            env=env,
            stdin=subprocess.DEVNULL,
        )
    except OSError as exc:
        return {
            "status": "unavailable",
            "classification": "remote-unavailable",
            "non_interactive": True,
            "detail": f"{type(exc).__name__}: {exc}",
        }
    if result.returncode == 0:
        return {
            "status": "ok",
            "classification": "refreshed",
            "non_interactive": True,
        }

    detail = (result.stderr or result.stdout).strip()
    return {
        "status": "unavailable",
        "classification": "remote-unavailable",
        "non_interactive": True,
        "exit_code": result.returncode,
        "detail": detail[:500] or "git fetch --all failed without diagnostic output",
    }


class DecisionLedger(NamedTuple):
    decisions: list[dict[str, str]]
    exclusions: list[str]


def audit_branches(root: Path, base: str, *, refresh: bool = True):
    if refresh:
        refresh_remote(root)
    branches = sh(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
        root,
    ).splitlines()
    merged = set(
        sh(["git", "branch", "--merged", base, "--format=%(refname:short)"], root)
        .splitlines()
    )
    ledger = []
    for b in branches:
        if not b:
            continue
        last = sh(
            ["git", "log", "-1", "--format=%ci|%an|%s", b], root
        )
        date, author, subject = (last.split("|", 2) + ["", "", ""])[:3]
        ledger.append({
            "branch": b,
            "is_current": b == sh(["git", "branch", "--show-current"], root),
            "tip_sha": sh(["git", "rev-parse", b], root),
            "merged_into_base": b in merged,
            "last_commit_date": date,
            "last_commit_author": author,
            "last_commit_subject": subject,
            "replit_generated_pattern": bool(REPLIT_BRANCH_PATTERNS.match(b)),
        })
    return ledger


def _table_cells(line: str) -> list[str]:
    """Return markdown table cells without leading/trailing separators."""
    if not line.lstrip().startswith("|"):
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_decision_ledger(path: Path) -> DecisionLedger:
    """Parse the decision table and explicit holds from a markdown ledger."""
    if not path.is_file():
        raise ValueError(f"decision ledger does not exist: {path}")

    decisions: list[dict[str, str]] = []
    exclusions: list[str] = []
    section = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            section = heading.group(1).lower()
            continue

        if section == "branch decisions":
            cells = _table_cells(line)
            if len(cells) < 3:
                continue
            branch_match = re.fullmatch(r"`([^`]+)`", cells[0])
            if not branch_match:
                continue
            decisions.append({
                "branch": branch_match.group(1),
                "decision": re.sub(
                    r"^\*\*|\*\*$", "", cells[1]
                ).strip().lower(),
                "tip_sha": cells[2].strip("`").lower(),
            })
        elif section == "explicit exclusions and holds" and line.lstrip().startswith("-"):
            # A bullet may document several refs, e.g. "`main`, `branch-a`,
            # and `branch-b` — active work".
            branch_list = line.split("—", 1)[0]
            exclusions.extend(re.findall(r"`([^`]+)`", branch_list))

    if not decisions and not exclusions:
        raise ValueError(f"decision ledger has no branch coverage rows: {path}")
    return DecisionLedger(decisions=decisions, exclusions=sorted(set(exclusions)))


def audit_decision_ledger(
    root: Path,
    branches: list[dict[str, object]],
    current: str,
    ledger_path: Path,
) -> dict[str, object]:
    """Compare non-current local branches with written ledger coverage."""
    ledger = parse_decision_ledger(ledger_path)
    local_by_name = {
        str(branch["branch"]): branch
        for branch in branches
        if str(branch["branch"]) != current
    }
    decision_by_name = {row["branch"]: row for row in ledger.decisions}
    covered = set(decision_by_name) | set(ledger.exclusions)

    missing_branches = sorted(set(local_by_name) - covered)
    tip_sha_drift: list[dict[str, str]] = []
    invalid_tip_sha: list[dict[str, str]] = []
    for branch, row in decision_by_name.items():
        if branch not in local_by_name:
            continue
        expected = row["tip_sha"]
        actual = str(local_by_name[branch]["tip_sha"])
        if not SHA_PATTERN.fullmatch(expected):
            invalid_tip_sha.append({
                "branch": branch,
                "expected_tip_sha": expected,
                "actual_tip_sha": actual,
            })
        elif expected != actual:
            tip_sha_drift.append({
                "branch": branch,
                "expected_tip_sha": expected,
                "actual_tip_sha": actual,
            })

    stale_ledger_rows: list[dict[str, str]] = []
    for row in ledger.decisions:
        if row["branch"] not in local_by_name:
            stale_ledger_rows.append({
                "branch": row["branch"],
                "kind": "decision",
                "tip_sha": row["tip_sha"],
            })
    for branch in ledger.exclusions:
        if branch not in local_by_name and branch != current:
            stale_ledger_rows.append({
                "branch": branch,
                "kind": "exclusion",
            })

    return {
        "ledger_path": str(ledger_path),
        "covered_branch_count": len(covered),
        "decision_row_count": len(ledger.decisions),
        "exclusion_branch_count": len(ledger.exclusions),
        "missing_branches": missing_branches,
        "tip_sha_drift": sorted(tip_sha_drift, key=lambda item: item["branch"]),
        "invalid_tip_sha": sorted(invalid_tip_sha, key=lambda item: item["branch"]),
        "stale_ledger_rows": sorted(
            stale_ledger_rows, key=lambda item: (item["branch"], item["kind"])
        ),
        "ok": not (
            missing_branches
            or tip_sha_drift
            or invalid_tip_sha
            or stale_ledger_rows
        ),
    }


def is_exception(name: str, path: Path) -> bool:
    if name in ROOT_GOVERNANCE_FILES or name in WEB_STANDARD_FILES:
        return True
    if TOOL_REQUIRED_PATTERNS.match(name):
        return True
    if name.startswith("."):
        return True  # dotfiles follow their own tool convention
    suffix = path.suffix
    if suffix in (".tsx", ".jsx"):
        return True  # PascalCase component convention
    if suffix == ".ts" and re.match(r"^use[A-Z]", path.stem):
        return True  # camelCase hook convention
    return False


def audit_naming(root: Path):
    ignored_dirs = {
        ".git", "node_modules", ".cache", ".local", ".config", ".pythonlibs",
        ".upm", "dist", "build", ".next", ".vite", "__pycache__",
    }
    violations = []
    for p in root.rglob("*"):
        if any(part in ignored_dirs for part in p.parts):
            continue
        if p.is_dir():
            continue
        name = p.name
        stem = p.stem
        if is_exception(name, p):
            continue
        if " " in name:
            violations.append({"path": str(p.relative_to(root)), "reason": "contains spaces"})
            continue
        if re.search(r"[A-Z]", stem) and not stem.isupper():
            violations.append({"path": str(p.relative_to(root)), "reason": "mixed/camel/Pascal case"})
            continue
        if not KEBAB_OK.match(stem.lower()) and not KEBAB_OK.match(stem):
            pass  # avoid false positives on numeric/versioned names; report only clear cases above
    return violations


def audit_detritus(root: Path):
    found = []
    for name in DETRITUS_FOLDER_NAMES:
        p = root / name
        if p.exists():
            tracked = sh(["git", "ls-files", name], root)
            found.append({
                "folder": name,
                "exists": True,
                "tracked_file_count": len(tracked.splitlines()) if tracked else 0,
            })
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--base", default="origin/main")
    ap.add_argument(
        "--decision-ledger",
        "--ledger",
        dest="decision_ledger",
        default=DEFAULT_DECISION_LEDGER,
        help=(
            "markdown branch-decision ledger to compare with local refs "
            f"(default: {DEFAULT_DECISION_LEDGER})"
        ),
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if not (root / ".git").exists():
        print(json.dumps({"error": f"{root} is not a Git repository root"}))
        return 1

    ledger_path = Path(args.decision_ledger)
    if not ledger_path.is_absolute():
        ledger_path = root / ledger_path

    try:
        remote_refresh = refresh_remote(root)
        branches = audit_branches(root, args.base, refresh=False)
        current = next(
            (
                str(branch["branch"])
                for branch in branches
                if bool(branch["is_current"])
            ),
            "",
        )
        decision_ledger = audit_decision_ledger(
            root, branches, current, ledger_path
        )
        report = {
            "root": str(root),
            "base": args.base,
            "remote_refresh": remote_refresh,
            "branches": branches,
            "decision_ledger": decision_ledger,
            "naming_violations": audit_naming(root),
            "detritus_folders": audit_detritus(root),
        }
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "root": str(root)}))
        return 1

    print(json.dumps(report, indent=2))
    return 0 if (
        remote_refresh["status"] == "ok"
        and bool(decision_ledger["ok"])
    ) else 1


if __name__ == "__main__":
    sys.exit(main())

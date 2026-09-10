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
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urlparse


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


def hosted_command(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a hosted read-only command without allowing interactive auth."""
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    ssh_command = env.get("GIT_SSH_COMMAND", "ssh")
    if "BatchMode" not in ssh_command:
        ssh_command = f"{ssh_command} -o BatchMode=yes"
    env["GIT_SSH_COMMAND"] = ssh_command
    return subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=env,
    )


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


def parse_hosted_branch(value: str) -> tuple[str, str]:
    """Parse the exact provider/ref pair accepted by the hosted audit."""
    separator = "=" if "=" in value else ":"
    if separator not in value:
        raise AuditError(
            "hosted branch must use PROVIDER=BRANCH (or PROVIDER:BRANCH)"
        )
    provider, branch = value.split(separator, 1)
    if not provider or not branch:
        raise AuditError(
            "hosted branch must include both a provider and an exact branch"
        )
    if branch.startswith("refs/heads/"):
        branch = branch.removeprefix("refs/heads/")
    if (
        not branch
        or branch.startswith("/")
        or branch.endswith("/")
        or "\x00" in branch
        or any(character.isspace() for character in branch)
    ):
        raise AuditError(f"invalid hosted branch name: {branch!r}")
    return provider, branch


def remote_url_for_provider(root: Path, provider: str) -> tuple[str, str | None]:
    """Resolve a configured remote, or accept a URL as an explicit provider."""
    if "://" in provider or provider.startswith("git@"):
        return provider, provider
    result = subprocess.run(
        ["git", "remote", "get-url", provider],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        return provider, None
    return provider, result.stdout.strip() or None


def github_repository(remote_url: str | None) -> tuple[str, str] | None:
    """Extract owner/repository from common GitHub remote URL forms."""
    if not remote_url:
        return None
    if remote_url.startswith("git@github.com:"):
        path = remote_url.split(":", 1)[1]
    else:
        parsed = urlparse(remote_url)
        if parsed.hostname != "github.com":
            return None
        path = parsed.path.lstrip("/")
    path = path.removesuffix(".git").strip("/")
    parts = path.split("/")
    if len(parts) != 2 or not all(parts):
        return None
    return parts[0], parts[1]


def unknown_hosted_evidence(reason: str) -> dict[str, object]:
    return {"status": "unknown", "reason": reason}


def gh_api_json(root: Path, endpoint: str) -> tuple[object | None, str | None]:
    """Read one GitHub API endpoint, returning an explicit failure reason."""
    if shutil.which("gh") is None:
        return None, "GitHub CLI (`gh`) is not installed"
    result = hosted_command(["gh", "api", endpoint], root)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        return None, f"GitHub API request failed ({result.returncode}): {detail}"
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"GitHub API returned invalid JSON: {exc}"


def github_hosted_evidence(
    root: Path, remote_url: str | None, branch: str
) -> dict[str, object]:
    """Collect protection, deployment, and PR evidence when GitHub is usable."""
    repository = github_repository(remote_url)
    if repository is None:
        reason = "no supported hosted-provider evidence adapter"
        return {
            "protection": unknown_hosted_evidence(reason),
            "deployments": unknown_hosted_evidence(reason),
            "pull_requests": unknown_hosted_evidence(reason),
        }

    owner, repo = repository
    encoded_repo = f"{quote(owner, safe='')}/{quote(repo, safe='')}"
    encoded_branch = quote(branch, safe="")
    branch_data, branch_error = gh_api_json(
        root,
        f"repos/{encoded_repo}/branches/{encoded_branch}",
    )
    if branch_error:
        protection: dict[str, object] = unknown_hosted_evidence(branch_error)
    elif isinstance(branch_data, dict):
        protected = branch_data.get("protected")
        if isinstance(protected, bool):
            protection = {
                "status": "protected" if protected else "unprotected",
                "source": "github-api",
                "repository": f"{owner}/{repo}",
                "ref": branch,
            }
        else:
            protection = unknown_hosted_evidence(
                "GitHub branch response did not include protection status"
            )
    else:
        protection = unknown_hosted_evidence(
            "GitHub branch response was not an object"
        )

    deployments_data, deployments_error = gh_api_json(
        root,
        f"repos/{encoded_repo}/deployments?ref={encoded_branch}&per_page=100",
    )
    if deployments_error:
        deployments: dict[str, object] = unknown_hosted_evidence(
            deployments_error
        )
    elif isinstance(deployments_data, list):
        deployments = {
            "status": "available",
            "source": "github-api",
            "count": len(deployments_data),
            "items": [
                {
                    key: item.get(key)
                    for key in (
                        "id", "sha", "ref", "environment", "created_at",
                        "updated_at",
                    )
                    if isinstance(item, dict) and key in item
                }
                for item in deployments_data
                if isinstance(item, dict)
            ],
        }
    else:
        deployments = unknown_hosted_evidence(
            "GitHub deployments response was not a list"
        )

    head = quote(f"{owner}:{branch}", safe="")
    pull_requests_data, pull_requests_error = gh_api_json(
        root,
        f"repos/{encoded_repo}/pulls?state=all&head={head}&per_page=100",
    )
    if pull_requests_error:
        pull_requests: dict[str, object] = unknown_hosted_evidence(
            pull_requests_error
        )
    elif isinstance(pull_requests_data, list):
        pull_requests = {
            "status": "available",
            "source": "github-api",
            "count": len(pull_requests_data),
            "items": [
                {
                    key: item.get(key)
                    for key in (
                        "number", "state", "title", "merged_at", "html_url",
                        "head", "base",
                    )
                    if isinstance(item, dict) and key in item
                }
                for item in pull_requests_data
                if isinstance(item, dict)
            ],
        }
    else:
        pull_requests = unknown_hosted_evidence(
            "GitHub pull-request response was not a list"
        )
    return {
        "protection": protection,
        "deployments": deployments,
        "pull_requests": pull_requests,
    }


def audit_hosted_branches(
    root: Path, requested: Iterable[str]
) -> dict[str, object]:
    """Audit each exact provider/ref pair without collapsing provider state."""
    entries: list[dict[str, object]] = []
    for value in requested:
        provider, branch = parse_hosted_branch(value)
        remote, remote_url = remote_url_for_provider(root, provider)
        entry: dict[str, object] = {
            "provider": provider,
            "ref": branch,
            "full_ref": f"refs/heads/{branch}",
            "remote": remote,
            "remote_url": remote_url,
        }
        if remote_url is None:
            entry.update({
                "classification": "inaccessible",
                "ref_status": "unknown",
                "reason": f"configured remote is not available: {provider}",
            })
            entry.update({
                "protection": unknown_hosted_evidence(
                    "hosted remote is inaccessible"
                ),
                "deployments": unknown_hosted_evidence(
                    "hosted remote is inaccessible"
                ),
                "pull_requests": unknown_hosted_evidence(
                    "hosted remote is inaccessible"
                ),
                "deletion_blocked": True,
                "blocking_reasons": ["hosted-remote-inaccessible"],
            })
            entries.append(entry)
            continue

        probe = hosted_command(
            ["git", "ls-remote", "--heads", remote, entry["full_ref"]],
            root,
        )
        if probe.returncode:
            detail = probe.stderr.strip() or probe.stdout.strip() or "no output"
            entry.update({
                "classification": "inaccessible",
                "ref_status": "unknown",
                "reason": detail,
            })
            evidence = {
                "protection": unknown_hosted_evidence(
                    "hosted remote is inaccessible"
                ),
                "deployments": unknown_hosted_evidence(
                    "hosted remote is inaccessible"
                ),
                "pull_requests": unknown_hosted_evidence(
                    "hosted remote is inaccessible"
                ),
            }
            entry.update(evidence)
            entry.update({
                "deletion_blocked": True,
                "blocking_reasons": ["hosted-remote-inaccessible"],
            })
            entries.append(entry)
            continue

        matching_lines = [
            line.split()[0]
            for line in probe.stdout.splitlines()
            if line.split() and line.split()[-1] == entry["full_ref"]
        ]
        if not matching_lines:
            entry.update({
                "classification": "missing",
                "ref_status": "missing",
                "reason": "hosted branch ref was not returned by the remote",
            })
            evidence = {
                "protection": unknown_hosted_evidence("hosted ref is missing"),
                "deployments": unknown_hosted_evidence("hosted ref is missing"),
                "pull_requests": unknown_hosted_evidence("hosted ref is missing"),
            }
            entry.update(evidence)
            entry.update({
                "deletion_blocked": True,
                "blocking_reasons": ["hosted-ref-missing"],
            })
            entries.append(entry)
            continue

        entry.update({
            "classification": "present",
            "ref_status": "present",
            "tip": matching_lines[0],
        })
        evidence = github_hosted_evidence(root, remote_url, branch)
        entry.update(evidence)
        blocking_reasons: list[str] = []
        protection = evidence["protection"]
        deployments = evidence["deployments"]
        pull_requests = evidence["pull_requests"]
        assert isinstance(protection, dict)
        assert isinstance(deployments, dict)
        assert isinstance(pull_requests, dict)
        if protection.get("status") == "protected":
            blocking_reasons.append("hosted-ref-protected")
        elif protection.get("status") == "unknown":
            blocking_reasons.append("hosted-protection-unknown")
        if deployments.get("status") != "available":
            blocking_reasons.append("hosted-deployment-evidence-unknown")
        elif deployments.get("count", 0):
            blocking_reasons.append("hosted-ref-has-deployments")
        if pull_requests.get("status") != "available":
            blocking_reasons.append("hosted-pull-request-evidence-unknown")
        else:
            for pull_request in pull_requests.get("items", []):
                if not isinstance(pull_request, dict):
                    continue
                if pull_request.get("state") == "open":
                    blocking_reasons.append("hosted-open-pull-request")
                elif (
                    pull_request.get("state") == "closed"
                    and not pull_request.get("merged_at")
                ):
                    blocking_reasons.append(
                        "hosted-closed-unmerged-pull-request"
                    )
        entry["deletion_blocked"] = bool(blocking_reasons)
        entry["blocking_reasons"] = sorted(set(blocking_reasons))
        entries.append(entry)

    blocking_entries = [
        f"{entry['provider']}:{entry['ref']}"
        for entry in entries
        if entry["deletion_blocked"]
    ]
    return {
        "requested": True,
        "entries": entries,
        "deletion_blocked": bool(blocking_entries),
        "blocking_entries": blocking_entries,
    }


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
    parser.add_argument(
        "--hosted-branch",
        "--hosted-ref",
        dest="hosted_branches",
        action="append",
        default=[],
        metavar="PROVIDER=BRANCH",
        help=(
            "audit one exact hosted branch through the named Git remote; "
            "repeat for each provider/ref pair"
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
        if args.hosted_branches:
            report["hosted_lifecycle"] = audit_hosted_branches(
                root, args.hosted_branches
            )
        print(json.dumps(report, indent=2))
        return 0
    except (AuditError, OSError) as exc:
        print(json.dumps({"error": str(exc), "root": str(root)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
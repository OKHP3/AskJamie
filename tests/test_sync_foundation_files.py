"""Focused safety regressions for the sibling foundation sync tool."""

import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sync-foundation-files.py"
SPEC = importlib.util.spec_from_file_location("sync_foundation", SCRIPT)
sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sync)


class SyncSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="askjamie-sync-safety-")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name) / "askjamie"
        (self.repo / ".git").mkdir(parents=True)
        self.target = self.repo / "assets/css/theme.css"
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(b"before")
        self.repos = {"askjamie": self.repo}
        self.plan = [{
            "status": "sync-needed",
            "file": "assets/css/theme.css",
            "preimages": {"askjamie": b"before"},
            "writes": [{
                "repo": "askjamie",
                "preimage": b"before",
                "content": b"after",
            }],
        }]

    def test_changed_preimage_refuses_before_write(self):
        self.target.write_bytes(b"changed")
        with patch.object(sync, "repo_file_dirty", return_value=False):
            problems = sync.preflight_writes(self.plan, self.repos)
        self.assertIn("file changed since plan was built", problems[0])
        self.assertEqual(self.target.read_bytes(), b"changed")

    def test_source_dirty_state_refuses_before_destination_write(self):
        source = Path(self.temporary.name) / "overkill-hill"
        source_target = source / "assets/css/theme.css"
        source_target.parent.mkdir(parents=True)
        source_target.write_bytes(b"canonical")
        plan = [{
            "status": "sync-needed",
            "file": "assets/css/theme.css",
            "preimages": {"overkill-hill": b"canonical", "askjamie": b"before"},
            "writes": [{"repo": "askjamie", "preimage": b"before", "content": b"canonical"}],
        }]
        repos = {"overkill-hill": source, "askjamie": self.repo}
        with patch.object(sync, "repo_has_index_lock", return_value=False), \
                patch.object(sync, "repo_file_dirty", side_effect=[True, False]):
            problems = sync.preflight_writes(plan, repos)
        self.assertTrue(any("overkill-hill/assets/css/theme.css" in problem for problem in problems))
        self.assertEqual(self.target.read_bytes(), b"before")

    def test_staged_and_untracked_status_are_dirty(self):
        for porcelain in ("M  assets/css/theme.css\n", "?? assets/css/theme.css\n"):
            result = subprocess.CompletedProcess([], 0, stdout=porcelain, stderr="")
            with patch.object(sync.subprocess, "run", return_value=result):
                self.assertTrue(sync.repo_file_dirty(self.repo, "assets/css/theme.css"))

    def test_index_lock_is_never_moved_or_ignored(self):
        lock = self.repo / ".git/index.lock"
        lock.write_text("active", encoding="utf-8")
        with patch.object(sync, "repo_file_dirty", return_value=False):
            problems = sync.preflight_writes(self.plan, self.repos)
        self.assertTrue(any(".git/index.lock exists" in problem for problem in problems))
        self.assertTrue(lock.exists())

    def test_index_lock_uses_git_resolved_path_for_linked_worktree(self):
        lock = Path(self.temporary.name) / "shared" / "index.lock"
        lock.parent.mkdir()
        lock.write_text("active", encoding="utf-8")
        result = subprocess.CompletedProcess(
            ["git", "rev-parse", "--git-path", "index.lock"],
            0,
            stdout=str(lock) + "\n",
            stderr="",
        )
        with patch.object(sync.subprocess, "run", return_value=result):
            self.assertTrue(sync.repo_has_index_lock(self.repo))

    def test_dirty_target_refuses_before_write(self):
        with patch.object(sync, "repo_file_dirty", return_value=True):
            problems = sync.preflight_writes(self.plan, self.repos)
        self.assertTrue(any("file has local edits" in problem for problem in problems))

    def test_dry_run_does_not_write_or_run_hooks(self):
        before = self.target.read_bytes()
        with patch.object(sync, "POST_WRITE_HOOKS", {"askjamie": {"assets/css/theme.css": [["hook"]]}}), \
                patch.object(sync.subprocess, "run") as run:
            # Dry-run planning never invokes hooks or writes the target.
            for write in self.plan[0]["writes"]:
                self.assertEqual(write["content"], b"after")
        self.assertEqual(self.target.read_bytes(), before)
        run.assert_not_called()

    def test_failed_post_hook_is_serializable_and_blocks_commit(self):
        hook_failure = subprocess.CompletedProcess(["hook"], 1, stdout="", stderr="hook failed")
        with patch.object(sync, "POST_WRITE_HOOKS", {"askjamie": {"assets/css/theme.css": [["hook"]]}}), \
                patch.object(sync.subprocess, "run", return_value=hook_failure):
            failures = sync.run_post_hooks("askjamie", "assets/css/theme.css", self.repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("hook failed", failures[0])
        self.assertNotEqual(hook_failure.returncode, 0)

    def test_failed_post_hook_end_to_end_skips_commit_and_returns_json(self):
        repos = {name: Path(self.temporary.name) / name for name in ("overkill-hill", "glee-fullytools", "askjamie")}
        for name, repo in repos.items():
            target = repo / "assets/css/theme.css"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"after" if name == "overkill-hill" else b"before")
        plan = {
            "file": "assets/css/theme.css",
            "status": "sync-needed",
            "preimages": {name: b"before" if name != "overkill-hill" else b"after" for name in repos},
            "writes": [{
                "repo": "askjamie",
                "bytes": 5,
                "source_repo": "overkill-hill",
                "preimage": b"before",
                "content": b"after",
            }],
            "missing_in": [],
            "timestamps": {name: (1, "git") for name in repos},
            "conflict_groups": None,
            "source_repo": "overkill-hill",
            "winning_repos": ["overkill-hill"],
        }
        self.target.write_bytes(b"before")
        output = io.StringIO()
        with patch.object(sync, "mirror_root", return_value=Path(self.temporary.name)), \
                patch.object(sync, "discover_repos", return_value=repos), \
                patch.object(sync, "validate_repos", return_value=[]), \
                patch.object(sync, "plan_for_file", return_value=plan), \
                patch.object(sync, "repo_has_index_lock", return_value=False), \
                patch.object(sync, "repo_file_dirty", return_value=False), \
                patch.object(sync, "run_post_hooks", return_value=["askjamie/assets/css/theme.css: post-hook hook failed (hook failed)"]), \
                patch.object(sync, "commit_repo") as commit_repo, \
                patch.object(sync.sys, "argv", ["sync-foundation-files.py", "--commit", "--file", "theme.css", "--json"]), \
                redirect_stdout(output):
            exit_code = sync.main()
        report = json.loads(output.getvalue())
        self.assertEqual(exit_code, 2)
        self.assertFalse(commit_repo.called)
        self.assertEqual(report["hook_failures"], ["askjamie/assets/css/theme.css: post-hook hook failed (hook failed)"])
        self.assertEqual(self.target.read_bytes(), b"after")


if __name__ == "__main__":
    unittest.main()

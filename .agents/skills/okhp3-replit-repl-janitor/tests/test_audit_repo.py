from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit-repo.py"
SPEC = importlib.util.spec_from_file_location("audit_repo", SCRIPT)
assert SPEC and SPEC.loader
audit_repo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_repo)


class AuditRepoTests(unittest.TestCase):
    @staticmethod
    def git(root: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout.strip()

    def test_naming_exceptions_and_violations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in [
                "SiteTokens.css", "useDebounce.ts", "ChatPane.tsx",
                "My Document.md", "README.md", "robots.txt", "my_file.json",
                "photo.PNG",
            ]:
                (root / name).write_text("x", encoding="utf-8")
            violations = {
                item["path"]: item["reason"]
                for item in audit_repo.audit_naming(root)
            }
            self.assertEqual(violations["SiteTokens.css"], "mixed/camel/Pascal case")
            self.assertEqual(violations["My Document.md"], "contains spaces")
            self.assertEqual(violations["my_file.json"], "uses underscores instead of hyphens")
            self.assertEqual(violations["photo.PNG"], "uppercase extension")
            self.assertNotIn("useDebounce.ts", violations)
            self.assertNotIn("ChatPane.tsx", violations)
            self.assertNotIn("README.md", violations)
            self.assertNotIn("robots.txt", violations)

    def test_nested_detritus_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            nested = root / "docs" / "attached_assets"
            nested.mkdir(parents=True)
            (nested / "note.txt").write_text("x", encoding="utf-8")
            folders = audit_repo.audit_detritus(root)
            self.assertEqual(folders[0]["folder"], "docs/attached_assets")

    def test_missing_base_fails_visibly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            with self.assertRaises(audit_repo.AuditError):
                audit_repo.ensure_base(root, "origin/main")

    def test_approved_local_deletion_preserves_recovery_state(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        self.git(root, "branch", "feature/recover")
        self.git(root, "checkout", "-q", "feature/recover")
        (root / "feature.txt").write_text("recover me\n", encoding="utf-8")
        self.git(root, "add", "feature.txt")
        self.git(root, "commit", "-qm", "feature commit")
        feature_tip = self.git(root, "rev-parse", "feature/recover")
        self.git(root, "checkout", "-q", "main")
        self.git(root, "update-ref", "refs/archive/existing", "HEAD")
        self.git(root, "update-ref", "refs/recovery/existing", "HEAD")
        self.git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
        (root / "README.md").write_text("stashed work\n", encoding="utf-8")
        self.git(root, "stash", "push", "-qm", "preserve this")

        before = audit_repo.recovery_snapshot(root)
        self.git(root, "update-ref", "refs/recovery/feature-recover", feature_tip)
        self.git(root, "branch", "-D", "feature/recover")
        after = audit_repo.recovery_snapshot(root)
        result = audit_repo.compare_recovery_snapshots(
            before, after, ["feature/recover"]
        )

        self.assertTrue(result["passed"], result["errors"])
        self.assertEqual(result["changed_refs"], [])
        self.assertTrue(result["stashes_unchanged"])
        self.assertEqual(result["unreachable_objects"], [])
        self.assertEqual(
            before["refs"]["refs/archive/existing"],
            after["refs"]["refs/archive/existing"],
        )
        self.assertEqual(
            before["refs"]["refs/remotes/origin/main"],
            after["refs"]["refs/remotes/origin/main"],
        )

    def test_guard_is_read_only_without_exact_approval(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        self.git(root, "branch", "feature/unapproved")
        before = audit_repo.recovery_snapshot(root)
        self.git(root, "branch", "-D", "feature/unapproved")
        after = audit_repo.recovery_snapshot(root)

        result = audit_repo.compare_recovery_snapshots(before, after)

        self.assertFalse(result["passed"])
        self.assertIn(
            "refs/heads/feature/unapproved",
            result["unexpected_removed_refs"],
        )
        self.assertIn(
            "refs/heads/feature/unapproved",
            result["removed_refs"],
        )

    def test_recovery_snapshot_round_trip_and_cli_verification(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        snapshot_path = root / "recovery.json"
        snapshot = audit_repo.recovery_snapshot(root)
        audit_repo.write_recovery_snapshot(snapshot_path, snapshot)
        loaded = audit_repo.read_recovery_snapshot(snapshot_path)

        self.assertEqual(snapshot, loaded)
        self.assertEqual(
            json.loads(snapshot_path.read_text(encoding="utf-8")),
            snapshot,
        )
        cli_snapshot = root / "cli-recovery.json"
        snapshot_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--snapshot-recovery",
                str(cli_snapshot),
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(snapshot_result.returncode, 0, snapshot_result.stderr)
        verify_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--verify-recovery",
                str(cli_snapshot),
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(verify_result.returncode, 0, verify_result.stderr)
        self.assertTrue(
            json.loads(verify_result.stdout)["recovery_guard"]["passed"]
        )

    def test_lost_objects_fail_even_with_approval(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        self.git(root, "branch", "feature/lost")
        self.git(root, "checkout", "-q", "feature/lost")
        (root / "lost.txt").write_text("only on deleted branch\n", encoding="utf-8")
        self.git(root, "add", "lost.txt")
        self.git(root, "commit", "-qm", "unique commit")
        self.git(root, "checkout", "-q", "main")
        before = audit_repo.recovery_snapshot(root)
        self.git(root, "branch", "-D", "feature/lost")
        after = audit_repo.recovery_snapshot(root)

        result = audit_repo.compare_recovery_snapshots(
            before, after, ["feature/lost"]
        )

        self.assertFalse(result["passed"])
        self.assertIn(
            "refs/heads/feature/lost", result["missing_recovery_refs"]
        )
        self.assertTrue(result["unreachable_objects"])

    @classmethod
    def git_repo_from(cls, directory: tempfile.TemporaryDirectory[str]) -> Path:
        root = Path(directory.name)
        cls.git(root, "init", "-q", "-b", "main")
        cls.git(root, "config", "user.email", "test@example.com")
        cls.git(root, "config", "user.name", "Test User")
        (root / "README.md").write_text("initial\n", encoding="utf-8")
        cls.git(root, "add", "README.md")
        cls.git(root, "commit", "-qm", "initial")
        return root


if __name__ == "__main__":
    unittest.main()
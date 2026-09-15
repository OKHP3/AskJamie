from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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

    def test_hosted_branch_parser_preserves_exact_provider_and_ref(self) -> None:
        self.assertEqual(
            audit_repo.parse_hosted_branch("github=agent/feature-one"),
            ("github", "agent/feature-one"),
        )
        self.assertEqual(
            audit_repo.parse_hosted_branch("replit:agent/feature-one"),
            ("replit", "agent/feature-one"),
        )
        with self.assertRaises(audit_repo.AuditError):
            audit_repo.parse_hosted_branch("github")

    def test_hosted_lifecycle_fixture_blocks_unverified_cleanup(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        remote = root / "redacted-hosted.git"
        self.git(root, "init", "--bare", "-q", str(remote))
        self.git(root, "remote", "add", "fixture-host", str(remote))
        for branch in (
            "feature/protected",
            "feature/deployed",
            "feature/pr-associated",
        ):
            self.git(root, "branch", branch)
            self.git(root, "push", "-q", "fixture-host", branch)

        evidence_fixtures = {
            "feature/protected": {
                "protection": {"status": "protected", "source": "fixture"},
                "deployments": {
                    "status": "available", "count": 0, "items": [],
                },
                "pull_requests": {
                    "status": "available", "count": 0, "items": [],
                },
            },
            "feature/deployed": {
                "protection": {"status": "unprotected", "source": "fixture"},
                "deployments": {
                    "status": "available",
                    "count": 1,
                    "items": [{"id": 7, "environment": "production"}],
                },
                "pull_requests": {
                    "status": "available", "count": 0, "items": [],
                },
            },
            "feature/pr-associated": {
                "protection": {"status": "unprotected", "source": "fixture"},
                "deployments": {
                    "status": "available", "count": 0, "items": [],
                },
                "pull_requests": {
                    "status": "available",
                    "count": 1,
                    "items": [{
                        "number": 42,
                        "state": "open",
                        "merged_at": None,
                    }],
                },
            },
        }

        def fixture_evidence(
            _root: Path, _remote_url: str | None, branch: str
        ) -> dict[str, object]:
            return evidence_fixtures[branch]

        with patch.object(
            audit_repo, "github_hosted_evidence", side_effect=fixture_evidence
        ):
            report = audit_repo.audit_hosted_branches(
                root,
                [
                    "fixture-host=feature/missing",
                    "fixture-host=feature/protected",
                    "fixture-host=feature/deployed",
                    "fixture-host=feature/pr-associated",
                    "missing-remote=feature/inaccessible",
                ],
            )
        entries = {entry["ref"]: entry for entry in report["entries"]}

        self.assertEqual(entries["feature/missing"]["classification"], "missing")
        self.assertEqual(
            entries["feature/protected"]["classification"], "present"
        )
        self.assertEqual(
            entries["feature/deployed"]["classification"], "present"
        )
        self.assertEqual(
            entries["feature/pr-associated"]["classification"], "present"
        )
        self.assertEqual(
            entries["feature/inaccessible"]["classification"], "inaccessible"
        )

        for branch in (
            "feature/missing",
            "feature/protected",
            "feature/deployed",
            "feature/pr-associated",
            "feature/inaccessible",
        ):
            self.assertTrue(entries[branch]["deletion_blocked"], branch)

        self.assertIn(
            "hosted-ref-missing",
            entries["feature/missing"]["blocking_reasons"],
        )
        self.assertIn(
            "hosted-ref-protected",
            entries["feature/protected"]["blocking_reasons"],
        )
        self.assertIn(
            "hosted-ref-has-deployments",
            entries["feature/deployed"]["blocking_reasons"],
        )
        self.assertIn(
            "hosted-open-pull-request",
            entries["feature/pr-associated"]["blocking_reasons"],
        )
        self.assertIn(
            "hosted-remote-inaccessible",
            entries["feature/inaccessible"]["blocking_reasons"],
        )
        deletion_candidates = [
            entry["ref"]
            for entry in report["entries"]
            if not entry["deletion_blocked"]
        ]
        self.assertNotIn("feature/inaccessible", deletion_candidates)
        plan = report["cleanup_plan"]
        self.assertEqual(plan["merge"], [])
        self.assertEqual(plan["delete"], [])
        self.assertEqual(
            [(item["provider"], item["ref"]) for item in plan["keep"]],
            [
                ("fixture-host", "feature/deployed"),
                ("fixture-host", "feature/pr-associated"),
                ("fixture-host", "feature/protected"),
            ],
        )
        self.assertEqual(
            [(item["provider"], item["ref"]) for item in plan["review"]],
            [
                ("fixture-host", "feature/missing"),
                ("missing-remote", "feature/inaccessible"),
            ],
        )
        self.assertEqual(
            plan["review"][1]["blocking_reasons"],
            ["hosted-remote-inaccessible"],
        )

    def test_hosted_cleanup_plan_never_deletes_blocked_or_unverified_refs(
        self,
    ) -> None:
        entries = [
            {
                "provider": "origin",
                "ref": "feature/unknown",
                "deletion_blocked": True,
                "blocking_reasons": [
                    "hosted-pull-request-evidence-unknown",
                    "hosted-protection-unknown",
                ],
            },
            {
                "provider": "origin",
                "ref": "feature/protected",
                "deletion_blocked": True,
                "blocking_reasons": ["hosted-ref-protected"],
            },
            {
                "provider": "origin",
                "ref": "feature/verified",
                "deletion_blocked": False,
                "blocking_reasons": [],
            },
        ]

        plan = audit_repo.hosted_cleanup_plan(entries)

        self.assertEqual(plan["merge"], [])
        self.assertEqual(plan["delete"], [])
        self.assertEqual(
            [item["ref"] for item in plan["keep"]],
            ["feature/protected"],
        )
        self.assertEqual(
            plan["review"],
            [{
                "provider": "origin",
                "ref": "feature/unknown",
                "blocking_reasons": [
                    "hosted-protection-unknown",
                    "hosted-pull-request-evidence-unknown",
                ],
            }],
        )

    def test_github_api_fixtures_produce_evidence_and_deletion_holds(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        self.git(
            root,
            "remote",
            "add",
            "origin",
            "https://github.com/example/repository.git",
        )
        tip = self.git(root, "rev-parse", "HEAD")
        branches = ("feature/protected", "feature/unprotected")
        api_fixtures = {
            "repos/example/repository/branches/feature%2Fprotected": {
                "protected": True,
            },
            "repos/example/repository/branches/feature%2Funprotected": {
                "protected": False,
            },
            (
                "repos/example/repository/deployments?"
                "ref=feature%2Fprotected&per_page=100"
            ): [],
            (
                "repos/example/repository/deployments?"
                "ref=feature%2Funprotected&per_page=100"
            ): [{
                "id": 17,
                "sha": tip,
                "ref": "feature/unprotected",
                "environment": "production",
                "created_at": "2026-09-15T10:00:00Z",
                "updated_at": "2026-09-15T10:01:00Z",
                "ignored": "not included in audit evidence",
            }],
            (
                "repos/example/repository/pulls?"
                "state=all&head=example%3Afeature%2Fprotected&per_page=100"
            ): [],
            (
                "repos/example/repository/pulls?"
                "state=all&head=example%3Afeature%2Funprotected&per_page=100"
            ): [
                {
                    "number": 21,
                    "state": "open",
                    "title": "Open work",
                    "merged_at": None,
                    "html_url": "https://github.com/example/repository/pull/21",
                },
                {
                    "number": 20,
                    "state": "closed",
                    "title": "Merged work",
                    "merged_at": "2026-09-14T09:00:00Z",
                    "html_url": "https://github.com/example/repository/pull/20",
                },
                {
                    "number": 19,
                    "state": "closed",
                    "title": "Closed without merge",
                    "merged_at": None,
                    "html_url": "https://github.com/example/repository/pull/19",
                },
            ],
        }

        def hosted_fixture(
            args: list[str], _root: Path
        ) -> subprocess.CompletedProcess[str]:
            if args[:3] == ["git", "ls-remote", "--heads"]:
                branch = args[-1]
                return subprocess.CompletedProcess(
                    args, 0, stdout=f"{tip}\t{branch}\n", stderr=""
                )
            self.assertEqual(args[:2], ["gh", "api"])
            endpoint = args[2]
            self.assertIn(endpoint, api_fixtures)
            return subprocess.CompletedProcess(
                args,
                0,
                stdout=json.dumps(api_fixtures[endpoint]),
                stderr="",
            )

        with patch.object(
            audit_repo, "hosted_command", side_effect=hosted_fixture
        ), patch.object(audit_repo.shutil, "which", return_value="/fixture/gh"):
            report = audit_repo.audit_hosted_branches(
                root, [f"origin={branch}" for branch in branches]
            )

        entries = {entry["ref"]: entry for entry in report["entries"]}
        protected = entries["feature/protected"]
        unprotected = entries["feature/unprotected"]

        self.assertEqual(protected["protection"]["status"], "protected")
        self.assertEqual(protected["protection"]["source"], "github-api")
        self.assertEqual(protected["deployments"]["items"], [])
        self.assertEqual(protected["pull_requests"]["items"], [])
        self.assertEqual(
            protected["blocking_reasons"], ["hosted-ref-protected"]
        )

        self.assertEqual(unprotected["protection"]["status"], "unprotected")
        self.assertEqual(unprotected["deployments"]["count"], 1)
        self.assertEqual(
            unprotected["deployments"]["items"][0],
            {
                "id": 17,
                "sha": tip,
                "ref": "feature/unprotected",
                "environment": "production",
                "created_at": "2026-09-15T10:00:00Z",
                "updated_at": "2026-09-15T10:01:00Z",
            },
        )
        self.assertEqual(unprotected["pull_requests"]["count"], 3)
        self.assertEqual(
            [
                (item["number"], item["state"], item["merged_at"])
                for item in unprotected["pull_requests"]["items"]
            ],
            [
                (21, "open", None),
                (20, "closed", "2026-09-14T09:00:00Z"),
                (19, "closed", None),
            ],
        )
        self.assertEqual(
            unprotected["blocking_reasons"],
            [
                "hosted-closed-unmerged-pull-request",
                "hosted-open-pull-request",
                "hosted-ref-has-deployments",
            ],
        )
        self.assertTrue(protected["deletion_blocked"])
        self.assertTrue(unprotected["deletion_blocked"])
        self.assertTrue(report["deletion_blocked"])
        self.assertEqual(
            report["blocking_entries"],
            ["origin:feature/protected", "origin:feature/unprotected"],
        )

    def test_hosted_present_ref_reports_tip_independently(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        remote = root / "hosted.git"
        self.git(root, "init", "--bare", "-q", str(remote))
        self.git(root, "remote", "add", "hosted", str(remote))
        self.git(root, "branch", "feature/example")
        self.git(root, "push", "-q", "hosted", "feature/example")

        report = audit_repo.audit_hosted_branches(
            root,
            ["hosted=feature/example", "hosted=feature/missing"],
        )
        present, missing = report["entries"]

        self.assertEqual(present["classification"], "present")
        self.assertEqual(present["ref"], "feature/example")
        self.assertEqual(present["tip"], self.git(root, "rev-parse", "HEAD"))
        self.assertEqual(missing["classification"], "missing")
        self.assertTrue(report["deletion_blocked"])

    def test_approved_local_deletion_preserves_recovery_after_maintenance(
        self,
    ) -> None:
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
        self.git(root, "repack", "-ad")
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
        self.assertEqual(
            self.git(root, "rev-parse", "refs/recovery/feature-recover"),
            feature_tip,
        )
        self.git(root, "cat-file", "-e", f"{feature_tip}^{{commit}}")

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

    def test_tampered_protected_ref_snapshot_is_rejected(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        snapshot = audit_repo.recovery_snapshot(root)
        tampered = json.loads(json.dumps(snapshot))
        tampered["refs"]["refs/heads/main"] = "0" * 40

        with self.assertRaisesRegex(
            audit_repo.AuditError, "integrity check failed"
        ):
            audit_repo.validate_recovery_snapshot(tampered)

    def test_tampered_reachable_object_snapshot_is_rejected(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = self.git_repo_from(directory)
        snapshot = audit_repo.recovery_snapshot(root)
        tampered = json.loads(json.dumps(snapshot))
        tampered["reachable_objects"].append("f" * 40)
        tampered["reachable_objects"].sort()

        with self.assertRaisesRegex(
            audit_repo.AuditError, "integrity check failed"
        ):
            audit_repo.compare_recovery_snapshots(tampered, snapshot)

    def test_lost_objects_fail_even_with_approval_after_maintenance(self) -> None:
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
        self.git(root, "repack", "-ad")
        after = audit_repo.recovery_snapshot(root)

        result = audit_repo.compare_recovery_snapshots(
            before, after, ["feature/lost"]
        )

        self.assertFalse(result["passed"])
        self.assertIn(
            "refs/heads/feature/lost", result["missing_recovery_refs"]
        )
        self.assertIn(
            "removed local refs lack recovery refs: refs/heads/feature/lost",
            result["errors"],
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
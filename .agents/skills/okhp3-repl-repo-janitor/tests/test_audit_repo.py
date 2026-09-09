from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit-repo.py"
SPEC = importlib.util.spec_from_file_location("audit_repo", SCRIPT)
assert SPEC and SPEC.loader
audit_repo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_repo)


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class DecisionLedgerTests(unittest.TestCase):
    def make_repo(self) -> tuple[Path, str]:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        git(root, "init", "-q")
        git(root, "branch", "-M", "main")
        git(root, "config", "user.email", "test@example.com")
        git(root, "config", "user.name", "Test User")
        (root / "README.md").write_text("initial\n", encoding="utf-8")
        git(root, "add", "README.md")
        git(root, "commit", "-qm", "initial")
        return root, git(root, "rev-parse", "HEAD")

    def write_ledger(self, root: Path, rows: str, exclusions: str = "") -> Path:
        path = root / "ledger.md"
        path.write_text(
            "\n".join([
                "## Branch decisions",
                "| Branch | Decision | Tip SHA | Evidence |",
                "|---|---|---|---|",
                rows,
                "",
                "## Explicit exclusions and holds",
                exclusions,
            ]),
            encoding="utf-8",
        )
        return path

    def branch_facts(self, root: Path) -> list[dict[str, object]]:
        return audit_repo.audit_branches(root, "main")

    def test_reports_missing_drift_and_stale_rows(self) -> None:
        root, initial = self.make_repo()
        git(root, "branch", "reviewed")
        git(root, "branch", "unreviewed")
        ledger = self.write_ledger(
            root,
            f"| `reviewed` | **keep** | `{initial}` | active |",
            "- `obsolete` — no longer present",
        )
        branches = self.branch_facts(root)
        current = "main"
        result = audit_repo.audit_decision_ledger(root, branches, current, ledger)

        self.assertEqual(result["missing_branches"], ["unreviewed"])
        self.assertEqual(result["tip_sha_drift"], [])
        self.assertEqual(
            result["stale_ledger_rows"],
            [
                {"branch": "obsolete", "kind": "exclusion"},
            ],
        )
        self.assertFalse(result["ok"])

    def test_reports_tip_sha_drift_and_accepts_exclusions(self) -> None:
        root, initial = self.make_repo()
        git(root, "branch", "reviewed")
        git(root, "branch", "held")
        git(root, "checkout", "-q", "main")
        (root / "change.txt").write_text("changed\n", encoding="utf-8")
        git(root, "add", "change.txt")
        git(root, "commit", "-qm", "change")
        git(root, "branch", "-f", "reviewed", "main")
        ledger = self.write_ledger(
            root,
            f"| `reviewed` | **keep** | `{initial}` | active |",
            "- `held` — active work",
        )
        branches = self.branch_facts(root)
        current = "main"
        result = audit_repo.audit_decision_ledger(root, branches, current, ledger)

        self.assertEqual(result["missing_branches"], [])
        self.assertEqual(result["tip_sha_drift"][0]["branch"], "reviewed")
        self.assertEqual(result["stale_ledger_rows"], [])
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
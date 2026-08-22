from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_COMMAND_RE = re.compile(r"scripts/([A-Za-z0-9_.-]+)")
ARCHIVED_SCRIPT_RE = re.compile(r"scripts/archive/[^\s`'\"|;&]+")


def _active_script_allowlist():
    readme = ROOT / "scripts/README.md"
    active_scripts = set()
    for line in readme.read_text(encoding="utf-8").splitlines():
        match = re.search(r"\| `([^`]+)` \| active \|", line)
        if match:
            active_scripts.add(match.group(1))
    return active_scripts


def _assert_release_commands_use_active_scripts(source, text, active_scripts):
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue

        archived_match = ARCHIVED_SCRIPT_RE.search(line)
        if archived_match:
            raise AssertionError(
                f"{source} command references archived script "
                f"{archived_match.group(0)}: {line.strip()}"
            )

        for script_name in SCRIPT_COMMAND_RE.findall(line):
            if script_name not in active_scripts:
                raise AssertionError(
                    f"{source} command references non-active script "
                    f"scripts/{script_name}: {line.strip()}"
                )


def test_release_commands_use_only_documented_active_scripts():
    active_scripts = _active_script_allowlist()
    release_sources = (
        ROOT / ".github/workflows/validate.yml",
        ROOT / "scripts/post-merge.sh",
    )

    for source in release_sources:
        _assert_release_commands_use_active_scripts(
            source.relative_to(ROOT),
            source.read_text(encoding="utf-8"),
            active_scripts,
        )


def test_release_command_guard_names_archived_script_and_command():
    with pytest.raises(
        AssertionError,
        match=r"scripts/archive/old-release\.py.*python3 scripts/archive/old-release\.py",
    ):
        _assert_release_commands_use_active_scripts(
            Path("fixture-workflow.yml"),
            "run: python3 scripts/archive/old-release.py",
            _active_script_allowlist(),
        )


def test_search_index_check_does_not_rewrite_timestamp():
    index = ROOT / "assets/data/search-index.json"
    before = json.loads(index.read_text(encoding="utf-8"))

    result = subprocess.run(
        [sys.executable, "scripts/build-search-index.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    after = json.loads(index.read_text(encoding="utf-8"))
    assert after == before


def test_search_index_rebuild_is_stable_when_content_is_unchanged():
    index = ROOT / "assets/data/search-index.json"
    before = index.read_text(encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/build-search-index.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert index.read_text(encoding="utf-8") == before


def test_pages_artifact_excludes_repository_only_files(tmp_path):
    output = tmp_path / "dist-pages"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/prepare-pages-artifact.py",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (output / "index.html").exists()
    assert (output / "assets/js/app.js").exists()
    assert not (output / ".github").exists()
    assert not (output / "scripts").exists()
    assert not (output / "replit.md").exists()
    assert not (output / ".pytest_cache").exists()
    assert not (output / ".pages-manifest.json").exists()
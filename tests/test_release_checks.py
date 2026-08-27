from __future__ import annotations

import importlib.util
import json
import os
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


def test_site_audit_survives_disappearing_workspace_directory(tmp_path, monkeypatch):
    audit_path = ROOT / "scripts/audit-site.py"
    spec = importlib.util.spec_from_file_location("audit_site", audit_path)
    assert spec and spec.loader
    audit_site = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit_site)

    (tmp_path / "index.html").write_text(
        "<html><body><h1>Public page</h1></body></html>",
        encoding="utf-8",
    )
    (tmp_path / "extra.html").write_text(
        "<html><body><h1>Another public page</h1></body></html>",
        encoding="utf-8",
    )
    disappearing_directory = tmp_path / ".local/secondary_skills/recipe-creator"
    disappearing_directory.mkdir(parents=True)
    (tmp_path / "assets/data").mkdir(parents=True)
    (tmp_path / "assets/data/search-index.json").write_text(
        '{"pages": [{"url": "https://askjamie.bot/"}]}',
        encoding="utf-8",
    )
    (tmp_path / "sitemap.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          <url><loc>https://askjamie.bot/</loc></url>
        </urlset>
        """,
        encoding="utf-8",
    )

    real_scandir = os.scandir

    def flaky_scandir(path):
        if Path(path) == disappearing_directory:
            raise FileNotFoundError(
                2, "No such file or directory", str(disappearing_directory)
            )
        return real_scandir(path)

    monkeypatch.setattr(audit_site, "ROOT", tmp_path)
    monkeypatch.setattr(audit_site.os, "scandir", flaky_scandir)
    monkeypatch.setattr(sys, "argv", ["audit-site.py", "--quiet"])

    assert audit_site.main() == 1
    report = (tmp_path / "assets/docs/audit-report.md").read_text(
        encoding="utf-8"
    )
    assert "**Pages scanned:** 2" in report
    assert "Missing <title>" in report
    assert "Pages on disk not listed in sitemap.xml" in report
    assert "Page on disk not in search index: extra.html" in report


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


def _run_post_merge_with_fake_tools(tmp_path, *, reuse_server, fail_browser=False):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    server_pid_file = tmp_path / "server.pid"
    curl_count_file = tmp_path / "curl.count"

    (bin_dir / "curl").write_text(
        """#!/bin/sh
if [ "${REUSE_SERVER:-0}" = "1" ]; then exit 0; fi
count=0
if [ -f "$CURL_COUNT_FILE" ]; then count=$(cat "$CURL_COUNT_FILE"); fi
count=$((count + 1))
printf '%s' "$count" > "$CURL_COUNT_FILE"
[ "$count" -gt 1 ]
""",
        encoding="utf-8",
    )
    (bin_dir / "python3").write_text(
        """#!/bin/sh
if [ "$1" = "-m" ] && [ "$2" = "http.server" ]; then
  printf '%s' "$$" > "$SERVER_PID_FILE"
  exec sleep 60
fi
exit 0
""",
        encoding="utf-8",
    )
    (bin_dir / "node").write_text(
        """#!/bin/sh
case "$*" in
  *test_js_smoke.spec.mjs*)
    [ "${FAIL_BROWSER:-0}" = "1" ] && exit 9
    ;;
esac
exit 0
""",
        encoding="utf-8",
    )
    for tool in ("curl", "python3", "node"):
        (bin_dir / tool).chmod(0o755)

    env = {
        **os.environ,
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "BROWSER_BASE_URL": "http://127.0.0.1:5000",
        "SERVER_PID_FILE": str(server_pid_file),
        "CURL_COUNT_FILE": str(curl_count_file),
        "REUSE_SERVER": "1" if reuse_server else "0",
        "FAIL_BROWSER": "1" if fail_browser else "0",
    }
    result = subprocess.run(
        ["bash", "scripts/post-merge.sh"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return result, server_pid_file


def test_post_merge_reuses_existing_server_without_starting_another(tmp_path):
    result, server_pid_file = _run_post_merge_with_fake_tools(
        tmp_path, reuse_server=True
    )

    assert result.returncode == 0, result.stderr
    assert "reusing browser server" in result.stdout
    assert "starting temporary browser server" not in result.stdout
    assert not server_pid_file.exists()


def test_post_merge_cleans_up_temporary_server_after_success(tmp_path):
    result, server_pid_file = _run_post_merge_with_fake_tools(
        tmp_path, reuse_server=False
    )

    assert result.returncode == 0, result.stderr
    assert "starting temporary browser server" in result.stdout
    assert server_pid_file.exists()
    pid = int(server_pid_file.read_text(encoding="utf-8"))
    assert subprocess.run(["kill", "-0", str(pid)]).returncode != 0


def test_post_merge_cleans_up_temporary_server_after_browser_failure(tmp_path):
    result, server_pid_file = _run_post_merge_with_fake_tools(
        tmp_path, reuse_server=False, fail_browser=True
    )

    assert result.returncode != 0
    assert server_pid_file.exists()
    pid = int(server_pid_file.read_text(encoding="utf-8"))
    assert subprocess.run(["kill", "-0", str(pid)]).returncode != 0

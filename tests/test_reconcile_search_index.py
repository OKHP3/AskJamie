"""
Test that reconcile_search_index reports both template contamination
and missing-page issues in a single pass — guarding against the
early-return regression fixed in the task-37 audit rewrite.
"""
import importlib.util
import json
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import audit-site.py via importlib (hyphens prevent a normal import).
# ---------------------------------------------------------------------------
_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "audit-site.py"
_spec = importlib.util.spec_from_file_location("audit_site", _SCRIPT)
audit_site = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit_site)  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_index(path: Path, entries: list) -> None:
    """Write a minimal synthetic search-index.json with the given entries."""
    payload = {
        "generated": "2026-01-01T00:00:00Z",
        "site": "https://askjamie.bot",
        "count": len(entries),
        "entries": entries,
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_page(root: Path, rel: str) -> Path:
    """Create a minimal HTML stub at root/rel and return its Path."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("<html><body>stub</body></html>", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Core regression test
# ---------------------------------------------------------------------------

def test_reconcile_catches_template_contamination_and_missing_page(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    A synthetic index that contains both a /assets/templates/ URL and omits
    a real on-disk page must produce BOTH issue types in one call.

    This guards the fix that replaced an early return with an accumulated
    issues list in reconcile_search_index.
    """
    # --- fake repo skeleton ---------------------------------------------------
    (tmp_path / "assets" / "data").mkdir(parents=True)

    # Two real pages on disk
    about = _make_page(tmp_path, "about/index.html")
    contact = _make_page(tmp_path, "contact/index.html")

    # Index: one template URL + only /about/ (contact is on disk but absent)
    _write_index(
        tmp_path / "assets" / "data" / "search-index.json",
        [
            {
                "url": "/assets/templates/template--homepage.html",
                "title": "Homepage Template",
            },
            {
                "url": "/about/",
                "title": "About AskJamie",
            },
            # /contact/ intentionally omitted to trigger missing-page issue
        ],
    )

    # Redirect the module-level ROOT so the function reads our fake index
    monkeypatch.setattr(audit_site, "ROOT", tmp_path)

    issues = audit_site.reconcile_search_index([about, contact])

    template_issues = [i for i in issues if "template-scaffold" in i]
    missing_issues = [i for i in issues if "not in search index" in i]

    assert template_issues, (
        "Expected at least one template-contamination issue but got none.\n"
        f"Full issue list: {issues}"
    )
    assert missing_issues, (
        "Expected at least one missing-page issue but got none.\n"
        f"Full issue list: {issues}"
    )
    # Confirm the template URL is named in the issue text
    assert "/assets/templates/template--homepage.html" in template_issues[0]
    # Confirm the missing page is named in the issue text
    assert "contact" in missing_issues[0]


# ---------------------------------------------------------------------------
# Edge-case: template URL alone (no missing pages)
# ---------------------------------------------------------------------------

def test_reconcile_template_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Template issue appears even when all on-disk pages are indexed."""
    (tmp_path / "assets" / "data").mkdir(parents=True)
    about = _make_page(tmp_path, "about/index.html")

    _write_index(
        tmp_path / "assets" / "data" / "search-index.json",
        [
            {"url": "/assets/templates/template--interior.html", "title": "Interior Template"},
            {"url": "/about/", "title": "About"},
        ],
    )
    monkeypatch.setattr(audit_site, "ROOT", tmp_path)

    issues = audit_site.reconcile_search_index([about])

    assert any("template-scaffold" in i for i in issues)
    assert not any("not in search index" in i for i in issues)


# ---------------------------------------------------------------------------
# Edge-case: missing page alone (no template contamination)
# ---------------------------------------------------------------------------

def test_reconcile_missing_page_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Missing-page issue appears when index omits an on-disk page."""
    (tmp_path / "assets" / "data").mkdir(parents=True)
    about = _make_page(tmp_path, "about/index.html")
    contact = _make_page(tmp_path, "contact/index.html")

    _write_index(
        tmp_path / "assets" / "data" / "search-index.json",
        [
            {"url": "/about/", "title": "About"},
            # contact omitted, no template URLs
        ],
    )
    monkeypatch.setattr(audit_site, "ROOT", tmp_path)

    issues = audit_site.reconcile_search_index([about, contact])

    assert not any("template-scaffold" in i for i in issues)
    assert any("not in search index" in i for i in issues)


# ---------------------------------------------------------------------------
# Edge-case: clean index (no issues expected)
# ---------------------------------------------------------------------------

def test_reconcile_clean_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No issues when the index exactly matches the on-disk pages."""
    (tmp_path / "assets" / "data").mkdir(parents=True)
    about = _make_page(tmp_path, "about/index.html")

    _write_index(
        tmp_path / "assets" / "data" / "search-index.json",
        [{"url": "/about/", "title": "About"}],
    )
    monkeypatch.setattr(audit_site, "ROOT", tmp_path)

    issues = audit_site.reconcile_search_index([about])

    assert issues == [], f"Expected no issues for a clean index; got: {issues}"

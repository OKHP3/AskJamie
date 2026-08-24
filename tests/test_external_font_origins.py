from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-site.py"
spec = importlib.util.spec_from_file_location("validate_site_fonts", SCRIPT)
validate_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_site)  # type: ignore[union-attr]


def test_external_font_check_rejects_google_fonts_in_html(tmp_path, monkeypatch):
    page = tmp_path / "index.html"
    page.write_text(
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans">',
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_site, "ROOT", tmp_path)

    findings = validate_site.check_external_font_origins(page, page.read_text())

    assert len(findings) == 1
    assert findings[0].severity == "ERROR"
    assert findings[0].page == "index.html"
    assert "fonts.googleapis.com" in findings[0].msg


def test_external_font_check_rejects_google_font_file_in_css(tmp_path, monkeypatch):
    stylesheet = tmp_path / "assets" / "css" / "fonts.css"
    stylesheet.parent.mkdir(parents=True)
    stylesheet.write_text(
        '@font-face { src: url("https://fonts.gstatic.com/s/opensans.woff2"); }',
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_site, "ROOT", tmp_path)

    findings = validate_site.check_external_font_origins(
        stylesheet, stylesheet.read_text()
    )

    assert len(findings) == 1
    assert findings[0].page == "assets/css/fonts.css"
    assert "fonts.gstatic.com" in findings[0].msg


def test_external_font_check_allows_documented_non_font_origins(tmp_path, monkeypatch):
    page = tmp_path / "index.html"
    page.write_text(
        """
        <script src="https://www.googletagmanager.com/gtag/js?id=G-EXAMPLE"></script>
        <script type="module" src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"></script>
        """,
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_site, "ROOT", tmp_path)

    assert validate_site.check_external_font_origins(page, page.read_text()) == []


def test_stylesheet_discovery_excludes_repository_only_directories(tmp_path, monkeypatch):
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "site.css").write_text("", encoding="utf-8")
    (tmp_path / ".agents").mkdir()
    (tmp_path / ".agents" / "internal.css").write_text("", encoding="utf-8")
    monkeypatch.setattr(validate_site, "ROOT", tmp_path)

    assert validate_site.find_stylesheet_files() == [tmp_path / "assets" / "site.css"]
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-site.py"
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location("validate_site", SCRIPT)
validate_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_site)  # type: ignore[union-attr]


def test_plain_language_check_ignores_shared_ui_and_accepts_definitions(
    tmp_path, monkeypatch
):
    page = tmp_path / "index.html"
    page.write_text(
        """
        <html><body>
          <header><p>BrandGuard™</p></header>
          <nav><a href="/lens-system/">Lens System</a></nav>
          <main>
            <p>BrandGuard™ (our AI brand-voice protection tool) keeps tone clear.</p>
            <p>OverKill Hill P³™ (the R&amp;D studio behind AskJamie) builds the system.</p>
            <p>Lens System (a structured way to examine a story or challenge) follows.</p>
          </main>
          <footer><p>OKHP³™</p></footer>
        </body></html>
        """,
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_site, "ROOT", tmp_path)

    assert validate_site.check_plain_language_terms(page, page.read_text()) == []


def test_plain_language_check_reports_unexplained_first_use(tmp_path, monkeypatch):
    page = tmp_path / "about" / "index.html"
    page.parent.mkdir()
    page.write_text(
        "<html><body><main><p>BrandGuard™ helps teams publish faster.</p>"
        "</main></body></html>",
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_site, "ROOT", tmp_path)

    findings = validate_site.check_plain_language_terms(page, page.read_text())

    assert len(findings) == 1
    assert findings[0].severity == "ERROR"
    assert findings[0].page == "about/index.html"
    assert "BrandGuard" in findings[0].msg
    assert "plain-language definition" in findings[0].msg


def test_plain_language_check_still_inspects_prose_after_shared_banner(
    tmp_path, monkeypatch
):
    page = tmp_path / "index.html"
    page.write_text(
        """
        <html><body>
          <div class="site-specials">
            <p>BrandGuard™</p>
          </div>
          <main>
            <p>BrandGuard™ helps teams publish faster.</p>
          </main>
        </body></html>
        """,
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_site, "ROOT", tmp_path)

    findings = validate_site.check_plain_language_terms(page, page.read_text())

    assert len(findings) == 1
    assert findings[0].severity == "ERROR"
    assert findings[0].page == "index.html"
    assert "BrandGuard" in findings[0].msg
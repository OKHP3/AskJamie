import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-critical-theme-drift.py"
spec = importlib.util.spec_from_file_location("critical_theme_drift", SCRIPT)
drift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drift)


def test_current_critical_theme_contract_is_clean():
    assert drift.check_contracts(ROOT) == []


def test_shared_property_drift_is_reported(tmp_path):
    (tmp_path / "assets/css").mkdir(parents=True)
    critical = (ROOT / "assets/css/critical-hero.css").read_text(encoding="utf-8")
    theme = (ROOT / "assets/css/theme.css").read_text(encoding="utf-8")
    theme = theme.replace(
        ".askjamie-main .btn-quiet {\n  border-color: #d7d7d7;\n  color: #4b5563;",
        ".askjamie-main .btn-quiet {\n  border-color: #d7d7d7;\n  color: #7b5563;",
        1,
    )
    (tmp_path / "assets/css/critical-hero.css").write_text(critical, encoding="utf-8")
    (tmp_path / "assets/css/theme.css").write_text(theme, encoding="utf-8")

    findings = drift.check_contracts(tmp_path)

    assert any("quiet action: color drifted" in finding for finding in findings)


def test_missing_shared_selector_is_reported(tmp_path):
    (tmp_path / "assets/css").mkdir(parents=True)
    critical = (ROOT / "assets/css/critical-hero.css").read_text(encoding="utf-8")
    theme = (ROOT / "assets/css/theme.css").read_text(encoding="utf-8")
    theme = theme.replace(".askjamie-main .btn-quiet", ".askjamie-main .btn-quiet-renamed")
    (tmp_path / "assets/css/critical-hero.css").write_text(critical, encoding="utf-8")
    (tmp_path / "assets/css/theme.css").write_text(theme, encoding="utf-8")

    findings = drift.check_contracts(tmp_path)

    assert any("quiet action: shared selector missing" in finding for finding in findings)
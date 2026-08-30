from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_HTML = [
    path for path in ROOT.rglob("*.html")
    if not set(path.parts).intersection(
        {".local", ".git", "node_modules", "attached_assets", "dist", "templates", ".agents"}
    )
    and not path.relative_to(ROOT).as_posix().startswith("assets/templates/")
]


def test_public_pages_use_the_google_fonts_runtime_contract():
    stylesheet = re.compile(
        r"https://fonts\.googleapis\.com/css2\?family=Baloo\+2:.*Open\+Sans:.*Kalam:",
        re.IGNORECASE,
    )
    missing = [
        str(path.relative_to(ROOT))
        for path in PUBLIC_HTML
        if not stylesheet.search(path.read_text(encoding="utf-8"))
    ]

    assert not missing, "Google Fonts stylesheet missing from: " + ", ".join(missing)


def test_local_font_bundle_is_not_published():
    assert not (ROOT / "assets/css/fonts.css").exists()
    assert not (ROOT / "assets/fonts").exists()

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_HTML = [
    path for path in ROOT.rglob("*.html")
    if not {"assets", "templates"}.issubset(path.parts)
]


def test_public_pages_do_not_eagerly_load_google_analytics():
    eager_tag = re.compile(
        r"<script\b[^>]*\bsrc=[\"']https://www\.googletagmanager\.com/gtag/js",
        re.IGNORECASE,
    )
    offenders = [
        str(path.relative_to(ROOT))
        for path in PUBLIC_HTML
        if eager_tag.search(path.read_text(encoding="utf-8"))
    ]
    assert not offenders, "GA4 must be loaded only by the consent handler: " + ", ".join(offenders)


def test_consent_handler_and_privacy_control_are_present():
    app_js = (ROOT / "assets/js/app.js").read_text(encoding="utf-8")
    legal = (ROOT / "legal/index.html").read_text(encoding="utf-8")

    assert 'askjamie-analytics-consent' in app_js
    assert 'data-consent="accept"' in app_js
    assert 'data-consent="decline"' in app_js
    assert 'data-privacy-settings' in app_js
    assert 'id="privacy"' in legal
    assert "only after you choose" in legal
from pathlib import Path
import re
import base64
import hashlib


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_HTML = [
    path for path in ROOT.rglob("*.html")
    if not set(path.parts).intersection(
        {".local", ".git", "node_modules", "attached_assets", "dist", "templates", ".agents"}
    )
    and not path.relative_to(ROOT).as_posix().startswith("assets/templates/")
]


def test_public_pages_load_google_analytics_from_the_page_shell():
    eager_tag = re.compile(
        r"<script\b[^>]*\bsrc=[\"']https://www\.googletagmanager\.com/gtag/js",
        re.IGNORECASE,
    )
    missing = [
        str(path.relative_to(ROOT))
        for path in PUBLIC_HTML
        if not eager_tag.search(path.read_text(encoding="utf-8"))
    ]
    assert not missing, "GA4 page-shell script missing from: " + ", ".join(missing)


def test_analytics_tracker_and_privacy_disclosure_are_present():
    app_js = (ROOT / "assets/js/app.js").read_text(encoding="utf-8")
    legal = (ROOT / "legal/index.html").read_text(encoding="utf-8")

    assert "window.askJamieTrack" in app_js
    assert 'typeof window.gtag !== "function"' in app_js
    assert 'id="privacy"' in legal
    assert "Google Analytics 4" in legal
    assert "Browser controls" in legal
    assert "only after you choose" not in legal


def test_public_csp_uses_only_the_scoped_theme_script_hash():
    theme_hash = "sha256-" + base64.b64encode(
        hashlib.sha256(
            b'!function(){var s=localStorage.getItem("okh-theme");document.documentElement.setAttribute("data-theme",s==="dark"||(s!=="light"&&window.matchMedia&&window.matchMedia("(prefers-color-scheme:dark)").matches)?"dark":"light")}();'
        ).digest()
    ).decode()
    csp_re = re.compile(
        r'<meta[^>]+http-equiv=["\']Content-Security-Policy["\'][^>]+content="([^"]+)"',
        re.IGNORECASE,
    )
    theme_script_re = re.compile(r"<script>(.*?)</script>", re.DOTALL)

    for path in PUBLIC_HTML:
        raw = path.read_text(encoding="utf-8")
        policy_match = csp_re.search(raw)
        assert policy_match, f"missing CSP on {path.relative_to(ROOT)}"
        script_src = next(
            directive for directive in policy_match.group(1).split(";")
            if directive.strip().startswith("script-src")
        )
        assert "'unsafe-inline'" not in script_src, (
            f"broad inline script permission remains on {path.relative_to(ROOT)}"
        )
        assert theme_hash in script_src, (
            f"scoped theme hash missing from {path.relative_to(ROOT)}"
        )
        theme_scripts = [
            body for body in theme_script_re.findall(raw) if "okh-theme" in body
        ]
        assert len(theme_scripts) == 1, (
            f"expected one theme bootstrap on {path.relative_to(ROOT)}"
        )
        assert hashlib.sha256(theme_scripts[0].encode()).digest() == (
            base64.b64decode(theme_hash.removeprefix("sha256-"))
        ), f"theme hash drifted on {path.relative_to(ROOT)}"

    # A Content-Security-Policy-Report-Only header used to trial this same
    # hash-scoped, no-'unsafe-inline' script-src before it was rolled out.
    # It was retired when scripts/csp.py + scripts/generate-csp.py (the
    # shared policy generator ported from overkill-hill) started producing
    # _headers directly: the enforced policy above already is the hardened
    # state the report-only header used to preview, and neither
    # overkill-hill nor glee-fullytools carry a report-only header or test
    # for one. Nothing left to assert here.

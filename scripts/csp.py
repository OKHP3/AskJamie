#!/usr/bin/env python3
"""Canonical CSP policies and page classification for the static site.

Ported from OverKill Hill P3's scripts/csp.py so all three OKHP3 sites
(overkillhill.com, askjamie.bot, glee-fully.tools) keep the same CSP
architecture: script-src is hash-locked from the actual inline scripts on
each page; style-src is hash-locked the same way EXCEPT for pages that
render a live Mermaid diagram, which get a scoped 'unsafe-inline' style
grant instead, because Mermaid generates its own inline styles and <style>
blocks at render time in the browser and no build-time hash can ever cover
that. script-src is identical in rigor across every page class.
"""
from __future__ import annotations

import base64
import hashlib
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_FILE = ROOT / "config" / "csp-policies.json"
META_RE = re.compile(
    r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=(["\'])(.*?)\1\s*/?>',
    re.IGNORECASE,
)


def page_class(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel in {"404.html", "under-construction.html", "search/index.html"}:
        return "utility"
    source = path.read_text(encoding="utf-8", errors="replace")
    # Pages that host another application need an explicit frame destination.
    is_embed = "<iframe" in source
    # Mermaid renders its own inline styles and <style> blocks at runtime, per
    # diagram, per page load. A build-time hash allowlist can never cover
    # that, so pages with a live diagram get a scoped style-src relaxation
    # instead of silently losing their theme styling under a hash-only
    # policy. script-src is unaffected -- these pages stay just as
    # hash-locked for scripts as every other page. The two conditions are
    # independent, so a page could in principle need both allowances at once.
    is_diagram = _renders_live_mermaid(source)
    if is_embed and is_diagram:
        return "embed-diagram"
    if is_embed:
        return "embed"
    if is_diagram:
        return "diagram"
    return "standard"


def _renders_live_mermaid(source: str) -> bool:
    return bool(re.search(r"""class=["'][^"']*\bmermaid\b""", source, re.IGNORECASE))


def sha256_source(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return "'sha256-" + base64.b64encode(digest).decode("ascii") + "'"


def inline_sources(path: Path) -> tuple[set[str], set[str]]:
    source = path.read_text(encoding="utf-8", errors="replace")
    script_hashes = {
        sha256_source(match.group(1))
        for match in re.finditer(r"<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", source, re.I)
        if match.group(1).strip()
    }
    style_attr_hashes = {
        sha256_source(html.unescape(match.group(2)))
        for match in re.finditer(r'\bstyle=(["\'])(.*?)\1', source, re.I)
    }
    return script_hashes, style_attr_hashes


def all_pages() -> list[Path]:
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return sorted(
        ROOT / name
        for name in tracked.stdout.splitlines()
        if not name.startswith(("assets/templates/", "assets/partials/", "dist-pages/", "dist/"))
    )


def build_policies() -> dict[str, str]:
    classes = ("standard", "embed", "utility", "diagram", "embed-diagram")
    hashes: dict[str, set[str]] = {kind: set() for kind in classes}
    style_hashes: dict[str, set[str]] = {kind: set() for kind in classes}
    for page in all_pages():
        scripts, styles = inline_sources(page)
        kind = page_class(page)
        hashes[kind].update(scripts)
        style_hashes[kind].update(styles)

    common = (
        "default-src 'self'; "
        "script-src 'self' https://www.googletagmanager.com "
        + " ".join(sorted(hashes["standard"]))
        + "; script-src-attr 'none'; "
        "style-src 'self' https://fonts.googleapis.com "
        + " ".join(sorted(style_hashes["standard"]))
        + "; style-src-attr 'unsafe-hashes' "
        + " ".join(sorted(style_hashes["standard"]))
        + "; font-src 'self' data: https://fonts.gstatic.com; "
        "img-src 'self' data: https://www.googletagmanager.com; "
        "connect-src 'self' https://www.google.com https://www.google-analytics.com https://*.google-analytics.com https://www.googletagmanager.com; "
        "object-src 'none'; base-uri 'self'; form-action 'self'; "
        "manifest-src 'self'; upgrade-insecure-requests"
    )

    # Keep each class explicit even where it currently shares most directives.
    # This prevents an embed allowance from silently spreading to ordinary pages.
    #
    # "diagram_style" is a scoped style-src/style-src-attr relaxation for
    # page classes that render a live Mermaid diagram. Hashes and
    # 'unsafe-inline' must not appear together in the same directive -- CSP
    # ignores 'unsafe-inline' whenever a hash-source is present -- so the
    # style hashes are omitted entirely for these classes rather than added
    # alongside it.
    policies = {"standard": common}
    class_config = (
        ("embed", "https://okhp3.github.io", False),
        ("utility", "", False),
        ("diagram", "", True),
        ("embed-diagram", "https://okhp3.github.io", True),
    )
    for kind, frame, diagram_style in class_config:
        if diagram_style:
            style_directives = (
                "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
                "style-src-attr 'unsafe-inline'; "
            )
        else:
            style_directives = (
                "style-src 'self' https://fonts.googleapis.com "
                + " ".join(sorted(style_hashes[kind]))
                + "; style-src-attr 'unsafe-hashes' "
                + " ".join(sorted(style_hashes[kind]))
                + "; "
            )
        policy = (
            "default-src 'self'; "
            "script-src 'self' https://www.googletagmanager.com "
            + " ".join(sorted(hashes[kind]))
            + "; script-src-attr 'none'; "
            + style_directives
            + "font-src 'self' data: https://fonts.gstatic.com; "
            "img-src 'self' data: https://www.googletagmanager.com; "
            "connect-src 'self' https://www.google.com https://www.google-analytics.com https://*.google-analytics.com https://www.googletagmanager.com; "
            + (f"frame-src 'self' {frame}; " if frame else "")
            + "object-src 'none'; base-uri 'self'; form-action 'self'; "
            "manifest-src 'self'; upgrade-insecure-requests"
        )
        policies[kind] = policy
    return policies


def build_edge_policy() -> str:
    """Build the enforcing header policy, broad enough for every page class.

    style-src stays 'unsafe-inline' rather than hash-only: this envelope has
    to be broad enough to cover the "diagram" and "embed-diagram" page
    classes too (see csp.build_policies), and a hash-source alongside
    'unsafe-inline' in the same directive causes browsers to ignore
    'unsafe-inline' entirely. Per-page meta policies remain the real,
    tighter enforcement for every other page; this header is only ever
    meant to be a permissive outer bound, matching overkillhill.com's own
    scripts/csp.py::build_edge_policy.
    """
    scripts: set[str] = set()
    for page in all_pages():
        page_scripts, _ = inline_sources(page)
        scripts.update(page_scripts)
    return (
        "default-src 'self'; script-src 'self' https://www.googletagmanager.com "
        + " ".join(sorted(scripts))
        + "; script-src-attr 'none'; style-src 'self' 'unsafe-inline'; "
        "style-src-attr 'unsafe-inline'; font-src 'self'; "
        "img-src 'self' data: https://www.googletagmanager.com; "
        "connect-src 'self' https://www.google.com https://www.google-analytics.com https://*.google-analytics.com https://www.googletagmanager.com; "
        "object-src 'none'; base-uri 'self'; form-action 'self'; "
        "manifest-src 'self'; upgrade-insecure-requests"
    )


def meta_policy(path: Path) -> str | None:
    source = path.read_text(encoding="utf-8", errors="replace")
    match = META_RE.search(source)
    return match.group(2) if match else None


def render_meta(policy: str) -> str:
    return f'<meta http-equiv="Content-Security-Policy" content="{policy}" />'

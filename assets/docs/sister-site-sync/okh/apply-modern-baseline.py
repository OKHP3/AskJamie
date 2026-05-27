#!/usr/bin/env python3
"""
apply-modern-baseline.py -- one-shot upgrade pass for overkillhill.com.

STAGED COPY -- ready to drop into the OKHP3/OverKill-Hill repo.

Per-site constants that were changed from the AskJamie original:
  - THEME_COLOR_LEGACY_RE  pattern changed to match OKH brand orange (#c46a2c)
  - THEME_COLOR_PAIR       light/dark values changed to OKH palette

VERIFY before first run:
  1. Open any OKH HTML page and search for name="theme-color".
     If the content value is NOT #c46a2c, update THEME_COLOR_LEGACY_RE
     to match whatever value is actually present.
  2. Confirm the THEME_COLOR_PAIR light/dark split:
       light = #f6f2ee  (okh-paper, the light-mode page background)
       dark  = #c46a2c  (okh-orange, the brand accent for dark browser chrome)
     Adjust if the OKH site uses different values.
  3. Run (dry pass -- check output, no changes expected if already upgraded):
       python3 scripts/apply-modern-baseline.py
     Re-run to confirm idempotency:
       python3 scripts/apply-modern-baseline.py
     Target: "Files modified: 0 of N" on the second run.
  4. Run:  python3 scripts/audit-site.py --quiet
     Target: 0 issues.

CSP allow-list is verbatim from AskJamie -- all three sister sites share
the same tech stack (GA4 via GTM, Mermaid ESM from cdn.jsdelivr.net,
Google Fonts). No site-specific domains needed.

Source: AskJamie scripts/apply-modern-baseline.py (2026-05-27)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".local", "attached_assets", "node_modules", ".cache",
                ".git", ".vscode", "templates"}

# ---------------------------------------------------------------------------
# SITE-AGNOSTIC: CSP (identical across all three sister sites)
# ---------------------------------------------------------------------------

CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' "
    "https://www.googletagmanager.com https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https:; "
    "connect-src 'self' https://www.google-analytics.com "
    "https://*.google-analytics.com https://www.googletagmanager.com; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)

REFERRER_META = '<meta name="referrer" content="strict-origin-when-cross-origin" />'
CSP_META      = f'<meta http-equiv="Content-Security-Policy" content="{CSP}" />'

VIEWPORT_RE = re.compile(
    r'(\s*<meta\s+name="viewport"\s+content="[^"]+"\s*/?>)',
    re.IGNORECASE
)

# ---------------------------------------------------------------------------
# PER-SITE: theme-color split  <-- edit these when copying to a new sister site
# ---------------------------------------------------------------------------

# Matches the old single-value theme-color tag so it can be upgraded to a
# light/dark media-queried pair.
#
# VERIFY: check actual OKH HTML pages for their current theme-color value.
#   If the content is NOT #c46a2c, update the pattern below.
#
# OKH brand orange: #c46a2c (--okh-orange, the primary accent color)
THEME_COLOR_LEGACY_RE = re.compile(
    r'<meta\s+name="theme-color"\s+content="#c46a2c"\s*/?>',
    re.IGNORECASE
)

# Split into a light/dark pair:
#   light = #f6f2ee  (okh-paper, the OKH light-mode page background)
#   dark  = #c46a2c  (okh-orange, the OKH brand accent for dark browser chrome)
#
# VERIFY: confirm these match the OKH design intent before running.
THEME_COLOR_PAIR = (
    '<meta name="theme-color" content="#f6f2ee" media="(prefers-color-scheme: light)" />\n'
    '    <meta name="theme-color" content="#c46a2c" media="(prefers-color-scheme: dark)" />'
)

# ---------------------------------------------------------------------------
# SITE-AGNOSTIC LOGIC (copy verbatim across all sister sites)
# ---------------------------------------------------------------------------

def iter_html() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def add_security_meta(src: str) -> tuple[str, list[str]]:
    """Insert security meta tags right after <meta name=viewport>. Idempotent."""
    actions = []
    if 'name="referrer"' in src and 'http-equiv="Content-Security-Policy"' in src:
        return src, actions
    m = VIEWPORT_RE.search(src)
    if not m:
        return src, ["WARN: no <meta viewport> found -- security meta not added"]
    insert = ""
    indent = "    "
    if 'name="referrer"' not in src:
        insert += f"\n{indent}{REFERRER_META}"
        actions.append("added referrer meta")
    if 'http-equiv="Content-Security-Policy"' not in src:
        insert += f"\n{indent}{CSP_META}"
        actions.append("added CSP meta")
    if insert:
        src = src[:m.end()] + insert + src[m.end():]
    return src, actions


def split_theme_color(src: str) -> tuple[str, list[str]]:
    """Split single theme-color tag into a light/dark media pair. Idempotent."""
    if 'media="(prefers-color-scheme:' in src:
        return src, []  # already migrated
    if THEME_COLOR_LEGACY_RE.search(src):
        src = THEME_COLOR_LEGACY_RE.sub(THEME_COLOR_PAIR, src, count=1)
        return src, ["split theme-color into light/dark media pair"]
    return src, []


def upgrade_images(src: str) -> tuple[str, list[str]]:
    """Add fetchpriority to LCP img + loading=lazy to all others. Idempotent."""
    actions = []

    # Find the <main>...</main> region (first one wins; site uses one main)
    main_match = re.search(r'<main\b[^>]*>(.*?)</main>', src, re.DOTALL | re.IGNORECASE)
    lcp_img_position: int | None = None
    if main_match:
        first_inside = re.search(r'<img\b[^>]*>', main_match.group(1))
        if first_inside:
            lcp_img_position = main_match.start(1) + first_inside.start()

    out_parts = []
    last      = 0
    lazy_added = 0
    fp_added   = 0
    for m in re.finditer(r'<img\b[^>]*>', src):
        out_parts.append(src[last:m.start()])
        tag    = m.group(0)
        is_lcp = (m.start() == lcp_img_position)

        if is_lcp:
            # LCP img: fetchpriority="high" + loading="eager"
            if 'fetchpriority=' not in tag:
                tag = re.sub(r'(\s*/?>)$', r' fetchpriority="high"\1', tag, count=1)
                fp_added += 1
            if 'loading=' not in tag:
                tag = re.sub(r'(\s*/?>)$', r' loading="eager"\1', tag, count=1)
        else:
            # Non-LCP: add loading="lazy" if missing
            if 'loading=' not in tag:
                tag = re.sub(r'(\s*/?>)$', r' loading="lazy"\1', tag, count=1)
                lazy_added += 1

        out_parts.append(tag)
        last = m.end()
    out_parts.append(src[last:])
    new_src = "".join(out_parts)

    if lazy_added:
        actions.append(f'added loading="lazy" to {lazy_added} img(s)')
    if fp_added:
        actions.append(f'added fetchpriority="high" to {fp_added} LCP img')
    return new_src, actions


def main() -> int:
    files = iter_html()
    print(f"Scanning {len(files)} HTML files...\n")
    touched = 0
    for path in files:
        src      = path.read_text(encoding="utf-8", errors="replace")
        original = src
        all_actions: list[str] = []

        src, acts = add_security_meta(src)
        all_actions.extend(acts)

        src, acts = split_theme_color(src)
        all_actions.extend(acts)

        src, acts = upgrade_images(src)
        all_actions.extend(acts)

        if src != original:
            path.write_text(src, encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            print(f"  [MOD] {rel}")
            for a in all_actions:
                print(f"        - {a}")
            touched += 1
        else:
            rel = path.relative_to(ROOT).as_posix()
            print(f"  [ok ] {rel}")

    print(f"\nDone. Files modified: {touched} of {len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

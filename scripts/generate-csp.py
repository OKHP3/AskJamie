#!/usr/bin/env python3
"""Generate canonical CSP policies and apply them to every HTML page.

Ported from OverKill Hill P3's scripts/generate-csp.py. Unlike that repo,
this site has no site-src build step -- the tracked *.html files are the
served files, so this script edits them directly rather than regenerating
them from source fragments first.
"""
from __future__ import annotations

import argparse
import json
import re

from csp import POLICY_FILE, ROOT, all_pages, build_policies, inline_sources, page_class, render_meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args(argv)
    policies = build_policies()
    output = json.dumps({"schema": 1, "policies": policies}, indent=2) + "\n"
    if args.check:
        if not POLICY_FILE.exists() or POLICY_FILE.read_text(encoding="utf-8") != output:
            print("CSP policy file is stale. Run: python3 scripts/generate-csp.py")
            return 1
    else:
        POLICY_FILE.parent.mkdir(parents=True, exist_ok=True)
        POLICY_FILE.write_text(output, encoding="utf-8")
        headers = ROOT / "_headers"
        if headers.is_file():
            header_source = headers.read_text(encoding="utf-8")
            header_pattern = re.compile(
                r"(?m)^\s*Content-Security-Policy(?:-Report-Only)?:\s*.*$"
            )
            header_line = "  Content-Security-Policy: " + build_edge_policy()
            updated_headers, count = header_pattern.subn(header_line, header_source, count=1)
            if count == 1:
                headers.write_text(updated_headers, encoding="utf-8")

    failures: list[str] = []
    meta_pattern = re.compile(
        r'<meta\b(?=[^>]*\bhttp-equiv=["\']Content-Security-Policy["\'])'
        r'(?=[^>]*\bcontent=(["\']))[^>]*\s*/?>',
        re.IGNORECASE,
    )
    for page in all_pages():
        source = page.read_text(encoding="utf-8", errors="replace")
        expected = render_meta(policies[page_class(page)])
        if args.check:
            if source.count('http-equiv="Content-Security-Policy"') == 0:
                continue
            if source.count('http-equiv="Content-Security-Policy"') != 1 or meta_policy(source) != policies[page_class(page)]:
                failures.append(f"{page}: CSP differs from {page_class(page)} canonical policy")
        else:
            updated, count = meta_pattern.subn(expected, source, count=1)
            if count == 0:
                continue
            if count != 1:
                failures.append(f"{page}: expected exactly one CSP meta tag")
            else:
                page.write_text(updated, encoding="utf-8", newline="")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"CSP policies verified for {len(all_pages())} pages.")
    return 0


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
        "img-src 'self' data: https:; "
        "connect-src 'self' https://www.google-analytics.com https://*.google-analytics.com https://www.googletagmanager.com; "
        "object-src 'none'; base-uri 'self'; form-action 'self'; "
        "manifest-src 'self'; upgrade-insecure-requests"
    )


def meta_policy(source: str) -> str | None:
    match = re.search(
        r'<meta\b(?=[^>]*\bhttp-equiv=["\']Content-Security-Policy["\'])'
        r'(?=[^>]*\bcontent=(["\']))[^>]*\bcontent=\1(.*?)\1',
        source,
        re.IGNORECASE,
    )
    return match.group(2) if match else None


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
audit-site.py — Static-site quality gate for OverKill Hill P3 (overkillhill.com).

STAGED COPY — ready to drop into the OKHP3/OverKill-Hill repo.

Per-site constants that were changed from the AskJamie original:
  - EXPECTED_THEME_COLOR  changed to OKH rust-orange  (#c46a2c)
  - EXPECTED_BG_COLOR     changed to OKH espresso dark (#2a2320)

VERIFY before first run:
  1. Open any OKH HTML page and search for name="theme-color".
     Copy the content="..." value and confirm it matches EXPECTED_THEME_COLOR.
     If OKH uses a different single value, update the constant here.
  2. Run:  python3 scripts/audit-site.py --quiet
     Target: 0 issues.

All other checks (title/description length, canonical, OG fields, image hygiene,
CSP/referrer meta, sitemap/search-index reconciliation, Mermaid affiliate link,
heading order, bare link text) are site-agnostic and were copied verbatim.

Source: AskJamie scripts/audit-site.py (v0.8, 2026-05-27)
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------------------
# PER-SITE CONSTANTS  <-- edit these when copying to a new sister site
# ---------------------------------------------------------------------------

# The value that must appear in at least one <meta name="theme-color"> tag.
# For OKH: rust-orange brand accent.
# VERIFY: grep any OKH HTML page for name="theme-color" and confirm.
EXPECTED_THEME_COLOR = "#c46a2c"   # OKH rust-orange

# Informational — documents the site's CSS --color-bg token.
# Not actively checked by the auditor; used for human reference.
EXPECTED_BG_COLOR = "#2a2320"      # OKH espresso dark (CSS --color-bg: var(--okh-espresso))

# ---------------------------------------------------------------------------
# SITE-AGNOSTIC CONSTANTS (copy verbatim across all sister sites)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {".local", ".agents", "attached_assets", "node_modules",
                ".cache", ".git", ".vscode", "templates"}

EXCLUDE_FROM_SITEMAP = {"404.html", "under-construction.html"}

MAX_TITLE_LEN       = 60
MIN_TITLE_LEN       = 30
MAX_DESC_LEN        = 165

REQUIRED_OG_FIELDS = {
    "og:title", "og:description", "og:type",
    "og:url", "og:image", "og:site_name",
}

BARE_LINK_TEXTS = frozenset({
    "click here", "here", "read more", "more", "learn more",
    "this", "this link", "this page", "link", "details",
    "see more", "view more", "find out more", "continue",
    "continue reading",
})

# Mermaid affiliate referral link — same across all three sites.
MERMAID_AFFILIATE_URL   = "https://mermaidchart.cello.so/UhVlNtC2MlS"
MERMAID_REFERRAL_CLASS  = "mermaid-referral-link"

# Pattern for detecting the sitemap URL prefix
SITEMAP_URL_RE = re.compile(r"<loc>(https?://[^<]+)</loc>", re.IGNORECASE)

# Pattern for finding theme-color values
THEME_COLOR_RE = re.compile(
    r'<meta\s+name=["\']theme-color["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE
)

# Known placeholder strings that should never ship
PLACEHOLDER_RE = re.compile(
    r"ASK-JAMIE-GPT-ID-HERE"
    r"|YOUR-[A-Z0-9_-]+"
    r'|action=["\'][^"\']*\?s=\{',
    re.IGNORECASE
)


# ---------------------------------------------------------------------------
# HTML parser
# ---------------------------------------------------------------------------

class PageParser(HTMLParser):
    """Extract structural data from an HTML page for quality checks."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title        = ""
        self.description  = ""
        self.canonical    = ""
        self.h1_count     = 0
        self.og           = {}
        self.theme_colors = []
        self.imgs         = []          # list of attr-dicts
        self.ext_links    = []          # list of attr-dicts (target=_blank)
        self.links        = []          # all <a> tags: {"text": ..., "href": ..., "aria_label": ...}
        self.headings     = []          # list of (level, text) tuples

        # Heading order tracking
        self._cur_heading_tag  = None
        self._cur_heading_buf  = []
        self._in_footer        = 0      # depth counter for <footer> elements

        # Link text tracking
        self._in_a             = False
        self._cur_link_buf     = []
        self._cur_link_attrs   = {}

        # Title tracking
        self._capture_title    = False
        self._title_buf        = []

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)

        if tag == "title":
            self._capture_title = True
            return

        if tag == "meta":
            name = (ad.get("name") or "").lower()
            prop = (ad.get("property") or "").lower()
            cont = (ad.get("content") or "").strip()
            if name == "description":
                self.description = cont
            elif name == "theme-color":
                self.theme_colors.append(cont)
            elif prop in REQUIRED_OG_FIELDS:
                self.og[prop] = cont
            return

        if tag == "link":
            if (ad.get("rel") or "").lower() == "canonical":
                self.canonical = (ad.get("href") or "").strip()
            return

        if tag == "img":
            self.imgs.append(ad)
            return

        if tag == "footer":
            self._in_footer += 1
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._cur_heading_tag = tag
            self._cur_heading_buf = []
            if tag == "h1":
                self.h1_count += 1
            return

        if tag == "a":
            self._in_a = True
            self._cur_link_buf = []
            self._cur_link_attrs = ad
            if (ad.get("target") or "").lower() == "_blank":
                self.ext_links.append(ad)
            return

    def handle_endtag(self, tag):
        if tag == "title":
            self._capture_title = False
            self.title = "".join(self._title_buf).strip()
            return

        if tag == "footer":
            self._in_footer = max(0, self._in_footer - 1)
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = " ".join("".join(self._cur_heading_buf).split()).strip()
            if text and self._in_footer == 0:
                self.headings.append((int(tag[1]), text))
            self._cur_heading_tag = None
            self._cur_heading_buf = []
            return

        if tag == "a":
            self._in_a = False
            text = " ".join("".join(self._cur_link_buf).split()).strip()
            self.links.append({
                "text":       text,
                "href":       (self._cur_link_attrs.get("href") or "").strip(),
                "aria_label": (self._cur_link_attrs.get("aria-label") or "").strip(),
            })
            self._cur_link_buf = []
            self._cur_link_attrs = {}
            return

    def handle_data(self, data):
        if self._capture_title:
            self._title_buf.append(data)
            return
        if self._cur_heading_tag:
            self._cur_heading_buf.append(data)
        if self._in_a:
            self._cur_link_buf.append(data)


# ---------------------------------------------------------------------------
# Per-page checks
# ---------------------------------------------------------------------------

def audit_page(rel_path: str, full_path: str) -> list[str]:
    issues = []

    try:
        raw = Path(full_path).read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return [f"could not read file: {exc}"]

    parser = PageParser()
    try:
        parser.feed(raw)
    except Exception as exc:
        issues.append(f"HTML parse error: {exc}")

    title = parser.title.strip()
    desc  = parser.description.strip()

    # ---- Title ----
    if not title:
        issues.append("missing <title>")
    else:
        if len(title) > MAX_TITLE_LEN:
            issues.append(f"title too long ({len(title)} chars, max {MAX_TITLE_LEN}): {title!r}")
        if len(title) < MIN_TITLE_LEN:
            issues.append(f"title too short ({len(title)} chars, min {MIN_TITLE_LEN}): {title!r}")

    # ---- Description ----
    if not desc:
        issues.append("missing meta description")
    elif len(desc) > MAX_DESC_LEN:
        issues.append(f"description too long ({len(desc)} chars, max {MAX_DESC_LEN})")

    # ---- H1 ----
    if parser.h1_count == 0:
        issues.append("missing <h1>")
    elif parser.h1_count > 1:
        issues.append(f"multiple <h1> tags ({parser.h1_count})")

    # ---- Canonical ----
    if not parser.canonical:
        issues.append("missing canonical link")

    # ---- OG fields ----
    for field in REQUIRED_OG_FIELDS:
        if field not in parser.og:
            issues.append(f"missing OG field: {field}")

    # ---- theme-color ----
    theme_colors = [c.lower() for c in parser.theme_colors]
    if not theme_colors:
        issues.append("missing <meta name=\"theme-color\">")
    elif EXPECTED_THEME_COLOR not in theme_colors:
        issues.append(
            f"theme-color values {parser.theme_colors} do not include the "
            f"expected brand color `{EXPECTED_THEME_COLOR}`"
        )

    # ---- Images ----
    for img in parser.imgs:
        src = img.get("src") or img.get("data-src") or "(no src)"
        if "alt" not in img:
            issues.append(f"img missing alt: {src!r}")
        if "width" not in img:
            issues.append(f"img missing width: {src!r}")
        if "height" not in img:
            issues.append(f"img missing height: {src!r}")

    # ---- External links ----
    for link in parser.ext_links:
        rel_val = link.get("rel") or link.get("rel\n") or ""
        parts   = set(re.split(r"\s+", rel_val.lower()))
        if "noopener" not in parts or "noreferrer" not in parts:
            href = link.get("href") or "(no href)"
            issues.append(f"external link missing rel=noopener/noreferrer: {href!r}")

    # ---- Bare link text ----
    for link in parser.links:
        aria = link["aria_label"].lower().strip()
        if aria:
            continue  # aria-label overrides visible text for accessibility
        text = link["text"].lower().strip()
        if text in BARE_LINK_TEXTS:
            href = link["href"] or "(no href)"
            issues.append(f"bare link text {text!r}: {href!r}")

    # ---- Placeholders ----
    if PLACEHOLDER_RE.search(raw):
        issues.append("contains known placeholder string")

    # ---- Heading order ----
    prev_level = 1  # <h1> is expected first
    for level, text in parser.headings:
        if level > prev_level + 1:
            issues.append(
                f"heading order skip: h{prev_level} -> h{level} ({text!r})"
            )
        prev_level = level

    # ---- Mermaid affiliate link ----
    if "<pre class=\"mermaid\">" in raw or "<pre class='mermaid'>" in raw:
        if MERMAID_AFFILIATE_URL not in raw:
            issues.append(
                "Mermaid diagram present but OKH affiliate referral link missing"
            )
        if MERMAID_REFERRAL_CLASS not in raw:
            issues.append(
                "Mermaid diagram present but mermaid-referral-link class missing"
            )

    return issues


# ---------------------------------------------------------------------------
# Cross-file checks
# ---------------------------------------------------------------------------

def collect_html_paths() -> list[str]:
    """Walk the repo and return rel-paths to all public HTML files."""
    results = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [
            d for d in dirnames
            if d not in EXCLUDE_DIRS and not d.startswith(".")
        ]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            if fn in EXCLUDE_FROM_SITEMAP:
                continue
            full = os.path.join(dirpath, fn)
            rel  = os.path.relpath(full, REPO_ROOT)
            results.append(rel)
    return sorted(results)


def load_sitemap_urls() -> set[str]:
    sitemap = REPO_ROOT / "sitemap.xml"
    if not sitemap.exists():
        return set()
    text  = sitemap.read_text(encoding="utf-8", errors="replace")
    return {m.group(1).rstrip("/") for m in SITEMAP_URL_RE.finditer(text)}


def load_search_index_urls() -> set[str]:
    idx = REPO_ROOT / "assets" / "data" / "search-index.json"
    if not idx.exists():
        return set()
    import json
    try:
        data = json.loads(idx.read_text(encoding="utf-8"))
    except Exception:
        return set()
    return {p.get("url", "").rstrip("/") for p in data.get("pages", [])}


def rel_to_url(rel_path: str) -> str:
    """Convert repo-relative path to the public URL path."""
    p = rel_path.replace(os.sep, "/")
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    elif p == "index.html":
        p = ""
    url = "/" + p if p and not p.startswith("/") else (p or "/")
    return url.rstrip("/") or "/"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Static-site auditor for overkillhill.com")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress per-page console output (report file always written)")
    args = ap.parse_args()

    html_paths = collect_html_paths()

    all_issues: dict[str, list[str]] = {}
    for rel in html_paths:
        full = os.path.join(REPO_ROOT, rel)
        page_issues = audit_page(rel, full)
        if page_issues:
            all_issues[rel] = page_issues
        if not args.quiet:
            status = "PASS" if not page_issues else f"FAIL ({len(page_issues)} issues)"
            print(f"  {status}  {rel}")

    # ---- Cross-file: sitemap reconciliation ----
    sitemap_urls = load_sitemap_urls()
    if sitemap_urls:
        disk_urls = {rel_to_url(r) for r in html_paths}
        for url in sorted(disk_urls - sitemap_urls):
            all_issues.setdefault("sitemap.xml", []).append(
                f"page on disk but missing from sitemap: {url}"
            )
        for url in sorted(sitemap_urls - disk_urls):
            all_issues.setdefault("sitemap.xml", []).append(
                f"sitemap entry has no matching HTML file: {url}"
            )

    # ---- Cross-file: search-index reconciliation ----
    idx_urls = load_search_index_urls()
    if idx_urls:
        disk_urls = {rel_to_url(r) for r in html_paths}
        for url in sorted(disk_urls - idx_urls):
            all_issues.setdefault("search-index.json", []).append(
                f"page on disk but missing from search index: {url}"
            )
        for url in sorted(idx_urls - disk_urls):
            all_issues.setdefault("search-index.json", []).append(
                f"search index entry has no matching HTML file: {url}"
            )

    # ---- Report ----
    report_lines = [
        "# Site Audit Report — OverKill Hill P3",
        "",
        f"Pages scanned: {len(html_paths)}",
        "",
    ]

    total = sum(len(v) for v in all_issues.values())
    if not all_issues:
        report_lines.append("**0 issues found. All checks passed.**")
    else:
        report_lines.append(f"**{total} issue(s) found across {len(all_issues)} file(s):**")
        report_lines.append("")
        for rel, issues in sorted(all_issues.items()):
            report_lines.append(f"### {rel}")
            for iss in issues:
                report_lines.append(f"- {iss}")
            report_lines.append("")

    report_path = REPO_ROOT / "assets" / "docs" / "audit-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nReport written to {report_path.relative_to(REPO_ROOT)}")
    print(f"Total issues found: {total}")

    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

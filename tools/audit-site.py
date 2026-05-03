#!/usr/bin/env python3
"""
audit-site.py — static-site auditor for askjamie.bot.

Walks every .html file in the repo (excluding .local/, attached_assets/,
node_modules/, .cache/, .git/, .vscode/) and produces a Markdown report.

Per-page checks actually emitted as issues:
  * <title> length (<=70) and presence
  * <meta name="description"> length (<=165) and presence
  * exactly one <h1>
  * canonical link presence
  * required Open Graph fields: og:title, og:description, og:image, og:url
  * <html lang="..."> presence
  * every <img> has alt, width, and height attributes
  * external target="_blank" links carry rel="noopener noreferrer"
  * known placeholder strings (ASK-JAMIE-GPT-ID-HERE, the old SearchAction
    target ?s={search_term_string}, generic YOUR-...)
  * theme-color resolves to the AskJamie brand teal (#2c5e6f)

Cross-file reconciliation (best-effort; failures are reported as issues
rather than crashing the run):
  * sitemap.xml entries vs HTML files on disk
  * search-index.json entries vs HTML files on disk

Usage:
    python3 tools/audit-site.py
    python3 tools/audit-site.py --report tools/audit-report.md
    python3 tools/audit-site.py --quiet
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Tuple
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".local", "attached_assets", "node_modules", ".cache", ".git", ".vscode",
                "templates"}
EXCLUDE_FROM_SITEMAP = {"404.html", "under-construction.html"}

# Title / description recommended length budgets
TITLE_MAX = 70
DESC_MAX = 165

# Brand-correct theme color
EXPECTED_THEME_COLOR = "#2c5e6f"
EXPECTED_BG_COLOR = "#f5efe1"


def iter_html_files() -> List[Path]:
    out: List[Path] = []
    for p in ROOT.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


class PageParser(HTMLParser):
    """Lightweight extractor for the bits we need to audit."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.h1_count = 0
        self._in_h1 = False
        self.metas: Dict[str, str] = {}
        self.canonical = ""
        self.images: List[Dict[str, str]] = []
        self.external_links: List[Dict[str, str]] = []
        self.placeholder_hits: List[str] = []
        self.has_jsonld_website = False
        self.has_jsonld_breadcrumb = False
        self.has_jsonld_article = False
        self._jsonld_collect = False
        self._jsonld_buf: List[str] = []

    def handle_starttag(self, tag: str, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
            self._in_h1 = True
        elif tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key:
                self.metas[key.lower()] = a.get("content", "") or ""
        elif tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical = a.get("href", "") or ""
        elif tag == "img":
            self.images.append(
                {
                    "src": a.get("src", ""),
                    "alt": a.get("alt"),
                    "width": a.get("width"),
                    "height": a.get("height"),
                    "loading": a.get("loading"),
                }
            )
        elif tag == "a":
            href = a.get("href", "") or ""
            if a.get("target") == "_blank" and href.startswith(("http://", "https://")):
                rel = (a.get("rel") or "").lower()
                self.external_links.append({"href": href, "rel": rel})
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._jsonld_collect = True
            self._jsonld_buf = []

    def handle_endtag(self, tag: str):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "script" and self._jsonld_collect:
            self._jsonld_collect = False
            blob = "".join(self._jsonld_buf).strip()
            if '"WebSite"' in blob:
                self.has_jsonld_website = True
            if '"BreadcrumbList"' in blob:
                self.has_jsonld_breadcrumb = True
            if '"Article"' in blob or '"NewsArticle"' in blob:
                self.has_jsonld_article = True

    def handle_data(self, data: str):
        if self._in_title:
            self.title += data
        if self._jsonld_collect:
            self._jsonld_buf.append(data)


PLACEHOLDER_PATTERNS = [
    ("ASK-JAMIE-GPT-ID-HERE", "Placeholder GPT URL"),
    ("?s={search_term_string}", "Old SearchAction target"),
    ("YOUR-", "Generic placeholder"),
]
BARE_NOOPENER = re.compile(r'\brel="noopener"(?!\s*noreferrer)')


def audit_page(path: Path) -> List[str]:
    rel = path.relative_to(ROOT).as_posix()
    src = path.read_text(encoding="utf-8", errors="replace")
    issues: List[str] = []

    # placeholder text scan (raw)
    for needle, label in PLACEHOLDER_PATTERNS:
        if needle in src:
            issues.append(f"{label}: `{needle}` present")
    if BARE_NOOPENER.search(src):
        issues.append('Bare rel="noopener" without noreferrer present')

    # quick theme-color check
    m = re.search(r'<meta\s+name="theme-color"\s+content="([^"]+)"', src)
    if m and m.group(1).lower() != EXPECTED_THEME_COLOR:
        issues.append(
            f'theme-color is `{m.group(1)}`, expected `{EXPECTED_THEME_COLOR}` (brand teal)'
        )

    # parse for structural checks
    p = PageParser()
    try:
        p.feed(src)
    except Exception as exc:  # pragma: no cover
        issues.append(f"HTML parser raised: {exc!r}")
        return issues

    title = p.title.strip()
    if not title:
        issues.append("Missing <title>")
    elif len(title) > TITLE_MAX:
        issues.append(f"Title is {len(title)} chars (>{TITLE_MAX})")

    desc = p.metas.get("description", "").strip()
    if not desc:
        issues.append("Missing meta description")
    elif len(desc) > DESC_MAX:
        issues.append(f"Description is {len(desc)} chars (>{DESC_MAX})")

    if "html lang=" not in src and "<html lang=" not in src:
        issues.append("Missing lang attribute on <html>")

    if p.h1_count == 0:
        issues.append("No <h1> found")
    elif p.h1_count > 1:
        issues.append(f"{p.h1_count} <h1> elements (should be 1)")

    if not p.canonical:
        issues.append("Missing canonical link")

    for required in ("og:title", "og:description", "og:image", "og:url"):
        if required not in p.metas:
            issues.append(f"Missing {required}")

    # image hygiene
    for img in p.images:
        src_attr = img["src"] or "(no src)"
        if img["alt"] is None:
            issues.append(f"Image missing alt: {src_attr}")
        if img["width"] is None or img["height"] is None:
            issues.append(f"Image missing width/height: {src_attr}")

    # external link hygiene (we already raw-checked, but report each link missing noreferrer)
    for link in p.external_links:
        rel_attr = link["rel"]
        if "noreferrer" not in rel_attr or "noopener" not in rel_attr:
            issues.append(
                f'External target=_blank link lacks noopener+noreferrer: {link["href"]}'
            )

    return issues


def parse_sitemap() -> Tuple[List[str], List[str]]:
    """Return (urls, errors). Never raises."""
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return [], ["sitemap.xml is missing"]
    try:
        tree = ET.parse(sitemap)
    except ET.ParseError as exc:
        return [], [f"sitemap.xml is unparseable: {exc}"]
    locs = [
        (loc.text or "").strip()
        for loc in tree.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    ]
    return [u for u in locs if u], []


def url_to_relpath(url: str) -> str:
    """Map https://askjamie.bot/foo/ -> foo/index.html (or foo.html)."""
    path = url.replace("https://askjamie.bot", "").lstrip("/")
    if path == "":
        return "index.html"
    if path.endswith(".html"):
        return path
    if path.endswith("/"):
        return path + "index.html"
    return path + "/index.html"


def reconcile_sitemap(html_files: List[Path]) -> Tuple[List[str], List[str], List[str]]:
    """Return (in_sitemap_not_on_disk, on_disk_not_in_sitemap, errors)."""
    rels_on_disk = {p.relative_to(ROOT).as_posix() for p in html_files}
    rels_on_disk -= EXCLUDE_FROM_SITEMAP
    sitemap_urls, errors = parse_sitemap()
    if errors:
        return [], [], errors
    rels_in_sitemap = {url_to_relpath(u) for u in sitemap_urls}
    in_sitemap_missing_disk = sorted(rels_in_sitemap - rels_on_disk)
    on_disk_missing_sitemap = sorted(rels_on_disk - rels_in_sitemap)
    return in_sitemap_missing_disk, on_disk_missing_sitemap, []


def reconcile_search_index(html_files: List[Path]) -> List[str]:
    idx = ROOT / "assets/data/search-index.json"
    if not idx.exists():
        return ["search-index.json missing"]
    try:
        data = json.loads(idx.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"search-index.json is unreadable: {exc}"]
    try:
        pages = data.get("pages", data) if isinstance(data, dict) else data
        if not isinstance(pages, list):
            return [f"search-index.json has unexpected shape: {type(pages).__name__}"]
        indexed_urls = {item.get("url", "") for item in pages if isinstance(item, dict)}
        indexed_rels = {
            url_to_relpath(u) if u.startswith("http") else u.lstrip("/")
            for u in indexed_urls
            if u
        }
        indexed_rels = {
            r if r.endswith(".html") else r.rstrip("/") + "/index.html"
            for r in indexed_rels
        }
        indexed_rels = {r.lstrip("/") or "index.html" for r in indexed_rels}
        rels_on_disk = {p.relative_to(ROOT).as_posix() for p in html_files}
        rels_on_disk -= EXCLUDE_FROM_SITEMAP
        missing = sorted(rels_on_disk - indexed_rels)
        return [f"Page on disk not in search index: {p}" for p in missing]
    except Exception as exc:  # pragma: no cover — defensive
        return [f"search-index reconciliation crashed: {exc!r}"]


def render_report(per_page: Dict[str, List[str]],
                  sitemap_missing_disk: List[str],
                  disk_missing_sitemap: List[str],
                  search_issues: List[str]) -> str:
    total_issues = sum(len(v) for v in per_page.values()) + \
                   len(sitemap_missing_disk) + len(disk_missing_sitemap) + len(search_issues)
    lines = [
        "# AskJamie.bot — Automated Site Audit",
        "",
        f"**Pages scanned:** {len(per_page)}  ",
        f"**Total issues:** {total_issues}",
        "",
        "## Sitemap reconciliation",
        "",
    ]
    if not sitemap_missing_disk and not disk_missing_sitemap:
        lines.append("- OK — sitemap and on-disk pages are in sync.")
    if sitemap_missing_disk:
        lines.append("- **Sitemap entries with no file on disk:**")
        for x in sitemap_missing_disk:
            lines.append(f"  - `{x}`")
    if disk_missing_sitemap:
        lines.append("- **Pages on disk not listed in sitemap.xml:**")
        for x in disk_missing_sitemap:
            lines.append(f"  - `{x}`")
    lines += ["", "## Search-index reconciliation", ""]
    if not search_issues:
        lines.append("- OK — every public page is covered by the search index.")
    else:
        for x in search_issues:
            lines.append(f"- {x}")
    lines += ["", "## Per-page issues", ""]
    for page, issues in sorted(per_page.items()):
        if not issues:
            continue
        lines.append(f"### `{page}`")
        for issue in issues:
            lines.append(f"- {issue}")
        lines.append("")
    if all(not v for v in per_page.values()):
        lines.append("_No per-page issues found._")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="tools/audit-report.md",
                        help="Path to write the Markdown report.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress per-page console output.")
    args = parser.parse_args()

    html_files = iter_html_files()
    per_page: Dict[str, List[str]] = {}
    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        per_page[rel] = audit_page(path)
        if not args.quiet:
            count = len(per_page[rel])
            flag = "OK " if count == 0 else f"{count:>3}"
            print(f"  [{flag}] {rel}")

    sitemap_missing_disk, disk_missing_sitemap, sitemap_errors = reconcile_sitemap(html_files)
    search_issues = reconcile_search_index(html_files)
    if sitemap_errors:
        # Surface sitemap parse errors as issues against sitemap.xml itself.
        per_page["sitemap.xml"] = per_page.get("sitemap.xml", []) + sitemap_errors

    report = render_report(per_page, sitemap_missing_disk, disk_missing_sitemap, search_issues)
    out = ROOT / args.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"\nReport written to {out.relative_to(ROOT)}")

    total = sum(len(v) for v in per_page.values()) + len(sitemap_missing_disk) + \
            len(disk_missing_sitemap) + len(search_issues)
    print(f"Total issues found: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Build the static search index for overkillhill.com.

STAGED COPY -- ready to drop into the OKHP3/OverKill-Hill repo.

Per-site constants that were changed from the AskJamie original:
  - SITE_URL               changed to https://overkillhill.com
  - strip_brand_suffix()   suffixes changed to OKH brand name variants
  - derive_section()       section_map updated to OKH top-level URL segments

VERIFY before first run:
  1. Confirm SITE_URL matches the deployed domain exactly.
  2. Open a few OKH page <title> tags and check what brand suffix they use
     (e.g. " -- OverKill Hill P3(tm)" or " | OverKill Hill P3"). Update
     strip_brand_suffix() to match exactly.
  3. Confirm the section_map covers all top-level directories in the OKH repo.
     Add or rename entries as needed.
  4. Run:  python3 scripts/build-search-index.py
     Verify: Pages indexed > 0, file size > 0 KB.
  5. Run:  python3 scripts/audit-site.py --quiet
     Target: 0 issues (search-index reconciliation gate).

All other logic (TextExtractor parser, STRIP_TAGS, STRIP_CLASSES_CONTAINS,
VOID_TAGS, MAX_BODY cap, output format) is site-agnostic and was copied verbatim.

Source: AskJamie scripts/build-search-index.py (2026-05-27)
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# PER-SITE CONSTANTS  <-- edit these when copying to a new sister site
# ---------------------------------------------------------------------------

SITE_URL  = "https://overkillhill.com"
INDEX_OUT = os.path.join(REPO_ROOT, "assets", "data", "search-index.json")

# ---------------------------------------------------------------------------
# SITE-AGNOSTIC CONSTANTS (copy verbatim across all sister sites)
# ---------------------------------------------------------------------------

EXCLUDE_DIRS = {".git", ".local", "attached_assets", "tools", "node_modules",
                "templates"}
EXCLUDE_FILES = {"404.html", "under-construction.html"}

STRIP_TAGS = {"script", "style", "nav", "header", "footer", "noscript", "svg"}
# Do NOT add layout-decorator classes here -- they wrap actual page content
# and stripping them produces empty body excerpts.
STRIP_CLASSES_CONTAINS = {"site-header", "site-footer", "primary-nav", "skip-link",
                          "construction-overlay"}

# HTML5 void elements never receive a handle_endtag from html.parser.
# Do not push them onto the tag stack or subsequent </a> etc. will pop
# the wrong entry and leave a strip-zone permanently unclosed.
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


class TextExtractor(HTMLParser):
    """Collects visible text + structural data from an HTML document."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title       = ""
        self.description = ""
        self.canonical   = ""
        self.h1          = ""
        self.headings    = []   # h2/h3 strings
        self.body_chunks = []

        self._capture_title    = False
        self._stack            = []   # tag stack
        self._skip_depth       = 0    # >0 means inside a strip-zone
        self._cur_heading_buf  = None
        self._cur_heading_tag  = None

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)

        if tag == "title":
            self._capture_title = True
            return

        if tag == "meta":
            name = (attrs_d.get("name") or "").lower()
            if name == "description":
                self.description = (attrs_d.get("content") or "").strip()
            return

        if tag == "link":
            if (attrs_d.get("rel") or "").lower() == "canonical":
                self.canonical = (attrs_d.get("href") or "").strip()
            return

        # Skip-zone detection
        cls = attrs_d.get("class", "")
        if tag in STRIP_TAGS or any(s in cls for s in STRIP_CLASSES_CONTAINS):
            self._skip_depth += 1
            self._stack.append((tag, True))
            return

        # Void elements never close -- do not push onto the stack.
        if tag in VOID_TAGS:
            return

        self._stack.append((tag, False))

        # Heading collection (only outside strip zones)
        if self._skip_depth == 0:
            if tag == "h1" and not self.h1:
                self._cur_heading_buf = []
                self._cur_heading_tag = "h1"
            elif tag in ("h2", "h3"):
                self._cur_heading_buf = []
                self._cur_heading_tag = tag

    def handle_endtag(self, tag):
        if tag == "title":
            self._capture_title = False
            return

        # Pop the nearest matching stack entry (and everything above it
        # for unclosed tags that never received their own end tag).
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                removed = self._stack[i:]
                del self._stack[i:]
                for _, was_skip in removed:
                    if was_skip:
                        self._skip_depth = max(0, self._skip_depth - 1)
                break

        # Finalize a heading
        if self._cur_heading_tag == tag and self._cur_heading_buf is not None:
            text = " ".join("".join(self._cur_heading_buf).split()).strip()
            if text:
                if tag == "h1":
                    self.h1 = text
                else:
                    self.headings.append(text)
                self.body_chunks.append(text)
            self._cur_heading_buf = None
            self._cur_heading_tag = None

    def handle_data(self, data):
        if self._capture_title:
            self.title += data
            return
        if self._skip_depth > 0:
            return
        if self._cur_heading_buf is not None:
            self._cur_heading_buf.append(data)
        self.body_chunks.append(data)


def normalize_text(s: str) -> str:
    """Collapse whitespace and strip stray junk."""
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def derive_url_from_path(rel_path: str) -> str:
    """Convert a repo-relative .html path into the public URL path."""
    p = rel_path.replace(os.sep, "/")
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    elif p == "index.html":
        p = ""
    return "/" + p if p and not p.startswith("/") else (p or "/")


# ---------------------------------------------------------------------------
# PER-SITE FUNCTIONS  <-- review and update when copying to a new sister site
# ---------------------------------------------------------------------------

def derive_section(url_path: str) -> str:
    """Friendly section label for grouping search results.

    VERIFY: check the OKH repo's top-level directories and update this map
    to reflect the actual site structure. Add any missing sections and remove
    any that do not exist on the OKH site.
    """
    if url_path == "/":
        return "Home"
    parts = [p for p in url_path.split("/") if p]
    if not parts:
        return "Home"

    section_map = {
        "about":      "About",
        "contact":    "Contact",
        "legal":      "Legal",
        "writings":   "Writings",
        "lens-system": "Lens System",
        "universe":   "Universe",
        "tools":      "Tools",
    }

    if parts[0] in section_map:
        if len(parts) == 1:
            return section_map[parts[0]]
        # Lens System sub-sections
        if parts[0] == "lens-system":
            if parts[1] == "okhp3-brandguard":
                return "Lens System - BrandGuard"
            return "Lens System"
        return section_map[parts[0]]

    return "General"


def strip_brand_suffix(title: str) -> str:
    """Drop the trailing site brand from the page title for cleaner display.

    VERIFY: open several OKH page <title> tags and confirm the exact suffix
    strings used. Common patterns:
      " -- OverKill Hill P3(tm)"  (en-dash variant)
      " | OverKill Hill P3"
    Update this list to match exactly what the OKH pages produce.
    """
    title = normalize_text(title)
    for suffix in (
        " -- OverKill Hill P3(tm)",
        " | OverKill Hill P3(tm)",
        " -- OverKill Hill P3",
        " | OverKill Hill P3",
        " -- OverKill Hill",
        " | OverKill Hill",
    ):
        if title.endswith(suffix):
            return title[: -len(suffix)].strip()
    return title


# ---------------------------------------------------------------------------
# SITE-AGNOSTIC PROCESSING (copy verbatim across all sister sites)
# ---------------------------------------------------------------------------

def process_file(rel_path: str) -> dict | None:
    full = os.path.join(REPO_ROOT, rel_path)
    try:
        with open(full, encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"  ! failed to read {rel_path}: {e}", file=sys.stderr)
        return None

    parser = TextExtractor()
    try:
        parser.feed(html)
    except Exception as e:
        print(f"  ! parse error in {rel_path}: {e}", file=sys.stderr)

    title_clean = strip_brand_suffix(parser.title)
    body = normalize_text(" ".join(parser.body_chunks))

    # Trim body to a reasonable size (the index is downloaded by every visitor).
    MAX_BODY = 4000
    if len(body) > MAX_BODY:
        body = body[:MAX_BODY]

    url_path = derive_url_from_path(rel_path)

    return {
        "url":         url_path,
        "title":       title_clean or rel_path,
        "description": parser.description,
        "section":     derive_section(url_path),
        "h1":          parser.h1,
        "headings":    parser.headings[:20],
        "body":        body,
    }


def main():
    pages = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            if fn in EXCLUDE_FILES:
                continue
            full = os.path.join(dirpath, fn)
            rel  = os.path.relpath(full, REPO_ROOT)
            page = process_file(rel)
            if page:
                pages.append(page)

    pages.sort(key=lambda p: p["url"])

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "site":      SITE_URL,
        "count":     len(pages),
        "pages":     pages,
    }

    os.makedirs(os.path.dirname(INDEX_OUT), exist_ok=True)
    with open(INDEX_OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(INDEX_OUT) / 1024
    print(f"Wrote {INDEX_OUT}")
    print(f"  Pages indexed: {len(pages)}")
    print(f"  File size:     {size_kb:.1f} KB")


if __name__ == "__main__":
    main()

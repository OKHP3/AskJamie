#!/usr/bin/env python3
"""
Build the static search index for AskJamie.bot.

Walks every .html file in the repo (excluding 404, under-construction, and the
attached_assets / .git / .local trees), extracts:
    - canonical URL (from <link rel="canonical"> if present, else derived from path)
    - title (from <title>, with brand suffix stripped)
    - meta description
    - section label (Home / Lens System / BrandGuard / About / etc.)
    - H1
    - All H2 and H3 headings
    - Body text (visible content only - nav/header/footer/scripts/styles stripped)

Writes assets/data/search-index.json - a compact array of page records.

Run from repo root:  python3 scripts/build-search-index.py
"""

import json
import os
import re
import sys
import argparse
import subprocess
from datetime import datetime, timezone
from html.parser import HTMLParser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://askjamie.bot"
INDEX_OUT = os.path.join(REPO_ROOT, "assets", "data", "search-index.json")

EXCLUDE_DIRS = {".git", ".local", "attached_assets", "tools", "node_modules",
                "templates", "dist-pages"}  # assets/templates/ = developer scaffolding, never public pages
EXCLUDE_FILES = {"404.html", "under-construction.html"}

STRIP_TAGS = {"script", "style", "nav", "header", "footer", "noscript", "svg"}
# NOTE: do NOT add layout-decorator classes here (e.g. `askjamie-paper`,
# `brand-stripes`, `site-specials`) — those classes wrap the actual page
# content on AskJamie pages; stripping them produces empty body excerpts.
STRIP_CLASSES_CONTAINS = {"site-header", "site-footer", "primary-nav", "skip-link",
                          "construction-overlay"}

# HTML5 void elements never receive a `handle_endtag` from html.parser, so we
# must NOT push them onto the tag stack — otherwise a later `</a>` etc. will
# pop the wrong entry and leave a strip-zone permanently unclosed.
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


class TextExtractor(HTMLParser):
    """Collects visible text + structural data from an HTML document."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.h1 = ""
        self.headings = []  # h2/h3 strings
        self.body_chunks = []

        self._capture_title = False
        self._stack = []  # tag stack
        self._skip_depth = 0  # >0 means we're inside a strip-zone
        self._cur_heading_buf = None  # if collecting heading text
        self._cur_heading_tag = None

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

        # Void elements never close — don't push them onto the stack or
        # subsequent `handle_endtag` calls will pop the wrong entry.
        if tag in VOID_TAGS:
            return

        self._stack.append((tag, False))

        # Heading collection (only if we're not inside a strip zone)
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

        # Pop the nearest matching stack entry — and pop everything above it
        # too (those are unclosed tags that never received their own end tag,
        # such as paragraphs in HTML5 where `</p>` is optional).
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
                # Headings also count as body content for matching
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
        # Always add to body too (so headings are searchable from the body field)
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


def derive_section(url_path: str) -> str:
    """Friendly section label for grouping results."""
    if url_path == "/":
        return "Home"
    parts = [p for p in url_path.split("/") if p]
    if not parts:
        return "Home"

    section_map = {
        "about": "About",
        "contact": "Contact",
        "legal": "Legal",
        "universe": "Universe",
        "lens-system": "Lens System",
    }

    if parts[0] in section_map:
        if len(parts) == 1:
            return section_map[parts[0]]
        # Lens System sub-sections
        if parts[0] == "lens-system":
            if parts[1] == "okhp3-brandguard":
                return "Lens System · BrandGuard"
            return "Lens System"
    return "Lens System"


def strip_brand_suffix(title: str) -> str:
    """Drop the trailing site brand from the page title for cleaner display."""
    title = normalize_text(title)
    for suffix in (
        " — AskJamie™",
        " | AskJamie™",
        " — AskJamie",
        " | AskJamie",
    ):
        if title.endswith(suffix):
            return title[: -len(suffix)].strip()
    return title


def process_file(rel_path: str) -> dict | None:
    full = os.path.join(REPO_ROOT, rel_path)
    try:
        with open(full, encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"  ! failed to read {rel_path}: {e}", file=sys.stderr)
        return None

    # Generated navigation must never feed its own index.
    html = re.sub(r"<!-- AUTOGEN:UNIVERSE-MAP -->.*?<!-- /AUTOGEN:UNIVERSE-MAP -->", "", html, flags=re.S)
    parser = TextExtractor()
    try:
        parser.feed(html)
    except Exception as e:
        print(f"  ! parse error in {rel_path}: {e}", file=sys.stderr)

    title_clean = strip_brand_suffix(parser.title)
    body = normalize_text(" ".join(parser.body_chunks))

    # Trim body to a reasonable size (the index is downloaded by every visitor).
    # 4000 chars per page × 23 pages ≈ 92 KB pre-gzip, ~25 KB gzipped. Acceptable.
    MAX_BODY = 4000
    if len(body) > MAX_BODY:
        body = body[:MAX_BODY]

    url_path = derive_url_from_path(rel_path)

    return {
        "url": url_path,
        "title": title_clean or rel_path,
        "description": parser.description,
        "category": derive_section(url_path),
        "h1": parser.h1,
        "headings": parser.headings[:20],  # cap
        "body": body,
    }


def collect_pages():
    pages = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        # Prune excluded dirs in-place
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            if fn in EXCLUDE_FILES:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, REPO_ROOT)
            page = process_file(rel)
            if page:
                pages.append(page)

    pages.sort(key=lambda p: p["url"])
    return pages


def build_index_document():
    pages = collect_pages()

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "site": SITE_URL,
        "count": len(pages),
        "entries": pages,
    }
    return out


def canonical_for_check(document):
    """Remove the intentionally volatile timestamp before comparing output."""
    return {key: value for key, value in document.items() if key != "generated"}


def preserve_timestamp_when_unchanged(document):
    """Avoid dirtying the worktree when rebuilding unchanged content."""
    if not os.path.exists(INDEX_OUT):
        return document
    try:
        with open(INDEX_OUT, encoding="utf-8") as f:
            previous = json.load(f)
    except (OSError, json.JSONDecodeError):
        return document
    if canonical_for_check(previous) == canonical_for_check(document):
        document["generated"] = previous.get("generated", document["generated"])
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the committed index matches current HTML without rewriting it.",
    )
    args = parser.parse_args()

    out = preserve_timestamp_when_unchanged(build_index_document())
    if args.check:
        if not os.path.exists(INDEX_OUT):
            print(f"ERROR: missing generated index: {INDEX_OUT}", file=sys.stderr)
            return 1
        try:
            with open(INDEX_OUT, encoding="utf-8") as f:
                committed = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read generated index: {exc}", file=sys.stderr)
            return 1
        if canonical_for_check(committed) != canonical_for_check(out):
            print(
                "ERROR: search-index.json is out of date. "
                "Run `python3 scripts/build-search-index.py` and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"✓ Search index is current ({len(out['entries'])} pages).")
        return 0

    os.makedirs(os.path.dirname(INDEX_OUT), exist_ok=True)
    with open(INDEX_OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(INDEX_OUT) / 1024
    print(f"✓ Wrote {INDEX_OUT}")
    print(f"  Pages indexed: {len(out['entries'])}")
    print(f"  File size:     {size_kb:.1f} KB")
    return subprocess.call([sys.executable, os.path.join(REPO_ROOT, "scripts", "sync-universe-map.py")])


if __name__ == "__main__":
    sys.exit(main())

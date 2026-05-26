#!/usr/bin/env python3
"""Task #1 bulk edits:
  1. Remove construction-overlay blocks from 6 pages
  2. Add /search/ link to footer Navigation on all 26 pages
  3. Add static 2026 fallback to copyright year span
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent.parent
EXCLUDE = {".local", "attached_assets", ".cache", "node_modules", ".git", "scripts"}

def all_html():
    for p in sorted(ROOT.rglob("*.html")):
        if any(part in EXCLUDE for part in p.parts):
            continue
        if p.name in ("404.html", "under-construction.html"):
            continue
        yield p

# ── 1. Remove construction-overlay blocks ──────────────────────────────────
# Match from the HTML comment before the div through the closing comment.
OVERLAY_PATTERNS = [
    # full block with surrounding comments
    re.compile(
        r'\n?[ \t]*<!-- 🔧 AskJamie "under construction" gate -->.*?<!-- 🔧 end under.construction gate -->\n?',
        re.DOTALL
    ),
    # fallback: just the div block without comments
    re.compile(
        r'\n?[ \t]*<div class="construction-overlay"[^>]*>.*?</div>\s*</div>\s*<!-- 🔧 end',
        re.DOTALL
    ),
]

OVERLAY_FILES = [
    ROOT / "lens-system/index.html",
    ROOT / "lens-system/enterprise-sleuth/index.html",
    ROOT / "lens-system/okhp3-brandguard/index.html",
    ROOT / "lens-system/okhp3-brandguard/lego/index.html",
    ROOT / "lens-system/professional-portfolio/index.html",
    ROOT / "lens-system/resume-representative/index.html",
]

removed_overlays = []
for path in OVERLAY_FILES:
    if not path.exists():
        print(f"  SKIP (not found): {path}")
        continue
    text = path.read_text(encoding="utf-8")
    original = text
    for pat in OVERLAY_PATTERNS:
        text = pat.sub("", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        removed_overlays.append(path.name)
        print(f"  OVERLAY REMOVED: {path.relative_to(ROOT)}")
    else:
        print(f"  OVERLAY NOT FOUND (check manually): {path.relative_to(ROOT)}")

# ── 2. Add /search/ link to footer Navigation column ──────────────────────
# The target block looks like:
#   <li><a href="/legal/">Legal</a></li>
#          </ul>
#        </div>
# We insert a Search link after Legal.

SEARCH_LINK = '            <li><a href="/search/">Search</a></li>'

# Pattern: match the </ul> that closes the Navigation list (the one right
# after Legal), but only if Search isn't already there.
NAV_CLOSE_PAT = re.compile(
    r'(<li><a href="/legal/">Legal</a></li>)\s*(\s*</ul>)',
    re.DOTALL
)

added_search = []
skipped_search = []
for path in all_html():
    text = path.read_text(encoding="utf-8")
    if 'href="/search/"' in text:
        skipped_search.append(path.name)
        continue
    # Find the footer navigation list Legal link and inject Search after it
    if '<a href="/legal/">Legal</a>' not in text:
        print(f"  SEARCH SKIP (no legal link): {path.relative_to(ROOT)}")
        continue
    new_text = NAV_CLOSE_PAT.sub(
        r'\1\n' + SEARCH_LINK + r'\2',
        text,
        count=1
    )
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        added_search.append(str(path.relative_to(ROOT)))
        print(f"  SEARCH LINK ADDED: {path.relative_to(ROOT)}")
    else:
        print(f"  SEARCH LINK NOT MATCHED: {path.relative_to(ROOT)}")

# ── 3. Add static 2026 fallback to copyright year span ────────────────────
YEAR_PAT = re.compile(r'<span id="current-year-askjamie"></span>')
YEAR_REPLACEMENT = '<span id="current-year-askjamie">2026</span>'

updated_year = []
for path in all_html():
    text = path.read_text(encoding="utf-8")
    if YEAR_PAT.search(text):
        new_text = YEAR_PAT.sub(YEAR_REPLACEMENT, text)
        path.write_text(new_text, encoding="utf-8")
        updated_year.append(str(path.relative_to(ROOT)))
        print(f"  YEAR UPDATED: {path.relative_to(ROOT)}")

# Also fix 404.html and under-construction.html
for name in ("404.html", "under-construction.html"):
    path = ROOT / name
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if YEAR_PAT.search(text):
            path.write_text(YEAR_PAT.sub(YEAR_REPLACEMENT, text), encoding="utf-8")
            print(f"  YEAR UPDATED: {name}")

print()
print(f"Summary:")
print(f"  Overlays removed from {len(removed_overlays)} files: {removed_overlays}")
print(f"  Search link added to {len(added_search)} files")
print(f"  Year fallback added to {len(updated_year)} files")

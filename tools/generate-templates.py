#!/usr/bin/env python3
"""
generate-templates.py — Phase 13 template-library generator.

Reads representative production pages and writes one stripped template
per Page Type into /assets/templates/, following the rules in the
Phase 13 brief:

  * keep all CSS class names, IDs, structural HTML, nav, footer, scripts
  * strip page-specific copy and replace it with [[DOUBLE-BRACKET]] tokens
  * keep <head> metadata structure but tokenise the values
  * preserve nav logo and footer logo image paths (shared infrastructure);
    tokenise every other img src/alt
  * clear JSON-LD body to a single placeholder block; keep the wrapper
  * inject a TEMPLATE SECTION comment above every <section> inside <main>,
    auto-named from the section's first h1/h2 or aria-label
  * prepend a template-header comment block at the top of the file

Usage:
    python3 tools/generate-templates.py
"""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "assets" / "templates"

# (page_type_label, source_relpath, source_page_label_for_header)
SOURCES: List[Tuple[str, str, str]] = [
    ("homepage",         "index.html",                                                        "Homepage (root index)"),
    ("interior-single",  "about/index.html",                                                  "About page (interior, no form)"),
    ("interior-form",    "contact/index.html",                                                "Contact page (form-anchored)"),
    ("hub",              "lens-system/okhp3-brandguard/index.html",                           "BrandGuard hub (children grid)"),
    ("lens-detail",      "lens-system/resume-representative/index.html",                      "Lens-detail page (Résumé Representative)"),
    ("case-study",       "lens-system/okhp3-brandguard/lego/index.html",                      "BrandGuard case study (LEGO)"),
    ("error",            "404.html",                                                          "404 error page"),
    ("holding",          "under-construction.html",                                           "Under-construction holding page"),
    ("utility",          "search/index.html",                                                 "Search page (utility)"),
]

# Image src substrings that identify nav-logo / footer-logo / shared infra
# images. These are NOT tokenised — they remain real paths per Rule 5 exception.
SHARED_IMAGE_NEEDLES = [
    "AskJamie%20AvatarTallLeft%20Square%201024.png",   # 40x40 nav logo
    "AskJamie%20TitleCreamBlueBackdropBlueGrayLeft",   # crumb logo
]


# --------------------------------------------------------------------------
# meta-value tokenisation: preserve attribute structure, swap value
# --------------------------------------------------------------------------
META_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r'(<meta\s+name="description"\s+content=")[^"]*(")'),       r'\1[[PAGE-DESCRIPTION]]\2'),
    (re.compile(r'(<meta\s+name="keywords"\s+content=")[^"]*(")'),          r'\1[[PAGE-KEYWORDS]]\2'),
    (re.compile(r'(<meta\s+property="og:title"\s+content=")[^"]*(")'),      r'\1[[OG-TITLE]]\2'),
    (re.compile(r'(<meta\s+property="og:description"\s+content=")[^"]*(")'),r'\1[[OG-DESCRIPTION]]\2'),
    (re.compile(r'(<meta\s+property="og:url"\s+content=")[^"]*(")'),        r'\1[[OG-URL]]\2'),
    (re.compile(r'(<meta\s+property="og:image"\s+content=")[^"]*(")'),      r'\1[[OG-IMAGE-URL]]\2'),
    (re.compile(r'(<meta\s+property="og:image:alt"\s+content=")[^"]*(")'),  r'\1[[OG-IMAGE-ALT]]\2'),
    (re.compile(r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")'),     r'\1[[TWITTER-TITLE]]\2'),
    (re.compile(r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")'), r'\1[[TWITTER-DESCRIPTION]]\2'),
    (re.compile(r'(<meta\s+name="twitter:image"\s+content=")[^"]*(")'),     r'\1[[TWITTER-IMAGE-URL]]\2'),
    (re.compile(r'(<meta\s+name="twitter:image:alt"\s+content=")[^"]*(")'), r'\1[[TWITTER-IMAGE-ALT]]\2'),
    (re.compile(r'(<meta\s+name="twitter:url"\s+content=")[^"]*(")'),       r'\1[[TWITTER-URL]]\2'),
    (re.compile(r'(<meta\s+name="twitter:card"\s+content=")[^"]*(")'),      r'\1[[TWITTER-CARD]]\2'),
    (re.compile(r'(<meta\s+name="twitter:site"\s+content=")[^"]*(")'),      r'\1[[TWITTER-SITE]]\2'),
    (re.compile(r'(<meta\s+name="twitter:creator"\s+content=")[^"]*(")'),   r'\1[[TWITTER-CREATOR]]\2'),
    (re.compile(r'(<meta\s+property="og:type"\s+content=")[^"]*(")'),       r'\1[[OG-TYPE]]\2'),
    (re.compile(r'(<meta\s+property="og:site_name"\s+content=")[^"]*(")'),  r'\1[[OG-SITE-NAME]]\2'),
    (re.compile(r'(<link\s+rel="canonical"\s+href=")[^"]*(")'),             r'\1[[CANONICAL-URL]]\2'),
    (re.compile(r'<title>[^<]*</title>', re.IGNORECASE),                    '<title>[[PAGE-TITLE]]</title>'),
]


def tokenise_meta(src: str) -> str:
    out = src
    for pat, rep in META_PATTERNS:
        out = pat.sub(rep, out)
    return out


# --------------------------------------------------------------------------
# JSON-LD: clear body, keep wrapper
# --------------------------------------------------------------------------
JSONLD_BLOCK = re.compile(
    r'(<script\s+type="application/ld\+json"[^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE,
)
JSONLD_TYPE = re.compile(r'"@type"\s*:\s*"([^"]+)"')


def clear_jsonld(src: str) -> str:
    """Replace each JSON-LD body with a placeholder that preserves the
    original @type stub. If the original block had no @type (rare), use
    a token instead."""
    def replace(m: re.Match) -> str:
        body = m.group(2)
        type_match = JSONLD_TYPE.search(body)
        type_value = type_match.group(1) if type_match else "[[SCHEMA-TYPE]]"
        placeholder = (
            "\n"
            "  {\n"
            '    "@context": "https://schema.org",\n'
            f'    "@type": "{type_value}",\n'
            '    "_comment": "Replace this object with the page-specific structured data. The @type stub is preserved from the source page."\n'
            "  }\n"
        )
        return m.group(1) + placeholder + m.group(3)
    return JSONLD_BLOCK.sub(replace, src)


# --------------------------------------------------------------------------
# headings + paragraphs: tokenise inner text only when content is page-specific
# --------------------------------------------------------------------------
H1_PAT = re.compile(r'(<h1[^>]*>)([^<]+)(</h1>)', re.DOTALL)
H2_PAT = re.compile(r'(<h2[^>]*>)([^<]+)(</h2>)', re.DOTALL)
H3_PAT = re.compile(r'(<h3[^>]*>)([^<]+)(</h3>)', re.DOTALL)
SUBTITLE_PAT = re.compile(r'(<p\s+class="hero-subtitle"[^>]*>)([\s\S]*?)(</p>)')
TAGLINE_PAT  = re.compile(r'(<p\s+class="hero-tagline"[^>]*>)([\s\S]*?)(</p>)')
NOTE_PAT     = re.compile(r'(<p\s+class="note"[^>]*>)([\s\S]*?)(</p>)')
EYEBROW_LBL  = re.compile(r'(<span\s+class="breadcrumb-label"[^>]*>)([^<]+)(</span>)')


def tokenise_headings(body: str) -> str:
    body = SUBTITLE_PAT.sub(r'\1[[HERO-SUBTITLE]]\3', body)
    body = TAGLINE_PAT.sub(r'\1[[HERO-TAGLINE]]\3', body)
    body = NOTE_PAT.sub(r'\1[[SECTION-NOTE]]\3', body)
    body = EYEBROW_LBL.sub(r'\1[[BREADCRUMB-LABEL]]\3', body)
    body = H1_PAT.sub(r'\1[[HERO-HEADING]]\3', body)
    body = H2_PAT.sub(r'\1[[SECTION-HEADING]]\3', body)
    body = H3_PAT.sub(r'\1[[CARD-OR-ARTICLE-TITLE]]\3', body)
    return body


# --------------------------------------------------------------------------
# images: skip shared-infra logos; tokenise everything else
# --------------------------------------------------------------------------
IMG_PAT = re.compile(r'<img\s+[^>]*?>', re.IGNORECASE | re.DOTALL)
SRC_ATTR = re.compile(r'\bsrc="([^"]*)"')
ALT_ATTR = re.compile(r'\balt="([^"]*)"')


def is_shared_image(src_value: str) -> bool:
    return any(needle in src_value for needle in SHARED_IMAGE_NEEDLES)


def tokenise_images(body: str) -> str:
    def replace(m: re.Match) -> str:
        tag = m.group(0)
        src_match = SRC_ATTR.search(tag)
        if src_match and is_shared_image(src_match.group(1)):
            return tag
        tag = SRC_ATTR.sub('src="[[IMAGE-SRC]]"', tag)
        tag = ALT_ATTR.sub('alt="[[IMAGE-ALT]]"', tag)
        return tag
    return IMG_PAT.sub(replace, body)


# --------------------------------------------------------------------------
# section comments: inject a TEMPLATE SECTION marker above each <section>
# inside <main>. Auto-name from the section's first h1/h2 (captured from the
# ORIGINAL body, before tokenisation).
# --------------------------------------------------------------------------
SECTION_BOUND = re.compile(r'<section\b[^>]*>')
MAIN_OPEN = re.compile(r'<main\b[^>]*>')
MAIN_CLOSE = re.compile(r'</main\s*>', re.IGNORECASE)


def main_bounds(body: str) -> Tuple[int, int]:
    """Return (start, end) covering the inside of the first <main>...</main>.
    If no <main> is found, return (-1, -1)."""
    om = MAIN_OPEN.search(body)
    if not om:
        return -1, -1
    cm = MAIN_CLOSE.search(body, om.end())
    if not cm:
        return om.end(), len(body)
    return om.end(), cm.start()


def collect_section_names(original_body: str) -> List[str]:
    """In document order, return the first h1/h2 text inside each top-level
    <section> WITHIN <main>. Sections in the header/footer (e.g. Today's
    Special) are intentionally skipped — they are shared infrastructure,
    not page-specific content."""
    names: List[str] = []
    main_start, main_end = main_bounds(original_body)
    if main_start == -1:
        return names
    for m in SECTION_BOUND.finditer(original_body, main_start, main_end):
        # find the matching </section> by depth counting
        i = m.end()
        depth = 1
        while depth and i < len(original_body):
            nxt_open  = original_body.find("<section", i)
            nxt_close = original_body.find("</section>", i)
            if nxt_close == -1:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open + len("<section")
            else:
                depth -= 1
                i = nxt_close + len("</section>")
        chunk = original_body[m.end():i]
        # find first h1 then h2
        h = re.search(r'<h1[^>]*>([^<]+)</h1>', chunk)
        if not h:
            h = re.search(r'<h2[^>]*>([^<]+)</h2>', chunk)
        if not h:
            # fall back to aria-label of the section element itself
            arl = re.search(r'aria-label(?:ledby)?="([^"]+)"', m.group(0))
            names.append(arl.group(1).strip() if arl else f"Section {len(names)+1}")
        else:
            names.append(html.unescape(h.group(1)).strip())
    return names


def comment_for(name: str, idx: int) -> str:
    return (
        "\n      <!-- ================================================\n"
        f"        TEMPLATE SECTION {idx}: {name}\n"
        "        Replace inner [[TOKENS]] with page-specific content.\n"
        "        Keep all class names, IDs, and structural elements intact.\n"
        "      ================================================ -->"
    )


def inject_section_comments(body: str, names: List[str]) -> str:
    """Insert a TEMPLATE SECTION comment immediately before each <section>
    inside <main>. Section opening tags are unchanged by tokenisation, so
    positions align between the original and tokenised bodies. Sections
    outside <main> (e.g. the Today's Special block in the site header) are
    intentionally NOT annotated — they are shared infrastructure."""
    main_start, main_end = main_bounds(body)
    if main_start == -1:
        return body
    out_parts: List[str] = []
    last = 0
    idx = 0
    for m in SECTION_BOUND.finditer(body, main_start, main_end):
        idx += 1
        name = names[idx - 1] if idx - 1 < len(names) else f"Section {idx}"
        out_parts.append(body[last:m.start()])
        out_parts.append(comment_for(name, idx))
        out_parts.append(body[m.start():m.end()])
        last = m.end()
    out_parts.append(body[last:])
    return "".join(out_parts)


# --------------------------------------------------------------------------
# Today's-Special banner: tokenise the link target + body text
# --------------------------------------------------------------------------
TODAYS_SPECIAL = re.compile(
    r'(<a\s+class="site-specials-link"\s+href=")([^"]+)(">\s*)([^<]+?)(\s*</a>)',
    re.DOTALL,
)


def tokenise_todays_special(src: str) -> str:
    return TODAYS_SPECIAL.sub(
        r'\1[[TODAYS-SPECIAL-URL]]\3[[TODAYS-SPECIAL-TEXT]]\5', src
    )


# --------------------------------------------------------------------------
# template header comment block
# --------------------------------------------------------------------------
def header_block(page_type: str, source_path: str, template_filename: str) -> str:
    today = date.today().isoformat()
    return (
        "<!--\n"
        "  ============================================================\n"
        "  ASKJAMIE™ PAGE TEMPLATE\n"
        "  ============================================================\n"
        f"  Template Type  : {page_type}\n"
        f"  Source Page    : {source_path}\n"
        f"  Template Path  : /assets/templates/{template_filename}\n"
        f"  Generated      : {today}\n"
        "  Generator      : tools/generate-templates.py (Phase 13)\n"
        "  ============================================================\n"
        "  USAGE INSTRUCTIONS:\n"
        "  1. Copy this file to the appropriate directory and rename to index.html\n"
        "  2. Search for all [[ ]] tokens and replace with real content\n"
        "  3. Update the <link rel=\"canonical\"> to the new page's URL\n"
        "  4. Update all Open Graph og:url and og:title meta tags\n"
        "  5. Update the JSON-LD structured data values (replace the placeholder\n"
        "     object body with the page-specific schema content)\n"
        "  6. Add page-specific JavaScript if needed (do not remove existing tags)\n"
        "  7. Remove this comment block before publishing\n"
        "  ============================================================\n"
        "-->\n"
    )


# --------------------------------------------------------------------------
# main pipeline
# --------------------------------------------------------------------------
def generate_one(page_type: str, source_relpath: str) -> Path:
    source_path = ROOT / source_relpath
    src = source_path.read_text(encoding="utf-8")

    # collect section names BEFORE tokenisation
    section_names = collect_section_names(src)

    # transformation pipeline
    out = src
    out = tokenise_meta(out)
    out = clear_jsonld(out)
    out = tokenise_todays_special(out)
    out = tokenise_headings(out)
    out = tokenise_images(out)
    out = inject_section_comments(out, section_names)

    # prepend template header
    template_filename = f"template--{page_type}.html"
    out = header_block(page_type, source_relpath, template_filename) + out

    target = TEMPLATES_DIR / template_filename
    target.write_text(out, encoding="utf-8")
    return target


def main() -> int:
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []
    for page_type, source_relpath, _label in SOURCES:
        path = generate_one(page_type, source_relpath)
        written.append(path)
        print(f"  wrote {path.relative_to(ROOT)}  (from {source_relpath})")
    print(f"\nGenerated {len(written)} template(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

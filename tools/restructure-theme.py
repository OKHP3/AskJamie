#!/usr/bin/env python3
"""
Reorder assets/css/theme.css into a stable, diff-friendly structure:

    1. GLOBAL    — common to all three sites
    2. OKH       — OverKill Hill brand-specific
    3. GLEE      — Glee-fully Tools brand-specific
    4. ASKJAMIE  — AskJamie brand-specific

This script uses an EXPLICIT line-range map (below).  It does NOT modify any
section's content — it only re-orders sections and wraps them with banners.

Re-running on an already-reorganised file will fail (line ranges no longer
match).  Always run against a known-good source.

USAGE
    cp assets/css/theme.css assets/css/theme.css.bak   # safety backup
    python3 tools/restructure-theme.py                  # reorganise in place
"""
from pathlib import Path
import datetime
import sys

SRC  = Path('assets/css/theme.css.bak')   # read from snapshot
DEST = Path('assets/css/theme.css')        # write reorganised file

# (start_line, end_line, tier, label)   — both endpoints INCLUSIVE, 1-indexed.
SECTIONS = [
    # ── GLOBAL ──────────────────────────────────────────
    (5, 71,      'GLOBAL', 'ROOT TOKENS'),
    (72, 139,    'GLOBAL', 'RESET & BASE'),
    (140, 170,   'GLOBAL', 'UTILS & LAYOUT — vertical rhythm + dividers'),
    (171, 325,   'GLOBAL', 'UTILS & LAYOUT — grid, cards, buttons, sr-only, skip-link'),
    (326, 398,   'GLOBAL', 'HEADER & NAV'),
    (399, 516,   'GLOBAL', 'Primary nav: About submenu (shared dropdown pattern)'),
    (517, 556,   'GLOBAL', 'HEADINGS VARIANTS'),
    (557, 629,   'GLOBAL', 'PRE-OPENING / ACTIVE BUILD NOTE'),
    (630, 672,   'GLOBAL', 'LATEST MILESTONE highlight'),
    (673, 725,   'GLOBAL', 'Newest Addition image zone'),
    (726, 869,   'GLOBAL', 'BRAND HEADER VARIANTS (subsite-shared paper header)'),
    (1014, 1102, 'GLOBAL', 'BRAND SIGNATURE STRIPES (shared keyframe animation)'),
    (1103, 1179, 'GLOBAL', 'SECTION STYLES'),
    (1180, 1230, 'GLOBAL', 'FOOTER'),
    (1231, 1268, 'GLOBAL', 'SCROLL REVEAL + chat mock (shared structure)'),
    (2534, 3138, 'GLOBAL', 'ARTICLE-SPECIFIC STYLES (long-form pages)'),
    (3139, 3230, 'GLOBAL', 'Under-construction overlay (used by all subsites)'),
    (3286, 3321, 'GLOBAL', 'Ko-fi support section'),
    (3322, 3436, 'GLOBAL', 'GPT Hero Card (reusable component)'),
    (3559, 3681, 'GLOBAL', 'CROSS-SITE SYNC utilities + inline-style extractors'),
    (3682, 4010, 'GLOBAL', 'SITE SEARCH (header trigger + modal overlay)'),

    # ── OVERKILL HILL P³ ────────────────────────────────
    (870, 1013,  'OKH', 'HERO — BLUEPRINT FORGE (OKH homepage hero)'),
    (1269, 1335, 'OKH', 'OKH under-construction hero + custom 404 page'),
    (1336, 1395, 'OKH', 'Mermaid — default OKH look (uses :not() to skip subsites)'),

    # ── GLEE-FULLY PERSONALIZABLE TOOLS ─────────────────
    (1760, 1855, 'GLEE', 'Glee Mermaid shell + retro-joyful base'),
    (1940, 1975, 'GLEE', '.glee-main tokens + body styles'),
    (1976, 2171, 'GLEE', 'Glee-fully hero layering'),
    (2172, 2236, 'GLEE', 'About page hero — paper effect'),
    (2237, 2335, 'GLEE', 'Contact page hero — paper effect'),
    (2336, 2443, 'GLEE', 'Legal page hero — paper effect'),
    (2444, 2511, 'GLEE', 'Glee-fully general styles'),
    (2512, 2533, 'GLEE', 'Secondary button + Glee accent variant'),
    (3231, 3285, 'GLEE', 'Glee Mermaid refined skin (supersedes earlier block in cascade)'),

    # ── ASKJAMIE ────────────────────────────────────────
    (1396, 1528, 'ASKJAMIE', '.askjamie-main tokens + paper hero'),
    (1529, 1759, 'ASKJAMIE', 'AskJamie system pages (404, under-construction)'),
    (1856, 1939, 'ASKJAMIE', 'AskJamie Mermaid (mid-century teal)'),
    (3437, 3447, 'ASKJAMIE', 'GPT Hero Card — BFS brand variant'),
    (3448, 3558, 'ASKJAMIE', 'BFS Framing Intelligent Futures hero'),
]

TIER_ORDER = ['GLOBAL', 'OKH', 'GLEE', 'ASKJAMIE']
TIER_BANNER = {
    'GLOBAL':   '1. GLOBAL — common to all three sites',
    'OKH':      '2. OVERKILL HILL P3 — brand-specific',
    'GLEE':     '3. GLEE-FULLY PERSONALIZABLE TOOLS — brand-specific',
    'ASKJAMIE': '4. ASKJAMIE — brand-specific',
}


def main() -> int:
    if not SRC.exists():
        print(f"  ✗ Backup file {SRC} not found.  Make one first:")
        print(f"      cp assets/css/theme.css {SRC}")
        return 2

    src_lines = SRC.read_text(encoding='utf-8').split('\n')
    n = len(src_lines)

    # ── Coverage check ────────────────────────────────────────────────
    covered: dict[int, str] = {}
    overlaps = []
    for start, end, tier, label in SECTIONS:
        for ln in range(start, end + 1):
            if ln in covered:
                overlaps.append((ln, covered[ln], label))
            covered[ln] = label

    missing = [ln for ln in range(5, n + 1) if ln not in covered and src_lines[ln-1].strip()]

    if overlaps:
        print(f"  ⚠️  {len(overlaps)} overlaps detected:")
        for ln, a, b in overlaps[:10]:
            print(f"     line {ln}: '{a}' vs '{b}'")
    if missing:
        print(f"  ⚠️  {len(missing)} non-blank source lines uncovered: {missing[:15]}")

    # ── Header + TOC ──────────────────────────────────────────────────
    today = datetime.date.today().isoformat()
    header_block = [
        '/* OverKill Hill P3 Universe - 2025 Cross-Site Theme',
        '   Source of truth shared by:',
        '     - OverKill Hill        (overkillhill.com)',
        '     - Glee-fully Tools     (glee-fully.tools)',
        '     - AskJamie             (askjamie.bot)',
        '',
        '   Update workflow: edit one site, paste the result into the other two so',
        '   all three stay in lock-step.  Section order is stable so diffs are surgical.',
        '',
        '   Sections are grouped:',
        '     1. GLOBAL    - common to all three sites',
        '     2. OKH       - OverKill Hill brand-specific overrides',
        '     3. GLEE      - Glee-fully Tools brand-specific overrides',
        '     4. ASKJAMIE  - AskJamie brand-specific overrides',
        '',
        f'   Last reorganised: {today}',
        '   Tool: tools/restructure-theme.py',
        '*/',
        '',
        '/* SECTION INDEX',
    ]
    for tier in TIER_ORDER:
        header_block.append(f'   -- {tier} --')
        for start, end, t, label in SECTIONS:
            if t == tier:
                span = end - start + 1
                # The L*-* numbers refer to the ORIGINAL source-of-truth line
                # range (from theme.css.bak) so historical diffs stay legible.
                # Once a section is moved into the new file its actual line
                # number changes; the source range stays stable.
                header_block.append(f'     - src L{start}-{end} ({span:>4} lines)  {label[:62]}')
    header_block.append('*/')
    header_block.append('')

    def banner(label: str) -> list[str]:
        line = '=' * 70
        return [
            '',
            f'/* {line}',
            f'   {label}',
            f'   {line} */',
            '',
        ]

    # ── Assemble output ───────────────────────────────────────────────
    out: list[str] = []
    out.extend(header_block)
    for tier in TIER_ORDER:
        out.extend(banner(TIER_BANNER[tier]))
        for start, end, t, label in SECTIONS:
            if t != tier:
                continue
            chunk = src_lines[start-1:end]
            out.extend(chunk)
            out.append('')

    new_text = '\n'.join(out).rstrip() + '\n'
    DEST.write_text(new_text, encoding='utf-8')

    # ── Verification ──────────────────────────────────────────────────
    src_text = '\n'.join(src_lines)
    s_open  = src_text.count('{')
    s_close = src_text.count('}')
    n_open  = new_text.count('{')
    n_close = new_text.count('}')

    print(f"\n  Source     : {len(src_lines):>5} lines  {s_open:>4} opens  {s_close:>4} closes")
    print(f"  Rewritten  : {len(new_text.splitlines()):>5} lines  {n_open:>4} opens  {n_close:>4} closes")

    if s_open != n_open or s_close != n_close:
        print('\n  ✗ BRACE COUNT CHANGED — restoring backup.')
        DEST.write_text(src_text, encoding='utf-8')
        return 1

    print('\n  ✓ Brace counts preserved; restructure complete.')
    print(f"\n  Sections by tier:")
    for tier in TIER_ORDER:
        items = [s for s in SECTIONS if s[2] == tier]
        total_lines = sum(end - start + 1 for start, end, _, _ in items)
        print(f"    {tier:<8} {len(items):>2} sections, {total_lines:>5} lines")
    return 0


if __name__ == '__main__':
    sys.exit(main())

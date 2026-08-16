---
name: AskJamie contrast ratio corrections
description: Two originally reported contrast failures were arithmetic errors; both ratios pass AA
---

## Corrections from 2026-08-16 audit

### S-01 (retracted) — Muted text
- Claimed: `#6b6b6b` on `#f6f2ee` = 4.21:1 FAIL
- Verified: actual ratio = **4.78:1 PASS** (AA threshold 4.5:1)
- Action: muted text was still darkened to `#5a5a5a` (now 6.19:1) as a margin improvement

### S-02 (retracted) — Footer links
- Claimed: `#2d6f7e` on `#020617` = 3.87:1 FAIL
- Wrong background: AskJamie overrides the global dark footer with `background: #f7f3ee`
- Verified: `#2d6f7e` on `#f7f3ee` = **5.16:1 PASS**
- The `#020617` dark footer applies to OKH (OverKill Hill) pages only, not askjamie.bot

## Correct Python contrast calculation
```python
def linearize(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def luminance(r, g, b):
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)
def contrast(hex1, hex2):
    l1 = luminance(*bytes.fromhex(hex1.lstrip('#')))
    l2 = luminance(*bytes.fromhex(hex2.lstrip('#')))
    li, da = max(l1, l2), min(l1, l2)
    return (li + 0.05) / (da + 0.05)
```
Always use Python; manual arithmetic has failed twice.

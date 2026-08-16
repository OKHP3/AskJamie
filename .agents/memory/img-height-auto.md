---
name: img height=auto removal side-effect
description: Removing height="auto" from img tags triggers "missing width/height" audit failures — must replace with explicit pixel values
---

## Rule
When removing `height="auto"` from `<img>` tags (which is invalid HTML), always add a concrete pixel height back. Do not leave the attribute absent — the audit script checks that both width and height are present.

**Why:** `height="auto"` is invalid HTML per spec. But removing it without adding an explicit value causes `audit-site.py` to flag "Image missing width/height" on every affected page.

## How to apply
For square images (filename contains `-square-`): set `height` equal to the `width` value already present.
For non-square images: check the actual image dimensions (width÷height ratio) and compute the correct height for the rendered width.

Logo image used on all 26+ pages:
- `askjamie-title-cream-blue-backdrop-blue-gray-left-square-1024.png` — 1024×1024 square
- Rendered at width="160" → use height="160"
- Rendered at width="200" (index.html hero) → use height="200"

The Python fix pattern (see 2026-08-16 session) re-adds height by matching the width for known square images.

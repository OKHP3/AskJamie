# OG Image Requirements — AskJamie™
*Generated: 2026-05-26 (Task #1 documentation)*
*Updated: 2026-05-28 (Task #23) — All 20 images converted to WebP; PNGs remain as orphaned source masters*

> **Status as of 2026-05-28:** All 20 OG images have been generated and are live in
> `assets/img/og/` as **WebP** files (23–92 KB each, down from 600 KB–1.2 MB PNG originals).
> All HTML pages reference the `.webp` versions with `og:image:type = image/webp`.
> The original `.png` source files remain in the same directory but are no longer referenced.

## The Problem

All pages currently use a **1024×1024** square avatar PNG as their Open Graph image.
The gold standard for social sharing is **1200×630 landscape** (16:9-ish).
Twitter/X and Facebook crop square images to landscape in card previews, cutting off
roughly a third of the image height and often decapitating the AskJamie™ character.

---

## Required Images

### Priority 1 — High-traffic / link-shared pages

| Page | Path | Suggested filename |
|------|------|--------------------|
| Homepage | `/` | `og-homepage-1200x630.png` |
| Lens System hub | `/lens-system/` | `og-lens-system-1200x630.png` |
| BrandGuard™ hub | `/lens-system/okhp3-brandguard/` | `og-brandguard-hub-1200x630.png` |
| BFS — Framing Intelligent Futures | `/lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/` | `og-bfs01-1200x630.png` |
| Contact | `/contact/` | `og-contact-1200x630.png` |

### Priority 2 — Lens System GPT pages

| Page | Path | Suggested filename |
|------|------|--------------------|
| Résumé Representative (AJ01) | `/lens-system/resume-representative/` | `og-aj01-resume-rep-1200x630.png` |
| Professional Portfolio (AJ02) | `/lens-system/professional-portfolio/` | `og-aj02-portfolio-1200x630.png` |
| Enterprise Sleuth™ (AJ03) | `/lens-system/enterprise-sleuth/` | `og-aj03-sleuth-1200x630.png` |

### Priority 3 — BrandGuard™ case studies (shared template)

All 12 remaining BRG case studies can share a single landscape template with a
brand-specific logo or name swapped in. Suggested: one reusable template
`og-brandguard-case-template-1200x630.psd/.fig` and one rendered PNG per case.

| Case | Filename |
|------|----------|
| LEGO | `og-brg01-lego-1200x630.png` |
| Starbucks | `og-brg02-starbucks-1200x630.png` |
| Brooks Running | `og-brg03-brooks-running-1200x630.png` |
| Ping (Golf) | `og-brg04-ping-1200x630.png` |
| Costco | `og-brg05-costco-1200x630.png` |
| Hershey | `og-brg06-hershey-1200x630.png` |
| LVMH | `og-brg07-lvmh-1200x630.png` |
| Dollar General | `og-brg08-dollar-general-1200x630.png` |
| Coca-Cola | `og-brg09-coca-cola-1200x630.png` |
| Discount Tire | `og-brg10-discount-tire-1200x630.png` |
| Scheels | `og-brg11-scheels-1200x630.png` |
| Mathews Archery | `og-brg12-mathews-archery-1200x630.png` |

---

## Specifications

| Attribute | Required value |
|-----------|---------------|
| **Dimensions** | 1200 × 630 px |
| **Format** | PNG or JPEG (.jpg) |
| **Max file size** | 1 MB (aim for ≤ 400 KB with PNG compression) |
| **Safe zone** | Keep key content within central 1000×500 px (100 px bleed on all sides) |
| **Text minimum size** | 32 px at 1200 px canvas (or ≥ 2.67% image height) |
| **Alt text** | Must be updated in `og:image:alt` + `twitter:image:alt` meta tags |

---

## Composition Guidance

### Adaptable source assets

The following existing assets could be adapted to landscape format:

- `assets/img/AskJamie TitleCreamBlueBackdropBlueGrayLeft Square 1024.png` —
  the title card. Place left-of-center with 630 px height, add branded copy
  on the right half.
- `assets/img/AskJamie AvatarTallLeft Square 1024.png` — the tall avatar.
  Crop to show top 2/3, place right-of-center as a visual anchor.
- `assets/img/BrandGuard/*.png` — brand-specific avatars. Already in 1024×1024;
  use as the right-side element with brand-color background on the left half.

### Suggested layout

```
┌──────────────────────────────────────────┐
│  [Logo mark]  [H1 Page title]             │ ← top-left
│                                            │
│  [Tagline or description — 1 short line]  │ ← center-left
│                                  [Avatar] │ ← right anchor
│                          askjamie.bot     │ ← bottom-right URL
└──────────────────────────────────────────┘
```

Background: AskJamie™ brand teal (`#2c5e6f`) or cream (`#f5efe1`) depending on
the page's light/dark treatment.

---

## How to Update a Page Once Images Are Produced

1. Save the image to `assets/img/og/` (create this folder).
2. Update the `og:image`, `og:image:alt`, `og:image:width`, `og:image:height`
   meta tags on the target page:

```html
<meta property="og:image" content="https://askjamie.bot/assets/img/og/og-homepage-1200x630.webp" />
<meta property="og:image:type" content="image/webp" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="AskJamie™ — your articulate AI persona" />
```

3. Update `twitter:image` and `twitter:image:alt` to match.
4. Rebuild the search index (`python3 scripts/build-search-index.py`).
5. Re-run the auditor (`python3 scripts/audit-site.py`) to confirm 0 issues.

---

## Notes

- Facebook's crawler requires images to be at least **200×200 px** and ≤ 8 MB.
  The 1200×630 spec satisfies this and the Twitter `summary_large_image` card spec.
- LinkedIn recommends **1200×627 px** — 1200×630 renders fine.
- The current 1024×1024 images will continue to render; this is an enhancement,
  not a blocker.
- `apply-modern-baseline.py` does not touch OG image tags — update manually per page.

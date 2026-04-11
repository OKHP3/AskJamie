# AskJamie™ — Replit App Theme

Reverse-engineered from `assets/css/theme.css` (`.askjamie-main` block).
Enter these values into the **Manage app themes** panel field by field.

---

## FOUNDATION — Colors

| Field | Value | Notes |
|---|---|---|
| Background color | `#f6f2ee` | AskJamie Paper — warm cream page background |
| Text color | `#2e2b29` | Warm espresso near-black — primary readable text |
| Muted background color | `#fdfbf7` | Lighter paper — card and panel surfaces |
| Muted text color | `#6b6b6b` | Warm gray — captions, metadata, secondary labels |

---

## FOUNDATION — Typography

| Field | Value | Notes |
|---|---|---|
| Sans-serif font | `Open Sans` | Primary body font — loaded from Google Fonts |
| Serif font | `Georgia` | No serif used in this design; nearest universal fallback |
| Monospace font | `Menlo` | No monospace in this design; browser/system default |

> **Note on Open Sans:** This is a Google Font. If the Replit theme panel does not list it by name,
> it will fall back to the system sans-serif, which is fine for the theme config.
> The actual site loads it via:
> `https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600&display=swap`

---

## FOUNDATION — Shape & Spacing

| Field | Value | Notes |
|---|---|---|
| Border radius | `0.75` rem | Standard card/component radius (--radius-md). Buttons use 999px pills. |

---

## COMPONENTS — Actions

| Field | Value | Notes |
|---|---|---|
| Primary background | `#2d6f7e` | AskJamie Teal — primary CTA buttons gradient start |
| Primary text | `#f9fafb` | Off-white — high contrast on teal |
| Secondary background | `#2e2b29` | Espresso dark — secondary/ghost button bg |
| Secondary text | `#ffffff` | White text on dark secondary buttons |
| Accent background | `#007c84` | Deep teal — hero stripe, strong accent |
| Accent text | `#f6f2ee` | Cream — readable on deep teal (the AskJamie contrast pair) |
| Destructive background | `#c53030` | Dark red — harmonizes with warm palette |
| Destructive text | `#ffffff` | White — readable on dark red |

---

## COMPONENTS — Forms

| Field | Value | Notes |
|---|---|---|
| Input | `#fdfbf7` | Paper surface — matches card background |
| Border | `#d7d7d7` | Light warm gray — visible on cream backgrounds |
| Focus Border | `#2d6f7e` | AskJamie Teal — matches `outline: 2px solid var(--color-accent)` in CSS |

---

## COMPONENTS — Containers

| Field | Value | Notes |
|---|---|---|
| Card background | `#fdfbf7` | Lighter paper — same as `--color-surface` |
| Card text | `#2e2b29` | Warm espresso — same as primary text |
| Popover background | `#fdfbf7` | Paper surface — consistent with card and input |
| Popover text | `#2e2b29` | Warm espresso — primary readable text |

---

## COMPONENTS — Charts

Five colors drawn directly from the AskJamie™ brand stripe palette for maximum on-brand consistency. They progress cool → warm across the range to ensure adjacent series are always distinguishable.

| Field | Value | Name | Notes |
|---|---|---|---|
| Chart 1 | `#2d6f7e` | AskJamie Teal | Primary brand color — leads every chart |
| Chart 2 | `#76b2ba` | Stripe Aqua | Lighter teal — same hue family, lower saturation |
| Chart 3 | `#e6a03c` | OKH Amber | Warm contrast — breaks the cool run, high legibility |
| Chart 4 | `#d5ba9a` | Stripe Warm Beige | Neutral mid-tone — soft separator between warm series |
| Chart 5 | `#69584c` | Stripe Mocha | Dark warm anchor — high contrast endpoint |

> These are all pulled directly from the hero brand stripe in `theme.css`. They reflect exactly the colors already visible in the site's visual identity.

---

## Full Colour Palette Reference

All named tokens from the `.askjamie-main` block in `theme.css`.

| Token name | Hex | Role |
|---|---|---|
| `--color-bg` | `#f6f2ee` | Paper base — body / page canvas |
| `--color-surface` | `#fdfbf7` | Card / panel background (lighter paper) |
| `--color-surface-soft` | `#f6f2ee` | Same as bg — soft inset panels |
| `--color-fg` | `#2e2b29` | Primary foreground text (warm espresso) |
| `--color-muted` | `#6b6b6b` | Muted gray — secondary text |
| `--color-accent` | `#2d6f7e` | AskJamie teal — links, active nav, focus rings, primary actions |
| `--color-border-subtle` | `#d7d7d7` | Form borders, card dividers |
| `stripe-deep-teal` | `#007c84` | Hero stripe — deep teal (accent bg) |
| `stripe-aqua` | `#76b2ba` | Hero stripe / Chart 2 — light aqua |
| `stripe-cream` | `#f5ead9` | Hero stripe — warm cream |
| `stripe-warm-beige` | `#d5ba9a` | Hero stripe / Chart 4 — warm beige |
| `stripe-mocha` | `#69584c` | Hero stripe / Chart 5 — dark mocha |
| `teal-hover` | `#3c8ea1` | Teal hover / CTA gradient end |
| `okh-amber` | `#e6a03c` | Chart 3 — shared OKH amber, warm contrast |
| `header-bg` | `#f6f2ee` | Nav header background |
| **Primary CTA gradient** | `linear-gradient(135deg, #2d6f7e, #3c8ea1)` | Buttons — teal to aqua diagonal |

---

## Heading Font

`Baloo 2` — loaded from Google Fonts. Rounded display font used exclusively for H1/H2 headings.
The site uses a three-font system: **Baloo 2** (headings) + **Open Sans** (body) + **Kalam** (handwritten accent).

Google Fonts URL:
```
https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Open+Sans:wght@400;500;600&family=Kalam:wght@400;700&display=swap
```

---

*Generated from askjamie.bot theme — 2026-04-10 · Updated 2026-04-11 (Focus Border, Containers, Charts)*

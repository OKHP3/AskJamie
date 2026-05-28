# Dark/Light Mode — Cross-Site CSS Diff Report

**Generated:** 2026-05-28  
**Scope:** `assets/css/theme.css` across all three sister sites  
**Sources compared:**
- `https://github.com/OKHP3/AskJamie/blob/main/assets/css/theme.css` (4 584 lines)
- `https://github.com/OKHP3/OverKill-Hill/blob/main/assets/css/theme.css` (5 521 lines)
- `https://github.com/OKHP3/Glee-fullyTools/blob/main/assets/css/theme.css` (5 505 lines)

---

## Summary table

| # | Area | AskJamie | OKH | Glee | Winner / Resolution |
|---|------|----------|-----|------|---------------------|
| 1 | `:root[data-theme="light"]` tokens | neutral white (#f9fafb) | warm paper (#eff2f5) | neutral white (#f9fafb) | **OKH** keeps warm paper (brand); Glee/AskJamie already override via body-class scope |
| 2 | Body background selector | `body[data-theme]` ❌ | `html[data-theme] body` ✅ | `html[data-theme] body` ✅ | **OKH/Glee** — `html[data-theme]` is correct; AskJamie bug fixed in Task #31 |
| 3 | Toggle HTML attribute | `data-theme` | `data-theme` | `data-color-scheme` ⚠ | **`data-theme`** — canonical for shared system; Glee's `data-color-scheme` is a Glee-local extension |
| 4 | Toggle button class | `.theme-toggle` | `.theme-toggle` | `.glee-color-toggle` | **Both coexist** — add `.glee-color-toggle` styles to GLEE tier (already `.glee-main`-scoped) |
| 5 | Toggle button style | emoji pill (🌓) | emoji pill (🌓) | SVG sun/moon/auto icon ✅ | **Glee** wins on UX — `.glee-color-toggle` added to staged OKH patch |
| 6 | Toggle state count | 2-state (light/dark) | 2-state (light/dark) | 3-state (light/dark/auto) ✅ | **Glee** wins — 3-state with `auto` (system preference) is best practice |
| 7 | `localStorage` key | `okh-theme` | `okh-theme` | `glee-color-scheme` | Site-specific keys are intentional — no change needed |
| 8 | AskJamie dark mode forced-off | Forces `data-theme="light"` ❌ | N/A | N/A | **Bug** — AskJamie JS forces light; fixed in Task #31 |
| 9 | `@media (prefers-color-scheme: dark)` brand block | None ❌ | None (dark-by-default) ✅ | Comprehensive `.glee-main` block ✅ | OKH correct (dark default). AskJamie needs a `.askjamie-main` block (Task #31) |
| 10 | Anti-FOSC on DOMContentLoaded | ❌ missing (overridden to light) | ✅ restores stored pref | ✅ restores stored pref | **OKH/Glee** — AskJamie fix in Task #31 |

---

## Divergence detail

### 1 · `:root[data-theme="light"]` token values

The light-mode CSS custom property overrides differ between OKH (warm paper) and Glee/AskJamie (neutral white):

| Token | AskJamie | OKH | Glee |
|-------|----------|-----|------|
| `--color-bg` | `#f9fafb` | `#eff2f5` | `#f9fafb` |
| `--color-surface` | `#ffffff` | `#f6f2ee` | `#ffffff` |
| `--color-surface-soft` | `#f3f4f6` | `#f0ebe5` | `#f3f4f6` |
| `--color-fg` | `#0f172a` | `#0f172a` | `#0f172a` |
| `--color-muted` | `#4b5563` | `#4b5563` | `#4b5563` |

**Resolution:** The `:root[data-theme="light"]` block lives in the GLOBAL tier and is the OKH-default layer. OKH's warm paper values are correct for its brand. Glee and AskJamie are *light-by-default* sites that define their entire surface palette via `.glee-main` / `.askjamie-main` body-class scoping — the `:root` light-mode tokens don't materially affect them in practice. **No change needed for OKH.**

---

### 2 · Body background selector — AskJamie bug

AskJamie's CSS uses `body[data-theme="dark"]` and `body[data-theme="light"]` but the JS sets `data-theme` on `document.documentElement` (i.e. `<html>`). The selector never matches, so the background swap silently fails.

**OKH** and **Glee** both correctly use `html[data-theme="dark"] body` and `html[data-theme="light"] body`.

**Resolution:** AskJamie bug — fixed in Task #31. The OKH staged file already uses the correct selectors.

---

### 3 · Toggle HTML attribute: `data-theme` vs `data-color-scheme`

Glee's JS toggle sets `html[data-color-scheme]` (a Glee-specific attribute), while OKH and AskJamie set `html[data-theme]`. Glee's CSS has explicit override blocks for both:

- `html[data-theme]` — inherited from the shared theme, governs OKH-side component styles
- `html[data-color-scheme]` — Glee-local, governs Glee-specific explicit dark/light overrides

This means Glee has two parallel attribute systems. The `@media (prefers-color-scheme: dark)` block handles the "auto" (system preference) case; `html[data-color-scheme="dark"]` handles the forced-dark case; and `html[data-color-scheme="light"]` handles forced-light on a system that prefers dark.

**Resolution:** `data-theme` remains the canonical attribute for the shared design system. Glee's `data-color-scheme` is a deliberate Glee extension — it coexists without conflict. When implementing the AskJamie toggle in Task #31, use `data-theme` (not `data-color-scheme`) to stay aligned with the shared CSS selectors.

---

### 4 + 5 · Toggle button: `.theme-toggle` vs `.glee-color-toggle`

| Attribute | `.theme-toggle` (OKH/AskJamie) | `.glee-color-toggle` (Glee) |
|-----------|-------------------------------|----------------------------|
| Shape | pill (border-radius 999px) | circle (border-radius 50%) |
| Size | auto (padding 0.25/0.6rem) | 34 × 34 px fixed |
| Icon | 🌓 emoji (font character) | SVG sun / moon / half-circle |
| Background | `rgba(15,23,42,0.7)` dark | transparent |
| Scope | unscoped (all brands) | `.glee-main`-scoped |

The `.glee-color-toggle` is superior: SVG icons scale crisply, accessibility attributes are properly managed (`aria-label` updates per state, `aria-pressed` used), and the transparent-background circular style works on both light and dark headers.

**Resolution:** Both button classes now coexist in the staged OKH `theme.css`. The `.glee-color-toggle` styles have been added to the GLEE tier of `assets/docs/sister-site-sync/okh/theme.css`. A similar `.askjamie-color-toggle` button is scoped for AskJamie in Task #31.

---

### 6 · Toggle state count: 2-state vs 3-state

Glee's toggle cycles through **three states**:

1. **`light`** — forces light mode (ignores system preference); `localStorage["glee-color-scheme"] = "light"`
2. **`dark`** — forces dark mode; `localStorage["glee-color-scheme"] = "dark"`
3. **`auto`** — removes the stored key; `@media (prefers-color-scheme: dark)` governs

OKH and AskJamie only toggle between `light` and `dark`, storing the choice in `localStorage["okh-theme"]`. There is no "follow system" option.

**Resolution:** The 3-state pattern is best practice and is recommended for all three sites. The OKH and AskJamie JS should be upgraded to the 3-state pattern. This is captured in Task #31 for AskJamie. When applying the OKH patch, upgrading the OKH JS toggle from 2-state to 3-state is optional but recommended (see JS upgrade notes below).

---

### 7 · `localStorage` keys

| Site | Key | 
|------|-----|
| OKH | `okh-theme` |
| AskJamie | `okh-theme` (same — both use OKH default) |
| Glee | `glee-color-scheme` |

These are intentionally site-specific to avoid cross-domain bleed (different domains, no shared storage). No change needed.

---

### 8 · AskJamie forces light mode — toggle dead on arrival

The AskJamie JS `initTheme()` function runs:

```js
// Subsites (Glee, AskJamie) are visually committed to their light look
document.documentElement.setAttribute("data-theme", "light");
```

This overwrites any stored `localStorage["okh-theme"]` preference and pins AskJamie to light mode on every page load. The toggle button fires correctly (updating the attribute), but the next page load resets it.

**Resolution:** Remove the forced `data-theme="light"` override for AskJamie. Instead, apply the stored preference (or no attribute, letting the brand default CSS take effect). Fixed in Task #31.

---

### 9 · `@media (prefers-color-scheme: dark)` brand coverage

**Glee** has a ~100-line `@media (prefers-color-scheme: dark)` block scoped to `.glee-main` that covers: token overrides, site header, nav links, mobile toggle, submenu, cards, footer, hero, stripe sections, site-status, site-specials, and the color-toggle button itself.

**OKH** has no such block — and doesn't need one. OKH's default palette is already dark (deep blueprint colors). Its light mode is the opt-in variant.

**AskJamie** has no such block — and **does** need one. AskJamie is light-by-default (like Glee). Without a dark-mode block, toggling to dark leaves hardcoded light-colored surfaces unaffected and the page looks broken. This is addressed in Task #31.

---

### 10 · Anti-FOSC handling

A Flash of Un-Styled Color (FOSC / FOUC) occurs when the page loads with the wrong theme briefly before JS runs. The fix is to apply the stored preference synchronously in a `<script>` in `<head>` before any rendering.

- **Glee JS**: Has a backup restore in `init()` but notes it's a "backup for pages without the anti-FOSC inline script", suggesting Glee pages include an inline script in `<head>`.
- **OKH JS**: Restores `localStorage["okh-theme"]` in `DOMContentLoaded` — handles most cases but not instant-on.
- **AskJamie JS**: Overrides to `data-theme="light"` — FOSC-free but toggle is broken.

**Resolution for Task #31:** Add a minimal inline `<script>` in `<head>` of each AskJamie page to apply the stored theme preference before first paint. This follows best practice and is documented in the Glee source.

---

## Changes applied to staged OKH `theme.css`

The following changes have been made to `assets/docs/sister-site-sync/okh/theme.css`:

### Added: `.glee-color-toggle` button styles (GLEE tier, end of section)

Added the full `.glee-color-toggle` component block immediately before the `SECTION · ASKJAMIE` banner. Styles are scoped to `.glee-main` so they have zero effect on OKH's default brand. Block includes:

- Base button styles (34×34 circular, transparent, SVG icon)
- Hover and focus-visible states
- `@media (prefers-color-scheme: dark)` variant (for the "auto" state visual)
- `html[data-color-scheme="dark"] .glee-main` explicit-dark overrides
- `html[data-color-scheme="light"] .glee-main` explicit-light overrides

---

## What is NOT changed (and why)

| Item | Decision |
|------|----------|
| OKH's warm-paper `:root[data-theme="light"]` values | Intentional brand choice — keep |
| OKH's 2-state JS toggle | Optional upgrade to 3-state; not changed in CSS-only patch |
| `data-theme` attribute name | Canonical — no change |
| AskJamie live files | Strictly out of scope for this task — covered by Task #31 |
| Glee CSS or JS files | Glee repo was empty at last check — nothing to update |

---

## Recommended next actions for OKH owner

1. **Apply the staged CSS patch** — copy `assets/docs/sister-site-sync/okh/theme.css` into the OKH repo
2. **Optional JS upgrade** — upgrade the OKH `theme-toggle` from 2-state to 3-state using the Glee pattern from `assets/js/app.js` lines 922–1030
3. **Optional anti-FOSC** — add `<script>` in each HTML page `<head>` to restore `localStorage["okh-theme"]` before first paint
4. **Verify** — run `python3 scripts/audit-site.py --quiet` (0 issues expected; the CSS patch is additive only)

# Hosted JavaScript Smoke Check

**Checked:** 2026-08-22  
**Published origin:** `https://askjamie.bot`  
**Method:** Playwright Chromium against the documented published site origin.

Replit deployment metadata reported no active Replit deployment for this
repository. The check therefore used the site’s documented public origin,
`https://askjamie.bot`, rather than inventing a Replit deployment URL.

## Result

The existing smoke suite passed:

```text
JavaScript smoke tests passed: Mermaid, search overlay, and dark mode.
```

The hosted browser probe also passed all targeted checks:

- Universe Mermaid rendered one SVG node.
- The configured Mermaid ESM module loaded from
  `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`.
- All 27 observed Mermaid CDN module responses returned HTTP 200.
- Search opened, accepted `BrandGuard`, and closed with Escape.
- The theme toggle changed the hosted document to `data-theme="dark"`.
- The JavaScript-disabled Universe fallback remained covered by the existing
  smoke test.
- Hosted routes `/`, `/universe/`, `/search/`, and `/about/` each returned
  HTTP 200.

## Reproduction

Run the existing smoke suite against the published origin:

```bash
BASE_URL=https://askjamie.bot node tests/test_js_smoke.spec.mjs
```

The hosted check found no CDN loading, routing, or JavaScript behavior
differences from the local smoke path.
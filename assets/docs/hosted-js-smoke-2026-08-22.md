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
- The configured Mermaid ESM module loaded from the site's local
  `/assets/vendor/mermaid/mermaid.esm.min.mjs` runtime.
- The locally vendored Mermaid module and its chunks returned successfully.
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

The repeatable GitHub Actions workflow is
`.github/workflows/hosted-js-smoke.yml`. It runs on demand and daily, outside
the static validation and deploy job, so a temporary hosted-service failure
cannot rewrite content or be mistaken for a local build failure.

When it fails, inspect the route named in the smoke-test assertion or
navigation error. A `request failed` line naming `/assets/vendor/mermaid/`
indicates a local Mermaid module or chunk loading problem; a `browser console
error` line identifies a runtime error. HTTP navigation or Mermaid timeouts
should be rerun before being treated as a persistent hosted regression, because
they can reflect a transient origin or network failure.

The hosted check found no local Mermaid loading, routing, or JavaScript behavior
differences from the local smoke path on the recorded check date.

## Retained workflow evidence

Beginning with the workflow hardening recorded on 2026-08-24, every scheduled
or manually triggered hosted run uploads a small artifact named
`hosted-js-smoke-<run number>-<attempt>`. Each artifact contains:

- `summary.md`, with the UTC check time, published origin, commit, pass/fail
  result, and the smoke suite's route/CDN/runtime diagnostics.
- `smoke-output.txt`, the same concise test output in plain text for searching.

Artifacts are retained for 90 days and are uploaded on both passing and failing
runs. This is intentionally separate from static validation and deployment.
The artifact does not contain credentials, visitor data, browser traces, or
page content beyond diagnostics printed by the smoke suite.
# Threat Model

## Project Overview

AskJamie is a public static marketing and documentation site for an AI persona and related portfolio artifacts. The production application is browser-served HTML, CSS, JavaScript, images, and generated search data with no backend runtime, database, authentication layer, or server-side form processing in scope.

## Assets

- **Site integrity** -- visitors must receive the intended HTML, CSS, JavaScript, and media without unauthorized modification. If client assets are tampered with, the attacker controls the entire user experience.
- **Visitor trust and brand content** -- the site presents brand, portfolio, and contact information. Unauthorized script execution or misleading navigation could damage user trust and brand reputation.
- **Published contact details and business context** -- the site intentionally exposes business contact information and public case-study content. The security goal is to avoid exposing anything beyond that intended public material.
- **Client-side search corpus** -- `assets/data/search-index.json` mirrors page content for browser search. It must not include non-public material or become an injection vehicle.
- **Edge security policy** -- `_headers` defines browser security controls such as HSTS and policy headers. These controls are part of the production security posture and should remain aligned with the shipped pages.

## Trust Boundaries

- **Browser to static host** -- all content crosses from the deployed static host to an untrusted browser. The client must be treated as hostile, and no security decision can rely on client state.
- **Public page content to shared browser JavaScript** -- static HTML and generated search-index data are consumed by `assets/js/app.js`. Anything rendered into the DOM from indexed content must be safely handled.
- **Site to third-party services** -- the site loads Google Fonts, Google Tag Manager, Google Analytics, and Mermaid from jsDelivr. These are explicit trust relationships because third-party content executes or influences rendering in the browser.
- **Production to dev-only repository content** -- scripts, templates, docs, agent tooling, and local task artifacts exist in the repository but are not part of the deployed static site. They should normally be ignored during production vulnerability assessment unless a public path exposes them.

## Scan Anchors

- **Production entry points:** `index.html`, `404.html`, `about/`, `contact/`, `legal/`, `search/`, `universe/`, `lens-system/`, `assets/js/app.js`, `assets/js/mermaid-init.js`, `assets/data/search-index.json`, `_headers`.
- **Highest-risk code areas:** `assets/js/app.js` search rendering and URL handling, `assets/js/mermaid-init.js`, inline scripts in page `<head>`, and third-party script/module imports.
- **Public surface:** all root and content-directory HTML pages plus browser-served assets under `assets/`.
- **Dev-only areas usually out of scope:** `scripts/`, `assets/templates/`, `assets/docs/`, `.agents/`, `.local/`, `docs/`, `node_modules/`.

## Threat Categories

### Tampering

The main tampering risk in this project is unauthorized modification of static assets or unsafe DOM updates in shared client-side code. The site must ensure that browser JavaScript does not treat URL parameters, generated search data, or page content as trusted executable markup unless it has been safely escaped or otherwise constrained.

Required guarantees:
- Shared client-side code MUST not execute or inject attacker-controlled markup into the DOM.
- Generated search data MUST be derived only from intended public pages and MUST remain non-executable when rendered.
- Browser navigation targets assembled from site data MUST stay within intended URL forms and MUST NOT permit script execution schemes.

### Information Disclosure

Because the site is public, most content is intentionally disclosed. The meaningful risk is accidental publication of non-public material through generated artifacts, docs, templates, or browser responses. The static search index is especially important because it aggregates page content into a single downloadable file.

Required guarantees:
- Only intentionally public pages MUST be included in `assets/data/search-index.json`.
- Dev-only content such as templates, local task files, docs, and agent tooling MUST NOT be linked into browser-served production assets.
- Error pages and page source MUST NOT expose secrets, credentials, or internal-only instructions.

### Spoofing

The project does not expose user authentication, but it does rely on third-party browser resources and outbound links. Visitors could be misled if third-party script origins or external navigation are not tightly controlled.

Required guarantees:
- Outbound links that open new tabs MUST prevent tabnabbing and preserve user context.
- Third-party script and module loading MUST be limited to explicitly approved origins.
- The deployed site MUST preserve canonical URLs and expected branding so users can distinguish first-party content from external destinations.

### Denial of Service

There is no server-side compute surface in production, so classic API or auth flooding threats are largely out of scope. The remaining concern is client-side performance degradation from expensive rendering or oversized browser-loaded assets.

Required guarantees:
- Search and diagram rendering MUST avoid attacker-controlled computational spikes through unbounded parsing or regex behavior on untrusted input.
- Public assets downloaded by every visitor SHOULD remain bounded in size and complexity so the browser experience remains available.

### Elevation of Privilege

There is no authenticated or role-separated production surface in the current deployment, so traditional privilege-escalation threats do not apply. The practical elevation risk here is a browser-side code execution bug that would let an attacker run arbitrary JavaScript in the site origin.

Required guarantees:
- No production code path should allow DOM XSS through query parameters, generated content, or external resource handling.
- CSP and related browser policies SHOULD continue to constrain script execution to intended sources, recognizing that inline scripts currently require a narrowly scoped exception.

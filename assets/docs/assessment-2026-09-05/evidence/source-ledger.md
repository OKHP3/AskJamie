# External guidance ledger

Retrieved September 5, 2026. Local source and runtime observations establish the defects; these primary references inform acceptance criteria and proposed changes. No external standard establishes conformance by itself.

| Source and publisher | Authority and exact use |
| --- | --- |
| [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), GitHub | Hosting provider guidance for validating, uploading and deploying a static Pages artifact. |
| [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use), GitHub | Action commit-SHA pinning and workflow permissions recommendations. |
| [Upload Artifact documentation](https://github.com/actions/upload-artifact), GitHub Actions | Hidden files excluded by default; supports investigation of `.well-known` transport. |
| [Node.js release table](https://nodejs.org/en/about/previous-releases), Node.js | Current v20 EOL status and supported LTS alternatives for QA tooling. |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/), W3C | Proposed accessibility review target, keyboard/reflow/contrast and focus requirements. |
| [Target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum), W3C | Minimum sizing and spacing exceptions; prevents an unsupported blanket 44px rule. |
| [frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors), MDN | Directive is unsupported in meta CSP; source `_headers` is not delivered-header proof. |
| [Web Vitals](https://web.dev/articles/vitals), Google Chrome team | Field thresholds and 75th-percentile framing; lab results are separate evidence. |
| [Structured data introduction](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data), Google Search Central | Structured data helps interpretation; markup alone does not promise display or ranking. |

The domain reports contain additional primary-source links beside the claims they support. Repository and live-site evidence is recorded in sibling JSON/text files. This ledger contains no private-source URLs.

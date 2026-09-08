# W01 Found-Ry content truth: corrected review

Date: 2026-09-08. Website baseline: `9e51286`. Found-Ry source checked during
closeout: `2537288`. Scope: issue #30, W01; not the differently numbered
32-task proposal.

The original worker note was recovered from Git snapshot `f8ff950`. It claimed
the AskJamie application was a public browser-only runtime using local storage.
That conclusion is rejected: it did not identify a supporting AskJamie runtime
source and conflicts with the separate application's authoritative files.
The original snapshot remains preserved as provenance; its proposed HTML must
not be applied to the website.

## Source check

`OKHP3/AskJamie-FoundRy` contains `workbench/server.py`, `store.py`, `service.py`,
and `docs/workbench.md`. Its `AGENTS.md` confirms intentionally public source,
a loopback Python/SQLite application and private draft state. It does not
establish a publicly hosted application. `found-ry/index.html` accurately
identifies the private local alpha, SQLite persistence and governed ZIP export.

Public source and private runtime data are distinct. A source repository link
is not inherently a disclosure of private drafts, and no such link should be
rejected solely because the application stores private data.

## Disposition

Review complete with correction. No runtime or availability rewrite is
justified. A link to the public workbench operating guide is a reasonable
visitor-journey proposal, recorded in W06. Replit deployment and operational
acceptance remain separate checks. Source presence alone is not a runtime test.

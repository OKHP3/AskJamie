---
name: AskJamie audit execution pattern
description: How accessibility audit reports are used on askjamie.bot — as an execution backlog, not a documentation artifact
---

## Rule
Every finding in `assets/docs/accessibility-audit-2026-08-16.md` is a task to execute. The report IS the to-do list. Do not treat it as complete until every line-item is shipped and validators confirm 0 issues.

**Why:** The user's explicit instruction: "that was not a report for the sake of a report — that is a report for the sake of execution."

## How to apply
After running an audit: immediately proceed to fix every finding in priority order (Critical → Serious → Moderate → Minor). Use the three validators as the acceptance gate before committing:
1. `python3 scripts/validate-site.py` — HTML structure
2. `python3 scripts/audit-site.py --quiet` — site-wide checks (must show 0 issues)
3. `node scripts/responsive-qa.mjs --static` — 208/208

Rebuild search index (`python3 scripts/build-search-index.py`) whenever any HTML page changes, or the audit script will flag a stale index.

## Outstanding items as of 2026-08-16
- Task #60: Keyboard focus ring live-browser verification (requires manual/Playwright testing)
- Task #62: aria-live region for search results — DONE (shipped 2026-08-16)
- Task #61: Reading level — DONE for legal/contact/coca-cola (FK now ≤10.5 on all three)
- M-01a: Jargon definitions on first body use across all 26 pages — not yet started
- Mi-01: height="auto" — DONE, replaced with explicit pixels sitewide

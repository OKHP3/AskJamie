# Delivery engineering PM ledger

Date: September 5, 2026. Repository: `OKHP3/AskJamie`.

## Scope

Owned packages: WP-05 required browser evidence and CSP diagnostics, WP-09
safe sibling-sync maintenance tooling, WP-10 supported CI runtime and supply
chain, WP-11 source/generated boundaries, and WP-14 hosted-governance and
measurement decision packet. Release-readiness checks also cover the first
batch and translation cleanup.

## Dispatch

The required first WP-09 worker was attempted with the AskJamie saved project,
isolated worktree, and GPT-5.6 Luna at medium reasoning. The app rejected the
valid project/worktree request three times before a worker ID was returned.
No worker was started, and no worker commit exists. Local work below is the
bounded fallback. This is a tooling dispatch blocker, not a package pass.

## Evidence and decisions

| Package | Current disposition | Evidence or next action |
| --- | --- | --- |
| WP-05 | Integrated, hosted/runtime acceptance open | Integrated as `22dafc5` from worker commit `d6f060a`; required browser launch and missing-CSP regressions now fail clearly. Full browser evidence remains 196/200. |
| WP-09 | Integrated, accepted locally | Integrated into `a7ca31f` from worker commits `c852738` and `bebdc1e`; 24 combined unittest cases pass, including the nine worker safety cases. No sibling write was run. |
| WP-10 | Integrated, clean-install evidence bounded | Integrated as `fb9346b` from worker commit `c6a61bb`; CI Node runtime moved to 24. Worker recorded 18 focused tests in a disposable environment. |
| WP-11 | Integrated, source boundary covered | Integrated as `fb9346b`; source collector tests explicitly exclude `dist-pages/` and `.scratch/`. |
| WP-14 | Decision packet only | `_headers` is not proven enforced by GitHub Pages. Settings, branch protection, analytics, and hosted measurement require owner approval and live readback. |
| Translation cleanup | Retained and inactive | No locale activation, translated route, locale index, or switcher markup. Catalog regeneration remains blocked by duplicate janitor packaging. |
| Ignored `.DS_Store` findings | Preserve and disposition | Eight ignored paths are hygiene findings. Do not delete without exact-path inventory and recovery decision. |

## Worker evidence ledger

WP-09 resolved thread ID is `01a074b7-3cd4-78a1-9719-023baa5f8650`; its client
dispatch was `client-new-thread:a9b9db39-ef94-4421-a6e2-bc8af25c8981`. It
produced isolated commits `c852738` and `bebdc1e` in
`/Users/okh/.codex/worktrees/843a/AskJamie`; the correction passed eight
focused safety regressions.
WP-05 resolved thread ID is `01a074b7-a97d-7330-91da-0d9acc5dd5d4`; its client
dispatch was `client-new-thread:c19133e4-1125-4101-93e3-fd271fc3af1b` and it
is working in `/Users/okh/.codex/worktrees/b6d3/AskJamie`. WP-10/WP-11
resolved thread ID is `01a074bc-4ae3-71d2-987b-d188fb53d61a`; its client
dispatch was `client-new-thread:5bdaede0-3083-4604-9cfb-35f89e64ce20`.
The parent Architect was notified of all dispatches and the WP-09 review gaps.

WP-05 commit: `d6f060a` in `/Users/okh/.codex/worktrees/b6d3/AskJamie`.
WP-10/WP-11 commit: `c6a61bb` in `/Users/okh/.codex/worktrees/9661/AskJamie`.

## WP-14 decision packet draft

Observed state: the recorded Pages configuration is workflow-based from
`main`, has `askjamie.bot`, custom 404, and HTTPS enforcement. The hosted
response evidence does not show CSP, anti-framing, or Permissions-Policy
response headers. `_headers` therefore remains a source intent, not proof of
GitHub Pages enforcement.

Owner decision required:

1. Accept GitHub Pages as the current host and document the response-header
   limitation, or select an approved edge host that can enforce the required
   headers.
2. If selecting an edge host, approve the exact provider, DNS change window,
   header policy, and rollback owner. Do not apply settings from this packet.
3. Approve whether privacy-safe aggregate measurement is wanted. If yes,
   authorize the specific analytics property and events, then review a
   redacted readback. No private analytics access was used here.

Readback after any approved external change: record the Pages/settings
response, deployed URL and commit, representative `curl -I` header results,
HTTPS/certificate state, and one rollback test or documented rollback
procedure. Rollback is to restore the prior hosting/DNS/header configuration,
verify the prior URL and certificate, and rerun the public HTTP probes. A
local code pass cannot substitute for this external readback.

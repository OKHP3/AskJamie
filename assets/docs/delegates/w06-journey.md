# W06 Found-Ry visitor journey: corrected review

Date: 2026-09-08. Website baseline: `9e51286`. Original worker commit:
`6949dd2`. Scope: issue #30, W06.

## Correction to the original handoff

The worker inspected the AskJamie website README and attributed its static
HTTP server command to the Found-Ry workbench. Those are separate repositories.
`python3 -m http.server 5000` previews the website; it does not launch the
capability workbench. The original "private repo" recommendation also conflicts
with the owner's public-source policy for AskJamie-FoundRy.

The correct source journey is the public AskJamie feature page, then
`OKHP3/AskJamie-FoundRy` and its `docs/workbench.md`. That application's README
specifies installing its requirements in a configured environment and running
`python3 -m workbench --port 8765`. Draft state remains local and private.
This review checked the source instructions, not an installation or a hosted
application. The Found-Ry integration owner owns executable startup acceptance.

## Visitor-facing result

The feature page's contact path and local-alpha availability wording are
consistent with the current application contract. Its links provide a
consultative journey, but there is no direct link to the public workbench
operating guide for someone who wants to inspect or run the source.

Proposed addition near the FAQ: "Want to inspect the source or run it locally?
Read the AskJamie Found-Ry operating guide. Your drafts stay on your computer."
The intended destination is
`https://github.com/OKHP3/AskJamie-FoundRy/blob/main/docs/workbench.md`.

This is a copy/navigation proposal, not an applied feature or a verified
external launch. No public hosted-app promise, private account locator or
incorrect website start command should be added. No message was sent through
the contact journey.

## Disposition

Review complete; initial source confusion corrected. Public source guidance
is suitable for a separately integrated page edit. No source HTML changed in
this task and no model-platform or installation acceptance is claimed.

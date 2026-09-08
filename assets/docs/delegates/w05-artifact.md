# W05 Found-Ry release integrity

Date: 2026-09-08

## Scope

This delegated pass stayed inside the approved AskJamie paths and did not
touch the owner's checkout or the separate Replit environment.

## Evidence

- Added a focused regression that builds a synthetic Found-Ry release surface,
  runs the shared cache-bust and CSP generators, and packages the isolated
  Pages artifact.
- The regression checks that the `found-ry/` route is preserved, the shared
  asset files are present, the fingerprinted `app.js`, `deferred-fonts.js`,
  and analytics import map survive into the packaged artifact, and the copied
  page keeps the generated CSP policy.

## Notes

- No runtime or shared script files were changed.
- The regression uses temporary fixture state only.

# Browser rerun evidence

Date: September 5, 2026. Commit under test: `f7888c0`. Working tree had the
PM WP-09 safety patch, PM ledger, and browser result output. Server: Python
`http.server` on `127.0.0.1:5188`, serving this worktree. The bundled Playwright
runtime from `load_workspace_dependencies` was used. External Google Fonts and
Google Tag Manager requests were blocked by the test environment and are
reported as warnings, not local asset failures.

## Result

Full browser responsive QA executed 200 route/viewport rows. Result: **FAIL,
196/200 passing**. The result file at `assets/audit/responsive-qa/results.json`
is disposable generated output and must not replace this dated record.

Failures recorded by the runner:

- `/lens-system/` at mobile-430, desktop-1024, and desktop-1280: a console
  `ERR_CONNECTION_TIMED_OUT` resource failure.
- `/lens-system/okhp3-brandguard/mathews-archery/` at tablet-768: two console
  `ERR_CONNECTION_TIMED_OUT` failures and a broken local image request for
  `assets/img/askjamie-title-cream-blue-backdrop-blue-gray-left-square-1024.png`.

The static mode remains a separate result: 200/200 source-lint rows. This
rerun does not establish hosted-header enforcement or clear the earlier
intermittent browser findings. WP-05 must capture the failed request URLs and
resource types, correlate the server log, and coordinate any asset/page repair
with the Experience PM before an affected-case rerun.

## Focused follow-up

After WP-05 added route/resource diagnostics, a focused browser probe used the
bundled Node `v24.19.0` and Playwright runtime against the four original
route/viewport combinations: `/lens-system/` at mobile-430, desktop-1024, and
desktop-1280, and the Mathews Archery case at tablet-768. The local server was
`127.0.0.1:5191`. All four rows had no non-blocked request failures, HTTP
errors, console errors, or broken eager images. The intentional third-party
block recorded two resources per row.

This is a current targeted result, not a replacement for the prior 196/200
full-run evidence. It shows that the original route/viewport combinations can
load cleanly in isolation. It does not identify the root cause of the earlier
Mathews image failure or clear it from the historical record.

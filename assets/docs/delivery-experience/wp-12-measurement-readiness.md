# WP-12 measurement and capture readiness

Date: 2026-09-05. Status: measurement and owner review pending.

## Current evidence

Historical mobile Lighthouse results recorded scores of 60, 71, 70, and 72
for homepage, BrandGuard, Universe, and Search, with LCP around 8.94, 7.80,
6.46, and 6.75 seconds. These are lab results from the dated assessment, not
current field measurements. Lighthouse is unavailable in this worktree.

The assessment measured the shared CSS at about 231 KB, shared JavaScript at
about 45 KB, search data at about 115 KB, and the 1024px navigation avatar at
756,775 bytes. These are file sizes, not transfer sizes or proof of a page-load
problem. Original artwork remains preserved.

## Controlled next run

Run homepage, Lens hub, BrandGuard detail, and Universe at 390px and 1280px
with a documented Chromium version, throttling, cache state, and at least three
samples. Record request bytes, image dimensions, font timing, LCP element,
layout shift, and Mermaid timing. Test a derived small navigation image only
after visual comparison and request measurement.

The capture script should wait for application readiness and image completion,
traverse lazy content, settle animations, and fail with resource diagnostics.
Existing visual references stay unchanged until each replacement is reviewed.

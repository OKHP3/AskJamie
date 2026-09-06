# WP-12 measurement and capture readiness

Date: 2026-09-05. Status: capture readiness implemented. Performance
measurement and any optimization remain partial.

## Current evidence

Historical mobile Lighthouse results recorded scores of 60, 71, 70, and 72
for homepage, BrandGuard, Universe, and Search, with LCP around 8.94, 7.80,
6.46, and 6.75 seconds. These are lab results from the dated assessment, not
current field measurements. The bundled workspace runtime was checked. It
supplies Playwright and Chromium, but not Lighthouse. An absent local
`node_modules` directory was not used as evidence for that limitation.

The assessment measured the shared CSS at about 231 KB, shared JavaScript at
about 45 KB, search data at about 115 KB, and the 1024px navigation avatar at
756,775 bytes. These are file sizes, not transfer sizes or proof of a page-load
problem. Original artwork remains preserved.

A bundled Chromium run against a dedicated local server captured same-origin
request evidence at 390px and 1280px. Homepage: 8 requests and 4 images,
279,727 and 305,052 bytes. Lens hub: 7 requests and 3 images, 308,629 and
279,727 bytes. BrandGuard detail: 7 requests and 3 images, 322,127 bytes at
both widths. Universe: 34 requests and 1 image, 535,297 and 825,572 bytes.
These are local response-body totals with external requests excluded, not
compressed transfer, LCP, or field performance measurements.

The integrated capture routine waits for page and image readiness, traverses
lazy content, settles animations, and writes a JSON readiness summary beside
temporary output. Its first bounded run captured homepage, Lens hub,
BrandGuard detail, and Universe at 390px and 1280px: 8 of 8 route/viewport
captures passed, with zero response errors and all sampled images loaded. It
did not replace a committed baseline.

## Bounded navigation-asset result

The navigation logo rendered at 40px while requesting the 1024px avatar, whose
natural-to-rendered width ratio was 25.6. A derived 80px PNG now serves only
the navigation logo, preserving the original for hero and metadata use. In
fresh browser contexts with same-origin requests only, no throttling,
device-scale factor 1, and the two capture viewports, each sampled route fell
by 748,203 local request bytes in the final paired local capture.

| Route | Before | After | Reduction |
| --- | ---: | ---: | ---: |
| Homepage | 1,165,430 | 417,227 | 748,203 |
| Lens hub | 1,771,302 | 1,023,099 | 748,203 |
| BrandGuard detail | 1,770,696 | 1,022,493 | 748,203 |
| Universe | 1,919,619 | 1,171,416 | 748,203 |

Two-times screenshot inspection at 390px and 1280px found the navigation logo
crisp and consistent.

This is not repeated sample-median evidence, compressed-transfer evidence, or
a user-performance result. It does not establish an LCP, CLS, field, or RUM
improvement. The capture report records `currentSrc`, natural and rendered
image dimensions, scale ratio, image loading state, resource bytes, fresh-cache
context, device scale, viewport, external-request blocking, and unthrottled
network conditions.

## Safety and remaining measurement work

The capture tests reject repository-root and populated committed-baseline
destinations unless an explicit replacement flag is supplied. They also
classify incomplete images, failed requests, and readiness or animation
timeouts as failures. Existing visual references remain unchanged until each
replacement is reviewed.

Remaining work is repeated route/viewport sampling, a supported Lighthouse
runtime for lab metrics, and field or RUM evidence. No current result should be
read as a production performance claim.

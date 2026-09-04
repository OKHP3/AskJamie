# Performance and Visual Baseline

**Captured:** 2026-08-22  
**Site:** AskJamie.bot  
**Method:** Lighthouse 12.8.2 against the local static server, using the
Playwright-managed Chromium binary. Visual references were captured with
Playwright at 1280px and 390px viewport widths.

This is a repeatable lab baseline, not field data. Network conditions, browser
versions, Google Fonts responses, analytics responses, and CPU load can change
the results. The report records a historical capture. The current site
intentionally uses Google Fonts and unconditional page-shell GA4.
The raw Lighthouse reports are in
`assets/audit/lighthouse-baseline-2026-08-22/`. The compact machine-readable
summary is `assets/audit/lighthouse-baseline-2026-08-22.json`.

## Lighthouse summary

| Page | Performance | Accessibility | Best practices | SEO | LCP | CLS | Max potential FID | TBT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Homepage `/` | 87 | 100 | 100 | 100 | 3.76 s | 0.034 | 16 ms | 0 ms |
| BrandGuard hub | 75 | 100 | 100 | 100 | 6.61 s | 0.003 | 89 ms | 40 ms |
| Universe `/universe/` | 44 | 100 | 100 | 100 | 6.16 s | 0.493 | 392 ms | 428 ms |
| Search `/search/` | 75 | 100 | 100 | 100 | 6.46 s | 0.069 | 49 ms | 0 ms |

Lighthouse 12 does not provide field INP in this lab report. The max potential
FID column is retained as the closest available lab interaction proxy. It
should not be presented as real visitor INP.

## Findings above the agreed thresholds

The task thresholds are performance below 90, CLS above 0.1, and LCP above
2.5 seconds.

### Performance below 90

All four pages are below 90 in this run. The Universe page is the most
significant outlier at 44, followed by the BrandGuard hub and Search at 75.
The homepage is closest to the target at 87.

### LCP above 2.5 seconds

All four pages exceed the 2.5 second target:

- **Homepage, 3.76 s:** Lighthouse identified the hero tagline
  `.hero-tagline` as the LCP element. Render delay accounted for about 88% of
  LCP in this run.
- **BrandGuard hub, 6.61 s:** Lighthouse identified the hero heading
  `#hero-title` as the LCP element. Render delay accounted for about 93% of
  LCP.
- **Universe, 6.16 s:** Lighthouse identified the hero tagline
  `.askjamie-hero-tagline` as the LCP element. Render delay accounted for about
  93% of LCP.
- **Search, 6.46 s:** Lighthouse identified `.search-hero-lede` as the LCP
  element. Render delay accounted for about 93% of LCP.

These are measurement findings only. Performance optimization is outside this
task. The large render-delay share is a useful target for a later performance
task, especially on pages with client-side initialization. Future comparisons
should record Google Fonts loading conditions rather than describe a self-hosted
font migration that is not part of the current site.

### CLS above 0.1

The Universe page recorded **0.493 CLS**, above the 0.1 threshold. Its
interactive Mermaid diagram is the highest-impact area to investigate because
the generated SVG replaces the initial diagram container after page load. The
other pages remained below the threshold, with Search at 0.069 as the next
highest value.

### Interaction and blocking observations

Universe also recorded the highest lab interaction cost: 392 ms max potential
FID and 428 ms TBT. BrandGuard recorded 89 ms max potential FID and 40 ms TBT.
The homepage and Search pages recorded 0 ms TBT in this run. These values are
lab observations, not a claim about field experience.

## Optimization verification

The Universe layout and Mermaid initialization were rechecked on 2026-08-22
with Lighthouse 12.8.2 against the same local static server and four routes.
The existing baseline remains the historical comparison point; it was not
overwritten.

| Page | Performance | LCP | CLS | Max potential FID | TBT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Homepage `/` | 73 (−14) | 9.68 s (+5.93 s) | 0.027 (−0.007) | 86 ms (+70 ms) | 36 ms (+36 ms) |
| BrandGuard hub | 75 (—) | 6.46 s (−0.15 s) | 0.004 (+0.001) | 158 ms (+69 ms) | 108 ms (+68 ms) |
| Universe `/universe/` | 88 (+44) | 2.63 s (−3.53 s) | 0.028 (−0.465) | 402 ms (+10 ms) | 296 ms (−132 ms) |
| Search `/search/` | 75 (—) | 6.46 s (−0.001 s) | 0.069 (−0.0001) | 49 ms (—) | 0 ms (—) |

The Universe result confirms that reserving the generated diagram's measured
space prevents the replacement from shifting the hero: CLS moved below the
0.1 threshold, while performance and LCP improved substantially. The
homepage and BrandGuard variance reinforces that these are lab samples, not
field guarantees; the Universe change is the clear signal because its CLS
improvement is much larger than the other pages' movement.

## Targeted performance pass

A follow-up Lighthouse 12.8.2 desktop run on 2026-08-22 verified the
above-the-fold and image-delivery changes against the same four routes:

| Page | Performance | LCP | Total payload |
| --- | ---: | ---: | ---: |
| Homepage `/` | 95 | 1.2 s | 1,240 KiB |
| BrandGuard hub | 99 | 0.8 s | — |
| Universe `/universe/` | 96 | 1.1 s | — |
| Search `/search/` | 97 | 1.2 s | — |

The homepage hero now paints before `app.js` initialization, its avatar uses
a right-sized WebP source with a PNG fallback, and the milestone card uses a
right-sized WebP source. The audited route scripts are deferred because they
do not provide parser-blocking behavior. These are desktop lab results;
mobile Lighthouse scores remain sensitive to device and browser timing and are
not represented as passing thresholds by this record.

## Repeatable route check

The current comparison run was captured on **2026-08-24** with Lighthouse
12.8.2. Start the configured static server, then run:

```bash
node scripts/lighthouse-routes.mjs --date=2026-08-24
```

The runner discovers the committed Playwright Chromium binary, tests `/`,
`/lens-system/okhp3-brandguard/`, `/universe/`, and `/search/` with the desktop
preset, writes raw reports to the dated directory under `assets/audit/`, and
compares each result with `lighthouse-baseline-2026-08-22.json`.

| Page | Before performance | After performance | Change | Before LCP | After LCP | CLS after |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Homepage `/` | 87 | 97 | +10 | 3.76 s | 1.33 s | 0.025 |
| BrandGuard hub | 75 | 97 | +22 | 6.61 s | 1.29 s | 0.001 |
| Universe `/universe/` | 44 | 96 | +52 | 6.16 s | 1.29 s | 0.013 |
| Search `/search/` | 75 | 97 | +22 | 6.46 s | 1.25 s | 0.055 |

The homepage, BrandGuard, and Search routes now clear the 90 performance target.
Universe remains below target because Mermaid still contributes blocking work,
but its layout shift remains below the 0.1 threshold. The route check's raw
Lighthouse accessibility score varied for two AskJamie routes because this
fresh browser session evaluated the active-navigation contrast and injected
search control labeling; the repository's canonical structural and accessibility
checks remained clean (`validate-site.py` and `audit-site.py`).

## Mobile Lighthouse comparison

On **2026-08-25**, the same four routes were measured with Lighthouse 12.8.2
using its `--form-factor=mobile` configuration against the local static server.
Raw reports and the compact summary are in
`assets/audit/lighthouse-2026-08-25-mobile/`. These are lab measurements under
emulated mobile conditions, not field data.

| Page | Performance | LCP | CLS | TBT |
| --- | ---: | ---: | ---: | ---: |
| Homepage `/` | 87 | 3.63 s | 0.002 | 55 ms |
| BrandGuard hub | 72 | 6.91 s | 0.003 | 0 ms |
| Universe `/universe/` | 58 | 6.46 s | 0.045 | 562 ms |
| Search `/search/` | 95 | 2.42 s | 0.026 | 0 ms |

### Mobile-only findings

- **Universe is the mobile outlier:** performance is 58, LCP is 6.46 s, and
  TBT is 562 ms. CLS remains below the 0.1 threshold, so the measured issue is
  render and blocking cost rather than a new layout-shift regression.
- **BrandGuard is slower than the desktop comparison:** performance is 72 and
  LCP is 6.91 s. Its CLS and TBT remain low in this sample.
- **Search is not a mobile regression in this run:** it scored 95 with LCP
  below 2.5 s. The homepage remained near its desktop score at 87.
- No visual identity changes were made in response to this measurement.

The mobile run is repeatable with:

```bash
node scripts/lighthouse-routes.mjs --preset=mobile --date=2026-08-25
```

The runner keeps mobile reports in a `-mobile` dated directory and preserves
the existing desktop command and output path.

## Mobile performance remediation verification

The remediation was measured on **2026-09-04** with Lighthouse 12.8.2 against
the same local static server, routes, and mobile preset as the 2026-08-25
baseline. Lighthouse used its Moto G Power emulation at 412×823 CSS pixels,
4× CPU slowdown, 150 ms simulated RTT, and approximately 1.5 Mbps simulated
download throughput. The before sample is
`assets/audit/lighthouse-2026-09-04-mobile/`; the final after sample is
`assets/audit/lighthouse-2026-09-04-final4-mobile/`. A second exact-code
verification is retained in `assets/audit/lighthouse-2026-09-04-final3-mobile/`.

| Page | Before performance | After performance | Before LCP | After LCP | Before TBT | After TBT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Homepage `/` | 83 | 60 | 4.05 s | 8.94 s | 88 ms | 311 ms |
| BrandGuard hub | 64 | 71 | 8.55 s | 7.80 s | 237 ms | 129 ms |
| Universe `/universe/` | 54 | 70 | 7.81 s | 6.46 s | 679 ms | 154 ms |
| Search `/search/` | 72 | 72 | 6.30 s | 6.75 s | 148 ms | 124 ms |

The homepage and Search markup were not changed by this remediation. Their
mobile movement is therefore treated as lab variance, not a product
regression: the same route runner produced materially different samples on
adjacent runs while external Google Fonts and analytics requests were in
flight. Across the two final exact-code samples, BrandGuard ranged from
6.91–7.80 s LCP and 127–129 ms TBT, while Universe ranged from 6.45–6.46 s
LCP and 154–167 ms TBT. The stable signal is reduced blocking work, especially
from the Universe Mermaid bundle. BrandGuard and Universe mobile LCP remain
budget exceptions in this environment and are not claimed as field
performance.

The final desktop comparison used the same four routes and desktop preset:

| Page | Performance | LCP | TBT |
| --- | ---: | ---: | ---: |
| Homepage `/` | 97 | 1.09 s | 0 ms |
| BrandGuard hub | 97 | 1.25 s | 0 ms |
| Universe `/universe/` | 96 | 1.33 s | 34 ms |
| Search `/search/` | 97 | 0.88 s | 0 ms |

The implementation keeps the existing visual and semantic behavior while
reducing first-view work:

- Universe dynamically imports Mermaid only when its diagram approaches the
  viewport on mobile; the source text and existing `<noscript>` explanation
  remain available as fallback content, and generated links retain their
  accessibility hardening.
- BrandGuard and Universe prefetch Google Fonts without making the stylesheet
  render-blocking, then enable the branded stylesheet after page load. The
  bounded `display=fallback` policy prevents a late webfont swap from
  redefining mobile LCP while retaining the branded face on faster visits.
- BrandGuard uses `content-visibility: auto` for below-the-fold portfolio
  sections with an intrinsic size reservation, reducing initial mobile layout
  and paint work without removing content.

The Mermaid visual references were not overwritten because these are loading
and scheduling changes, not intentional visual redesign. The capture helper
now scrolls the diagram into view before waiting for its SVG, matching the
new mobile lazy-render condition. All Lighthouse numbers above are lab data;
they remain sensitive to browser version, simulated throttling, Google Fonts
responses, analytics responses, and CPU contention, and should not be
presented as real-user or field metrics.

## Visual reference set

The committed reference images are in `assets/audit/visual-baseline/`:

- `homepage-full-desktop-1280.png`
- `homepage-full-mobile-390.png`
- `homepage-hero-desktop-1280.png`
- `homepage-hero-mobile-390.png`
- `brandguard-card-desktop-1280.png`
- `brandguard-card-mobile-390.png`
- `universe-diagram-desktop-1280.png`
- `universe-diagram-mobile-390.png`

The Universe references were refreshed after this intentional layout change.
The diagram remains fully visible at both reference widths while the reserved
slot prevents a post-load page shift.

The historical capture used the then-current analytics-denial state and the
light theme so that the reference images did not depend on a visitor decision
or a system color preference. The denial state is no longer part of the
runtime policy. These visual references are not analytics evidence.

## How to refresh

Start the local server, then run:

```bash
node scripts/capture-visual-baseline.mjs
```

For a new dated Lighthouse run, use the same four routes and write the raw
reports to a new dated directory under `assets/audit/`. Update the compact JSON
summary and this report only after reviewing the screenshots and raw metrics.
Do not overwrite the committed references for an intentional visual change
without recording why the change is expected.
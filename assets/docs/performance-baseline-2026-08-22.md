# Performance and Visual Baseline

**Captured:** 2026-08-22  
**Site:** AskJamie.bot  
**Method:** Lighthouse 12.8.2 against the local static server, using the
Playwright-managed Chromium binary. Visual references were captured with
Playwright at 1280px and 390px viewport widths.

This is a repeatable lab baseline, not field data. Network conditions, browser
versions, consent state, CDN responses, and CPU load can change the results.
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
task, especially on pages with client-side initialization. The later typography
migration removes the former external-font variable from future comparisons.

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

The capture used denied analytics consent and the light theme so that the
reference images do not depend on a visitor decision or a system color
preference.

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
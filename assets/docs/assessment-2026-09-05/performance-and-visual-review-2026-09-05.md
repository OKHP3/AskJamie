# Performance and visual review

Date: September 5, 2026. Source baseline `fd1ea19` plus the local assessment repair patch.

## Intentional visual changes

Footer navigation and body text now use the AskJamie theme tokens with sufficient selector specificity. The tested minimum normal-text contrast is 6.24:1 in light mode and 6.75:1 in dark mode. The paper background, teal identity, typography and artwork remain intact.

Homepage sections are visible without JavaScript or when the shared app fails to load. Animation is enabled only after its controller initializes; reduced motion removes the hidden state. Search copy identifies AskJamie and suggests indexed AskJamie subjects. The shared search's remaining orange accents are inherited styling and belong in the next brand-consistency review.

Reviewed focused captures:

- [Light footer, desktop](evidence/screenshots/after-footer-1280.png)
- [Light footer, mobile](evidence/screenshots/after-footer-390.png)
- [AskJamie search, mobile](evidence/screenshots/after-search-390.png)
- [AskJamie search, desktop](evidence/screenshots/after-search-1280.png)
- [Visible content without JavaScript](evidence/screenshots/after-nojs-desktop.png)

Before-state captures and computed-style evidence are in the same evidence directory. Browser interaction and contrast results are in [experience-qa-final.json](evidence/experience-qa-final.json).

## Repository capture routine

Executed `scripts/capture-visual-baseline.mjs` against the local server with the installed Playwright runtime and an overridden `OUTPUT_DIR`. The final serial capture used port 5187 and `/tmp/askjamie-assessment/reviewed-visual-baseline`. Homepage, first BrandGuard card and Universe images at 1280px and 390px were visually inspected.

The capture routine can record partly transparent scroll-reveal states and does not traverse the entire page to load all lazy content. Earlier captures under concurrent browser load also missed images. Committed baseline references were therefore preserved. A subsequent capture task should wait for image decoding and reveal completion, record viewport and color/motion preferences explicitly, and ensure fixed headers do not cover element captures. It should remain separate from the actual visual design.

Inspection confirmed that the first BrandGuard card is an inline anchor with block descendants and three client rectangles at 390px. This produces fragmented card borders and padding. A scoped next task should use an appropriate block/flex link-card layout, preserve semantic links and all 13 destinations, and test keyboard focus plus mobile/desktop appearance. The current patch does not change that card geometry.

## Performance evidence

No fresh Lighthouse run was performed because Lighthouse is unavailable in the current local runtime. The [September 4 mobile summary](../../audit/lighthouse-2026-09-04-final4-mobile/summary.json) remains historical: performance scores 60/71/70/72 and recorded LCP 8.94/7.80/6.46/6.75 seconds for homepage/BrandGuard/Universe/Search.

Packaging now excludes approximately 15.5 MB of incidental/source-only files while preserving originals. This is not proof of faster visitor loads: unrequested artwork is not on the critical network path. No traffic, conversion, field Core Web Vitals or current performance-score improvement is claimed.

Next performance task: obtain repeated current mobile traces with controlled cache/throttling, identify the actual LCP element and critical font/CSS/image requests, then make the smallest measured change. The [delivery plan](delivery-plan.md) owns that sequence.

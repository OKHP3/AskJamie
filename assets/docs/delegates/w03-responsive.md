# W03 Found-Ry responsive acceptance

Date: 2026-09-08. Source baseline: `9e51286`, with documentation and test-only
integration changes. Scope: issue #30, W03. No original W03 artifact was found
in the inspected local branches, worktrees or snapshot history, so the
integration owner performed a new bounded browser check.

## Method

Headless Chromium from the bundled Playwright runtime; loopback HTTP preview;
900px viewport height; reduced-motion enabled; third-party requests blocked.
The script opened `/found-ry/`, checked document width and landmarks, exercised
Tab and Enter to the skip link, then set the root font size to 200% and captured
full-page screenshots. Root and body computed font sizes both became 32px.
This is a text enlargement stress check, not proof of native browser zoom or
human assistive-technology behavior. The retained JSON records exact values.

## Results

| Width | Normal document width | Enlarged-text document width | Skip link focuses main | Page exceptions |
| --- | --- | --- | --- | --- |
| 320 | 320 | 400 | Yes | 0 |
| 390 | 390 | 400 | Yes | 0 |
| 768 | 768 | 768 | Yes | 0 |
| 1280 | 1280 | 1384 | Yes | 0 |

Normal-width acceptance passes for the sampled route. Enlarged text reveals
horizontal overflow in three of four cases. This remains an open reflow
finding, not a passing responsive certification. Diagnose the overflowing
components and coordinate the shared CSS owner before a repair. No visual
baseline was replaced and no shared stylesheet was edited by this review.

The recovered W02 keyboard note is consistent with this new limited skip-link
check. Neither establishes spoken VoiceOver/NVDA results.

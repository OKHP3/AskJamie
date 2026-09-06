# Universe map release validation, September 6, 2026

The universe page now uses a compact brand overview and six bounded detail
maps for 25 indexed pages. Diagrams render lazily on expansion. No new runtime
dependency or third-party script was added. The portable Python package remains
version 0.1.0 and unchanged from Skillz.

Local validation passed: structural HTML, link inventory, canonical audit,
asset fingerprints, map/index freshness, 11 generator regression cases,
36 Python tests excluding three POSIX process fixtures, and all 200 responsive
browser checks. The three POSIX fixtures require the Linux CI runner; Windows
shell adapters did not execute them reliably. No local pass is claimed for them.

The dedicated browser test verifies all six maps at 390px and 1280px, both
color schemes, node/link counts, full indexed URL coverage, expandable keyboard
controls, and ordinary navigation without JavaScript. Phone diagrams scroll
within their container rather than shrinking their labels to unreadable sizes.
Visual baseline changes are limited to the intentional universe overview.

The release workflow also runs the dedicated universe browser checks. Publishing
and hosted acceptance are verified separately after the pull request merges.
No Lighthouse performance score or human screen-reader result is claimed.

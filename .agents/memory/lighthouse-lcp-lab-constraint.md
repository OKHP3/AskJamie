---
name: Lighthouse LCP lab constraint
description: How to interpret the BrandGuard mobile Lighthouse gap between observed paint and emulated LCP.
---

Mobile Lighthouse can report a delayed LCP even when the same run has zero blocking time, no LCP invalidation, and much earlier observed paint timestamps. Treat the emulated LCP as a lab measurement, keep controlled third-party-isolated and normal samples separate, and do not use it as field evidence.

**Why:** The BrandGuard mobile run showed a 1.561-second gap between Speed Index and emulated LCP while local paint observers recorded the hero candidate at roughly 100ms.

**How to apply:** When this pattern repeats, preserve the raw report and observed metrics, investigate page geometry separately, and require owner approval before changing a performance budget.
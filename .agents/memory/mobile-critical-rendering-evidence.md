---
name: Mobile critical-rendering evidence
description: Durable guidance for separating critical CSS improvements from Lighthouse variance on mobile hero routes.
---

Mobile critical-rendering work should keep the first viewport paintable with a small local stylesheet and system-font fallback, while deferring large shared theme/font work without hiding or rewriting content. Treat controlled third-party-isolated Lighthouse samples and normal samples as separate lab evidence; neither is field evidence.

**Why:** Large late cascades can dominate hero render delay, while repeated Lighthouse runs on the same static route can vary substantially under CPU/network emulation. Reporting one favorable run as a budget pass is misleading.

**How to apply:** Keep the critical stylesheet in the cache-busting asset registry, preserve intrinsic image dimensions and accessible source content, compare controlled and normal runs in separate dated reports, and only claim a budget pass when repeat evidence supports it.
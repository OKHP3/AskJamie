---
name: Flesch-Kincaid scoring for HTML pages
description: How to get accurate FK scores from HTML — treating list items and block elements as sentence boundaries
---

## Rule
When computing FK grade-level scores from HTML, treat closing block-level tags (`</li>`, `</p>`, `</h1>`–`</h6>`, `</div>`, `</section>`, `</article>`) as sentence terminators before stripping tags. Otherwise list items and bullet points concatenate into artificially long "sentences" that inflate the score.

Also strip `<pre>`, `<code>`, `<script>`, `<style>`, `<nav>`, `<footer>`, and `<head>` blocks before scoring — technical content, navigation, and boilerplate are not body copy.

**Why:** Bullet lists like the coca-cola "5-Ring persona mapping" were being read as a 116-word single sentence (2.12 syllables/word), pushing FK to 12.9 when the actual prose was ~8–9 grade level.

## Correct approach (Python)
```python
html = re.sub(r'<(script|style|pre|code|head|nav|footer)[^>]*>.*?</\1>', '', html, flags=re.DOTALL|re.IGNORECASE)
html = re.sub(r'</(li|p|h[1-6]|div|section|article|td|th)>', '. ', html, flags=re.IGNORECASE)
html = re.sub(r'<[^>]+>', ' ', html)
```

## Verified results (2026-08-16)
After prose simplification + correct scoring:
- legal/ FK 12.3 → 9.5 ✓
- contact/ FK 11.7 → 7.8 ✓
- coca-cola/ FK 12.0 → 8.6 ✓

## Audit baselines are not reproducible (2026-08-17)
The accessibility audit doc claims its FK script is "embedded in Section 4, S-02" — it is not; no FK script exists anywhere in the repo. The audit's per-page FK numbers (e.g. legal 12.3) could not be reproduced by any extraction variant (with/without block boundaries, main-only or whole body). When a task cites those baselines, verify against your own implementation and target the threshold under the strictest variant rather than chasing exact baseline matches.

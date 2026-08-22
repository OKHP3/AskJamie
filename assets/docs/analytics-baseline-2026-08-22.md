# Visitor Analytics Baseline and Inquiry Funnel

**Review date:** 2026-08-22  
**Property requested:** GA4 `G-MT9Y10YY0G`  
**Site:** AskJamie.bot

## Executive finding

The GA4 property could not be reviewed from this workspace. No Google Analytics
connection or dashboard export is available through the configured Replit
integrations, and no authenticated GA4 data was supplied. The figures below are
therefore recorded as **unknown**, not estimated. This is an evidence gap, not
evidence of zero visitors or zero conversions.

The highest-impact improvement is to establish a recurring GA4 export or
read-only connection and review the newly defined events alongside the existing
page-view data. Until that happens, the site can measure intent, but cannot
demonstrate whether visitors complete the journey.

## Access review

On 2026-08-22, the Replit integration catalog was searched for Google Analytics
and GA4. No matching connector, authorized connection, or catalog setup option
was available. The workspace has no supplied GA4 export for property
`G-MT9Y10YY0G`. No GA4 key event could be configured from this environment.

The public site contains the consent-gated GA4 implementation and the
`search_open`, `gpt_click`, and `inquiry_click` event definitions, but those
facts do not provide historical visitor counts.

## GA4 baseline

| Requested measure | Baseline for this review | Evidence/status |
| --- | ---: | --- |
| Top 10 pages by sessions | Not available | GA4 property access/export unavailable |
| Average engagement time | Not available | GA4 property access/export unavailable |
| Search overlay usage rate | Not available | No `search_open` event existed before this review |
| Most-clicked external links / GPT links | Not available | No historical `gpt_click` event existed before this review |
| Contact page visits | Not available | GA4 property access/export unavailable |
| Contact entry/exit rate | Not available | Requires GA4 landing-page and page-path report |

### Measurement limitation

GA4 is consent-gated in `assets/js/app.js`. Visitors who decline analytics are
not sent to GA4, so any future report must describe its denominator as
**consented sessions**, not all site visits. This is intentional privacy
behavior; it is not a defect to be bypassed.

### Resulting evidence boundary

The highest-volume funnel exit cannot be identified from the available
evidence. Page views, consented sessions, event counts, and drop-off rates all
remain unknown. The only evidence-backed improvement at this time is to obtain
a read-only GA4 export or authorized connection, then review a stated date
range using consented sessions.

## Inquiry funnel map

The intended visitor path is:

1. **Homepage** — visitor understands AskJamie and chooses a next step.
2. **Lens System** — visitor compares the four lenses and sees which are live
   or in development.
3. **BrandGuard case study** — visitor reads a concrete example and can follow
   the published GPT link.
4. **Contact action** — visitor selects an inquiry path and opens an email with
   a useful subject line.

The main observable exits before this review were page navigation without a
conversion signal, external GPT navigation without a named event, and mailto
navigation without a named event. GA4 data is needed to quantify each
drop-off. The new events below make those points measurable for future
consented sessions.

## Conversion definition

### Primary conversion: `gpt_click`

`gpt_click` fires when a visitor activates a published ChatGPT GPT link
(`https://chatgpt.com/g/...`). Parameters include the destination, link text,
source page path, and the page title/lens context. This is the highest-signal
currently available conversion because it represents a visitor moving from
explanation to trying a live capability.

### Secondary conversion: `inquiry_click`

`inquiry_click` fires when a visitor activates a `mailto:` inquiry link.
Parameters include the email destination, source page path, link text, and an
inquiry type derived from the mailto subject or nearby heading. A click is an
**initiated inquiry**, not proof that an email was sent or received; static
websites cannot verify the completion of a visitor's mail client action.

Both events are sent only through the existing consent-gated `gtag` loader.
They do not load analytics or create cookies after a visitor declines consent.
Mark `gpt_click` as a GA4 key event after enough consented traffic exists to
make that designation meaningful. `inquiry_click` should remain a secondary
diagnostic event unless email completion can be measured elsewhere.

The supporting `search_open` event records overlay use and includes the source
page plus whether the visitor opened it with the button or keyboard. It supports
the requested search-usage calculation:
`search_open` events divided by consented sessions (or consented users, kept
consistent across the report).

## Contact-path update

The contact page now gives one subject-line choice for each supported path:
BrandGuard demo, Enterprise Sleuth inquiry, AJ01, AJ02, architecture, and
general collaboration/question. The main email link opens with a general
inquiry subject while the visible guidance lets the visitor choose a more
specific tag.

## Recommended next review

Run a GA4 report for a clearly stated date range using consented sessions only.
Export page sessions, average engagement time, landing-page exits, and counts
for `gpt_click` and `inquiry_click`. Compare the three highest-entry pages
against the funnel above and prioritize the first step with a substantial
consented-session drop and no downstream action.
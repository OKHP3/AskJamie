# AskJamie experience, content, and accessibility assessment

Assessment date: September 5, 2026. Source baseline: `fd1ea19` after the Architect synchronized the clone. Reviewer: Experience Worker, reporting through the Project Manager to the Project Architect. Scope: AskJamie only.

The site has a coherent visual identity, real content depth, understandable prototype disclosures on most BrandGuard detail pages, and a useful new explanation of the Lens System. Its largest improvement opportunity is consistency between that honest explanation and the older experience: search identifies the wrong brand, some interaction promises are unimplemented, and several commercial or affiliation claims run beyond the evidence linked from the page. Keep the paper treatment, owner voice, static architecture, Google Fonts, and documented analytics decision. Fix these seams before a redesign.

## Method and proof boundary

All **27 source HTML pages** were inventoried and reviewed for main content, headings, journeys, links, image markup, and structured metadata. This is 25 sitemap routes plus the two utility pages. Nine templates were separately inventoried; representative homepage, interior, lens-detail, and case-study templates were inspected for inherited behavior. Generated `dist-pages/` and concurrent `.scratch/` directories are not independent source pages. Shared `app.js`, relevant `theme.css` rules, brand analytics, and Universe initialization references were inspected.

`experience-source-ledger.json` records source paragraph, heading, and list text with source line numbers for every page. It is a review ledger, not an HTML archive: scripts, SVG, code samples, image markup, and some nested text are outside its extraction contract. File references below refer to the baseline, before the authorized search remediation. The Architect owns baseline validators and browser observations; its browser report supersedes the runtime hypotheses below. This worker did not run live GPT conversations, use Notion authentication, test a purchase, send email, or validate personal credentials. A page claiming a capability is evidence of the claim, not of model performance.

Evidence labels: **Confirmed** means directly observed source or measured file data; **Inferred** means the practical implication needs runtime or owner evidence; **Proposal** is a suggested improvement; **Unknown** is untested or externally dependent. Severity: **High** means a core journey or trust boundary is impaired; **Medium** means material friction or inconsistent accessibility; **Low** means localized polish or maintainability. Severity is not a legal or security verdict.

## Findings and acceptance criteria

### EXP-01. Search introduces another brand

**Confirmed, Medium.** `assets/js/app.js:720` names the modal Search OverKill Hill; `:728` introduces the Forge; `:750` describes Council archives; `:751-757` suggests ROY, Council, and Manifesto. `assets/js/askjamie-analytics.js:1` is only a tracking module and does not replace these strings. This is sitewide because all pages load the shared script. It makes the user doubt search scope and sends them toward weak or irrelevant queries.

**Recommendation:** use a synchronous AskJamie search-copy configuration selected before overlay construction. Keep other brand defaults intact. Use actual AskJamie concepts and indexed pages for suggestions. **Acceptance:** open search on homepage, contact, and a BrandGuard page; accessible name, placeholder, empty state, and no-results help all identify AskJamie; each suggestion returns useful AskJamie results; a fixture without the AskJamie body class preserves the existing default copy. This is in the Architect-authorized implementation batch.

### EXP-02. Dedicated search advertises an unimplemented Enter contract

**Confirmed source defect, Medium.** `search/index.html:123-126` promises Escape to clear and Enter to follow the top result. `assets/js/app.js:1089-1100` initializes and listens for input, but contains no dedicated-page key handler; the handler at `:875-885` belongs to the separate overlay. Native Escape behavior on `type=search` differs by browser and does not establish the advertised cross-browser contract. Enter on the dedicated field has no matching navigation implementation.

**Recommendation:** add AskJamie-only handlers for the advertised actions, preserving composing text and modifier shortcuts. **Acceptance:** Enter with matching results opens the first result; Enter with zero results does nothing; Escape clears query/results, updates the URL, retains the current category, and keeps focus in the field; IME confirmation and modified Enter do not navigate unexpectedly. This is in the authorized implementation batch.

### EXP-03. Dedicated search list semantics do not match its children

**Confirmed source structure, Medium.** `search/index.html:149` declares `role="list"`. `assets/js/app.js:1034-1038` inserts direct anchor children, without `listitem` containers. The overlay at `:859-863` does provide `listitem`. Assistive technology may receive an incomplete list relationship on the dedicated page.

**Recommendation:** use a native list with list items, or match the overlay's explicit list-item structure. Loading, empty, and error states should sit outside the list or use an appropriate alternative container. **Acceptance:** populated search passes the list-ownership rule in an accessibility scan; manual screen-reader review announces the result list and permits links to be navigated individually. Do not treat a static HTML scan before results arrive as coverage of this defect.

### EXP-04. Skip links are intercepted as decorative scrolling

**Confirmed source and Architect browser observation, High.** `assets/js/app.js:395-404` intercepts every local hash link, including the skip link, cancels the browser's default behavior, and calls `scrollIntoView` without moving focus or preserving the fragment. For example, `index.html:89` provides the skip link and `index.html:128` is the main destination. The Architect activated the live skip link and observed focus remain on the skip link with an empty URL fragment. This confirms the keyboard defect.

**Recommendation:** preserve native fragment navigation or explicitly move focus to an appropriate target without adding it to the regular tab sequence. Honor reduced motion in the actual JavaScript scroll options. **Acceptance:** on desktop and mobile, activating Skip to content places sequential navigation in main, the next Tab reaches main content rather than header controls, and reduced-motion mode has no smooth animation. See [W3C bypass blocks](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html).

### EXP-05. Desktop content visibility depends on successful JavaScript

**Confirmed source and Architect browser observation, High.** `assets/css/theme.css:1160-1168` hides unrevealed sections by default. `:7578` restores only hero visibility; `:3240-3249` restores smaller widths; `:3462-3478` restores reduced-motion rendering. At a normal-motion desktop width above 1024px, a blocked or failed `app.js` leaves sections such as `index.html:183`, `:221`, `:231`, and `:275` transparent. The Architect confirmed four transparent below-the-fold sections on the live homepage at 1280px with JavaScript disabled and explicit normal motion. Static page delivery should still expose its main content when enhancement fails.

**Recommendation:** make content visible by default and opt into animation only after its observer is ready, with a fail-open behavior. **Acceptance:** JS-disabled and script-blocked desktop renders expose every section and actionable link; ordinary JS-enabled scroll reveal still works; narrow and reduced-motion cases remain visible. This does not require a framework or dependency.

### EXP-06. Shared BFS promotion contradicts the independent-prototype disclosure

**Confirmed copy mismatch, High.** The repeated banner states that Builders FirstSource is protecting its claim using a BrandGuard GPT, for example `search/index.html:111-115` and `contact/index.html:142-146`. The BFS page explicitly states personal R&D, no official corporate product, and no official-system connection at `lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/index.html:243`. The new explanation reinforces no endorsement or partnership at `how-askjamie-works/index.html:181`.

**Recommendation:** make the banner describe Jamie's public-information demonstration about BFS. Preserve the topic and owner's enthusiasm while removing implied corporate adoption. **Acceptance:** every banner and homepage teaser accurately identifies the author and prototype boundary; its wording agrees with the destination disclosure. No claim about whether BFS has other AI programs is made.

### EXP-07. Older product claims outpace the linked evidence

**Confirmed claims, Unknown substantiation, High.** `about/index.html:201-205` says specialized modules are enterprise-ready. `lens-system/enterprise-sleuth/index.html:261-264` calls the method battle-tested and cites tens of thousands of prompt iterations. `lens-system/professional-portfolio/index.html:455` compares price with a month of junior salary, without a price on that page. `lens-system/resume-representative/index.html:175-185` promises an always-on career representative ready for every recruiter. The newer boundary at `how-askjamie-works/index.html:198-207` makes a narrower and more credible distinction between live pages, demonstrations, and external availability.

**Recommendation:** build a claim register and either link to public evidence or replace the specific unsupported readiness, count, price, and guarantee claims with descriptions of design intent. This is not a blanket rewrite of personality. **Acceptance:** each retained quantitative or production claim has an owner-approved source/date and explicit scope; samples remain labeled demonstrations; no statement equates a published GPT link with a verified enterprise deployment.

### EXP-08. A kit is presented as available without a clear acquisition path

**Confirmed journey structure, Medium.** `lens-system/professional-portfolio/index.html:343-382` describes an offered kit and `:537` says to grab it. `lens-system/resume-representative/index.html:295-337` lists kit deliverables. Final actions open a public GPT or contact fragment rather than a kit, pricing, or availability page. The experience may leave a motivated visitor unsure whether the kit exists for immediate purchase, is bespoke, or is still being developed.

**Recommendation:** state owner-confirmed availability and the exact next step next to the offer. If inquiry-only, say how to request the kit and what information is useful; do not invent a price or checkout. **Acceptance:** from either lens page, a visitor can identify the available deliverable, whether it is immediate or inquiry-based, and a single relevant next action.

### EXP-09. Public artifact sections contain private-workspace locators

**Confirmed links, Unknown anonymous access, Medium.** Ten BrandGuard detail pages contain Notion specification links. Examples: `brooks-running/index.html:595`, `coca-cola/index.html:615`, `costco/index.html:610`, `discount-tire/index.html:564`, `dollar-general/index.html:577`, `hershey/index.html:604`, `lego/index.html:242`, `lvmh/index.html:521`, `ping/index.html:638`, and `starbucks/index.html:597`, all under `lens-system/okhp3-brandguard/`. Some also expose ChatGPT project-workspace links, for example Discount Tire `:558`. These are presented alongside public artifacts; successful authenticated owner access would not prove public accessibility. Exact private locators are deliberately not reproduced here.

**Recommendation:** replace working-context links with owner-approved, public-safe Markdown sources or label unavailable material honestly. Use the existing public GitHub route where verified. Follow the owner's established private-Notion boundary; do not publish private source contents to solve a link problem. **Acceptance:** anonymous visitors can open every artifact represented as public; no private Notion or personal project locator is required to inspect the advertised evidence; unavailable evidence is explicitly marked.

### EXP-10. Case studies mostly demonstrate intended behavior, not measured results

**Confirmed source presentation, Unknown GPT behavior, Medium.** Examples: `bfs-framing-intelligent-futures/index.html:520-636` calls scenarios real conversations; `starbucks/index.html:405-495` describes what the GPT already does; Costco `:391` claims a test harness; Ping `:365` describes a prompt harness. These pages do not include a dated result table or direct result-level evidence alongside those claims. Several pages provide useful prompt specifications, which should be preserved.

**Recommendation:** add a small public evidence panel to each case: version/date, corpus scope, one normal case, one ambiguity case, one refusal or escalation case, observed output excerpt, and limitations. Where original transcripts cannot be published, label scenarios illustrative rather than observed. **Acceptance:** readers can distinguish instruction intent, illustrative examples, and actual test observations without visiting a private workspace. Do not fabricate a passing run. Prioritize BFS, then a representative consumer brand, before replicating the pattern.

### EXP-11. BrandGuard's reach needs a plain mechanism boundary

**Confirmed expansive metaphors, inferred misunderstanding, Medium.** `bfs-framing-intelligent-futures/index.html:222` describes staking semantic territory inside large language models; Brooks `:381` says brands do not own the answer unless they claim it; Starbucks `:607` connects the reusable architecture to claiming semantic territory. A reader could interpret this as a promise that publishing one Custom GPT controls unrelated model outputs, search ranking, or brand ownership.

**Recommendation:** retain the owner's AI-front-door metaphor but pair it with a concrete boundary: this controls the configured demonstration's instructions and selected knowledge, with outcomes subject to testing; effects on unrelated assistants or discovery require separate evidence. **Acceptance:** the page identifies the system actually configured and does not present broad model influence as an established consequence of publication.

### EXP-12. Contact cards require manual reconstruction of the intended email

**Confirmed structure, Proposal, Medium.** `contact/index.html:219-301` lists six inquiry routes and plain-text subject tags. Most cards do not contain their own mailto action; career cards instead include another GPT link. A visitor arriving at a deep contact fragment must scroll back to the general email and copy the subject tag.

**Recommendation:** add a clearly labeled email link with the appropriate subject on each card, keeping the visible email address and sensitive-information guidance at `:193`. Do not add a form service or promise a response SLA without owner input. **Acceptance:** each lens-to-contact deep link lands on a complete inquiry card with the right email subject; visitors without a configured mail app can still copy the address and tag.

### EXP-13. Structured personal claims are absent from the visible biography

**Confirmed mismatch, Unknown credential truth, Medium.** `about/index.html:437` and `index.html:395` put 13+ years and 28 certifications into Person structured data. The reviewed visible main content does not present those counts or evidence, and the identity is shortened to Jamie while the site also uses Jamie for the persona. This makes the machine-readable biography more specific than the visible explanation.

**Recommendation:** distinguish Jamie Hill from the AskJamie persona, and align structured data with visible, owner-approved facts. Add verified credential details only when appropriate evidence is available; do not infer they are false merely because the page lacks support. **Acceptance:** each structured personal assertion is visible or clearly represented on the relevant page and uses the same identity and scope. See [Google structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

### EXP-14. The global navigation downloads oversized identity artwork

**Confirmed file sizes and markup, Medium performance opportunity.** `search/index.html:85` loads the 1024px avatar as a 40x40 navigation image. The source PNG is **756,775 bytes**. It is reused sitewide and also appears in some heroes, so caching helps repeat visits but not the first cold request. The title artwork is 89,453 bytes. Shared CSS is 231,516 bytes, JS 44,849 bytes, and the search index 115,397 bytes. These are disk sizes, not compressed transfer sizes or measured timings.

**Recommendation:** derive visually checked small navigation and responsive hero variants from existing artwork. Preserve the source images and brand. Use the homepage's existing responsive-image pattern on relevant interior images. Prioritize the measured LCP element, since a hero logo and actual LCP image should not compete indiscriminately for high priority. `lens-system/index.html:161` and `resume-representative/index.html:169` combine lazy loading with high fetch priority; most BrandGuard heroes remain lazy. **Acceptance:** visual comparison at 390/1280 and 2x pixel density is acceptable, dimensions and alt text remain correct, cold image transfer decreases, and LCP does not regress. See [web.dev LCP guidance](https://web.dev/articles/optimize-lcp). Keep external Google Fonts as the documented decision.

### EXP-15. Long pages need a shorter route to evidence and next actions

**Confirmed content depth, Proposal, Low.** Main-content ledger extraction estimates roughly 2,010 words on BFS, 1,687 on Mathews, 1,572 on Professional Portfolio, and 1,477 on Brooks, excluding some code and linked text. Each repeats ecosystem and future-of-AI framing after the core proposition. For example, Professional Portfolio `:260`, `:476`, `:524` and Mathews `:420`, `:471`, `:535`, `:656` place multiple distinct reader jobs on one page.

**Recommendation:** offer compact local navigation and a consistent top summary: what it demonstrates, source boundary, evidence, and next action. Keep deeper narrative available. Move only duplicated explanation into links to the existing How page after owner-voice review. **Acceptance:** a first-time visitor can find the demo, limits, evidence, and contact path within one screen of local navigation; headings stay meaningful and anchored at 320px width.

### EXP-16. Utility status and recovery wording need reconciliation

**Confirmed contradiction, Low.** `under-construction.html:159-171` says the main GPT is fully available while its disabled button says the general GPT is coming soon. `404.html:141` calls a missing page technical difficulties, although its explanation correctly covers absent/moved paths.

**Recommendation:** the holding page should point directly to the currently available scoped lenses and use one clear general-GPT status. The 404 heading should state Page not found while preserving the existing illustration and friendly recovery copy. **Acceptance:** utility-page status agrees with the How page, all recovery actions are usable, and an actual unknown route retains HTTP 404 behavior verified by the Architect.

### EXP-17. The Universe fallback is substantially less useful than the diagram

**Confirmed fallback content, Proposal, Medium.** `universe/index.html:189-324` contains the detailed linked graph. The noscript fallback at `:328-340` names only broad families and provides one contact link. `:367` says some nodes are live and some experimental without identifying each node's status. Human screen-reader output remains unverified.

**Recommendation:** add a visible expandable text outline of the same families, links, and known status, available whether Mermaid succeeds or fails. Preserve the existing affiliate note directly below the diagram. **Acceptance:** a nonvisual reader or visitor with failed Mermaid loading can reach the same meaningful destinations and distinguish current public pages from concepts without interpreting source syntax. Use [W3C reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) for the diagram's bounded horizontal scrolling and surrounding prose.

### EXP-18. Templates retain real destination-specific links

**Confirmed maintenance hazard, Low.** `assets/templates/template--case-study.html:215` retains a real LEGO GPT destination and `:230` a ChatGPT project workspace. `template--lens-detail.html:203` and `:550` retain the Resume GPT. The homepage template `:179` still lazy-loads its hero while the real homepage has improved image markup.

**Recommendation:** replace identity-specific template links with required named placeholders and add a generation-time check that every placeholder is resolved to the intended page. Update performance and disclosure patterns at their source template after each approved improvement. **Acceptance:** a newly scaffolded case cannot silently point at another brand's GPT or personal workspace; templates remain excluded from public deployment and page QA counts.

### EXP-19. Light footer text is overridden by dark-footer rules

**Confirmed source and Architect browser observation, High accessibility defect.** Baseline `assets/css/theme.css:197-207` gives light-theme footers pale translucent text intended for a dark surface. These selectors outrank AskJamie rules at `:7321-7339`. The Architect observed `rgba(229,231,235,0.6)` links and `rgba(229,231,235,0.75)` inherited text over `rgb(247,243,238)` paper. Dark-mode footer headings also need to use the active foreground rather than the fixed light heading token.

**Remediation:** added AskJamie-scoped higher-specificity text/link/heading rules consuming existing semantic colors. Backgrounds, typography, layout, and other brands remain intact. **Acceptance result:** focused local browser checks found minimum contrast of 6.24:1 in light and 6.75:1 in dark across footer paragraphs, links, and headings. This is a measured footer result, not whole-site WCAG certification.

## Page-by-page coverage

All rows received source review. Shared EXP-01, EXP-04, EXP-05, and EXP-14 apply where the corresponding shell or reveal components exist. Rows do not claim each route was visually inspected by this worker.

| Source page | Primary job and evidence location | Meaningful observation and next improvement |
| --- | --- | --- |
| `index.html` | Introduce AskJamie, `:140`, `:164-165`, `:185-215` | Clear paper/voice identity and responsive hero markup; first two actions prioritize BrandGuard and Lens System rather than a general chat box. Align BFS teaser, structured personal claims, and How-page discovery. |
| `about/index.html` | Explain persona and owner, `:167`, `:190-205`, `:252-281` | Helpful what-it-is-not section conflicts with enterprise-ready language. Distinguish human biography, persona, and demonstrated readiness. |
| `contact/index.html` | Route inquiries, `:180-199`, `:219-301` | Visible direct email and sensitive-detail caution are useful. Complete each inquiry card with its own subject-specific mail action. |
| `how-askjamie-works/index.html` | Explain actual method and limits, `:127-145`, `:194-219` | Strongest statement of no hidden data handoff, external dependencies, and absent general chat. Use as canonical explanation for older pages. |
| `legal/index.html` | Disclosures, `:218-259` | Public-only/non-affiliation boundary and analytics disclosure are explicit. Preserve owner-decided analytics and fonts; legal sufficiency is outside this review. |
| `search/index.html` | Find pages, `:123-149` | Useful domain-specific example queries and live result status; shared overlay copy, Enter/Escape contract, and result-list semantics need repair. |
| `universe/index.html` | Orient across projects, `:189-324`, `:328-369` | Extensive graph destinations and preserved referral note; add equivalent text outline and specific known statuses. |
| `lens-system/index.html` | Choose four lenses, `:165-171`, `:269-347` | Clearly rejects hidden handoffs. Offer user-task comparison and direct try/read choices; avoid treating every linked GPT as runtime-verified. |
| `lens-system/resume-representative/index.html` | Career-agent pattern, `:173-195`, `:295-337`, `:520` | Prototype context exists but always-on/commercial claims and kit availability are broader. Keep factual human approval central and clarify deliverable. |
| `lens-system/professional-portfolio/index.html` | Portfolio-agent recipe, `:190-195`, `:343-382`, `:455`, `:524-537` | Meaningful method-versus-persona distinction. Resolve unsupported price comparison and missing grab-the-kit destination; shorten path to evidence. |
| `lens-system/enterprise-sleuth/index.html` | Enterprise knowledge pattern, `:173-195`, `:254-264`, `:318-398` | Portability is described but platform equivalence and enterprise readiness are unverified. Separate reference design from actual integrations and evidence. |
| `lens-system/okhp3-brandguard/index.html` | Explain pattern and browse 13 cases, `:174`, `:271`, `:567-703` | Breadth is real; a case index is valuable. Add a comparison by demonstrated behavior and evidence maturity, not a new generalized product promise. |
| `lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/index.html` | BFS prototype, `:215-243`, `:373-422`, `:520-636` | Explicit personal/public-only boundary is strong. Shared teaser conflicts with it; label real-conversation evidence and constrain semantic-territory claims. |
| `lens-system/okhp3-brandguard/lego/index.html` | Adult-framed family-brand guide, `:353-369`, `:401-415`, `:425` | Direct LEGO history/Fair Play sources and adult framing are useful. Keep these specifics; remove private-workspace dependence and distinguish tested behavior. |
| `lens-system/okhp3-brandguard/starbucks/index.html` | Menu/support vocabulary prototype, `:273`, `:405-495` | Clear account separation and official allergen routing. Real-conversation wording needs dated observation or illustrative labeling. |
| `lens-system/okhp3-brandguard/brooks-running/index.html` | Runner guidance, `:299`, `:338-356`, `:496-536` | Concrete non-diagnosis boundary and public instruction spine. Improve evidence access and temper ownership-of-AI-answer framing. |
| `lens-system/okhp3-brandguard/ping/index.html` | Golf-fitting orientation, `:289-295`, `:334-365`, `:419-501` | Good fitter escalation, rumor refusal, and account disclaimer. Expose actual harness results and public artifact route. |
| `lens-system/okhp3-brandguard/costco/index.html` | Membership/model explainer, `:349-391`, `:460-541` | Avoids live inventory and stale prices in its stated design. Claimed 12-14-file corpus and test harness need inspectable version/evidence. |
| `lens-system/okhp3-brandguard/hershey/index.html` | Confection/brand-story prototype, `:316`, `:457-523` | Warm metaphor explicitly separated from official statements; ingredient/allergen routing is sensible. Evidence and public artifact access remain unverified. |
| `lens-system/okhp3-brandguard/lvmh/index.html` | Holding-company/maison orientation, `:331`, `:426-472`, `:575-607` | Distinct institutional audience is a strength. Preserve group/maison separation; show dated examples for current-news routing. |
| `lens-system/okhp3-brandguard/dollar-general/index.html` | Budget-shopping orientation, `:316-339`, `:412-466` | Specific budget/coupon/store-locator use cases make the concept understandable. Validate source-routing samples and replace private brief link. |
| `lens-system/okhp3-brandguard/coca-cola/index.html` | Archivist-style brand prototype, `:346-387`, `:398-457` | Copy-ready instruction spine gives visitors more evidence than generic sales prose. Replace private spec path and distinguish copy-ready draft from tested deployment. |
| `lens-system/okhp3-brandguard/discount-tire/index.html` | Safety-focused tire education, `:258`, `:377-484` | Explicit fitment/manual/professional routing is valuable. Remove build-history sentence at `:282` and reconcile public-artifact claim with workspace links. |
| `lens-system/okhp3-brandguard/scheels/index.html` | Sporting-goods orientation, `:295`, `:425-545` | Useful no-inventory/no-store-ops boundaries. Clarify allowed sporting context versus broad weapons refusal wording through observed tests, not speculative policy rewriting. |
| `lens-system/okhp3-brandguard/mathews-archery/index.html` | Archery-brand orientation, `:295`, `:471-580`, `:622-645` | Longer brand history is distinct content; hunting-law and bow-choice examples need dated source/escalation evidence and clearer local navigation. |
| `404.html` | Missing-path recovery, `:141-194` | Working home/report routes and friendly artwork. Name missing-page state directly, and verify actual unknown-path status server-side. |
| `under-construction.html` | Unfinished-path recovery, `:153-171` | Strong branded holding page; fully-available versus coming-soon GPT wording directly conflicts. Route to live scoped lenses. |

## Recommended delegation and sequence

1. **Worker: shared interaction repair.** Complete approved EXP-01/02, then Architect-reviewed EXP-03/04/05 if runtime evidence confirms them. Scope the AskJamie behavior, respect sister-site synchronization, retain browser regression evidence, and regenerate asset hashes once after shared edits are final.
2. **Worker: truth and public evidence.** Draft the minimal EXP-06/07/08/09/13 changes in one reviewable copy package. The PM resolves owner-only facts rather than guessing prices, credentials, affiliations, or availability. Public-source packaging precedes link replacement.
3. **Worker: representative case evidence.** Pilot EXP-10/11 on BFS and one consumer case, with an explicit evidence boundary. The PM approves the pattern before distributing across the remaining 11 cases.
4. **Worker: image and navigation polish.** Use browser measurements for EXP-14, then EXP-12/15/16/17. Preserve existing artwork and narrative. A framework migration or hosting change is unnecessary for these outcomes.
5. **PM: reusable template alignment.** Apply EXP-18 after the final patterns are validated, so new pages do not recreate fixed problems.

Each worker must provide before/after evidence, changed paths, a meaningful acceptance result, and remaining uncertainty. The Architect integrates and decides what is ready to publish. Copilot or Replit could perform a bounded worker package, but should receive the same exact source baseline, scope, acceptance checks, and no-sibling/no-publication boundaries.

## Current primary-source guidance used

Retrieved September 5, 2026. These inform the practical checks; they do not establish site conformance by themselves.

- [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md): applied to semantics, focus, resilient content, motion, and images. Repo instructions override generic editorial rules, including preserving owner voice and US English.
- [W3C WCAG 2.2 reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html): test ordinary prose at 320 CSS pixels and keep necessary diagram scrolling within the diagram.
- [W3C target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html): measure target sizes and permitted spacing exceptions rather than declaring all targets below 44px failures.
- [W3C bypass blocks](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html): verify functional keyboard skipping, not just the presence of a skip-link element.
- [W3C modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/): verify focus entry, containment, Escape, and return, including mobile navigation interactions.
- [Google structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies): align markup with represented page content; syntax validity is not rich-result eligibility or ranking proof.
- [web.dev LCP optimization](https://web.dev/articles/optimize-lcp): avoid lazy-loading a measured LCP image and prioritize resources using actual traces.

## Authorized local remediation and validation

The Architect approved EXP-01/02 plus the runtime-confirmed EXP-05/19 for immediate local repair. `assets/js/app.js` now selects AskJamie overlay copy before construction, implements dedicated-page keyboard actions with modifier/composition guards, and arms AskJamie scroll reveal only after an observer exists. `assets/css/theme.css` leaves AskJamie content visible by default and fixes footer contrast using the existing palette. Other content, private-link, offer, and skip-link recommendations remain outstanding unless the Architect records a later change.

`scripts/experience-qa.cjs` runs against the local source server using already-available Playwright/Chromium. Its focused cases cover all six overlay suggestions, no-result help, focus return, Enter navigation, delayed index loading with a changed query, Escape/query/category state, modifier/composition preservation, other-brand copy, no-JS and blocked-script rendering, optional reveal/reduced-motion behavior, and light/dark footer contrast. External requests are blocked for deterministic local checks, so these results do not measure production network latency or third-party availability. All 11 focused cases passed. Detailed results are in `experience-qa-results.json`. See the Architect's `validation-and-changes.md` for the combined final release checks and publication status.

The Architect separately probed 17 public GPT URLs: 13 returned HTTP 200, while Starbucks BRG02, Costco BRG05, LVMH BRG07, and Coca-Cola BRG09 returned HTTP 404 in that probe. This is an observed transport result; it does not establish why the service returned it, and HTTP 200 does not prove an interactive GPT works. Use `evidence/public-gpt-probe.txt` and work package WP07 for follow-up. No GPT CTA was silently changed by this worker.

## Explicit unknowns

Human VoiceOver/NVDA spoken output, Safari/Firefox behavior, genuine device zoom and touch ergonomics, field Core Web Vitals, anonymous access to every external GPT/repository/artifact, actual GPT corpus/version/evaluation results, offer availability/pricing, credential substantiation, and external service terms are not proven by this source audit. The Architect's current browser findings may close some local rendering and keyboard unknowns. Do not convert source compliance, HTTP availability, or a successful static audit into proof of these wider outcomes.

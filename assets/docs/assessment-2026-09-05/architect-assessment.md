# AskJamie website assessment and architecture direction

Assessment date: September 5, 2026. Target: `OKHP3/AskJamie` and `https://askjamie.bot/`.

## Architectural judgment

Keep the static HTML architecture and the AskJamie paper-and-teal identity. Both fit the site's actual job: explain the Lens System, demonstrate public-information concepts, and help visitors decide whether to explore a GPT or contact Jamie. A backend or framework migration would add operating obligations without resolving the defects observed here.

The most valuable next investment is reliable visitor journeys and truthful, consistent presentation. The codebase has substantial validation and release machinery, but passing those checks has allowed wrong-brand search copy, unreadable footer links, and a JavaScript-dependent content reveal to reach production. The engineering opportunity is to make the existing quality gates represent what a visitor actually sees and does.

This is a comprehensive source and representative runtime assessment, not proof that every browser, assistive technology, external GPT, business claim, or future release is correct. Findings below distinguish observations from recommendations. No visitor analytics, private Notion content, or authenticated GPT conversations were accessed.

## Reading and delivery map

- [Delivery plan and delegated work packages](delivery-plan.md): priorities, owners, dependencies, acceptance criteria, and release boundaries.
- [Infrastructure and security assessment](infrastructure-security.md): packaging, CI, hosting, shared tooling, dependency and security findings.
- [Experience and content assessment](experience-content.md): route coverage, accessibility, search, navigation, content credibility, and visual recommendations.
- [Validation and implementation record](validation-and-changes.md): final local changes, check outcomes, and remaining release conditions.
- [Evidence directory](evidence/): timestamped GitHub, HTTP, source, and browser observations.

## Baseline and scope

The clone began clean at `04cc3e7b8965f568253b6e2c18aa532f6e2a3d57`. A fetch discovered one newer merged commit. The clean clone was fast-forwarded to `fd1ea19eb9c07c7c72c38281130413c6199bd0cc`, the deployed baseline for this review. No merge was manufactured and no recovery branch was removed.

The source inventory contains 27 public HTML paths: 25 sitemap/search routes and two utility pages. Nine developer templates and a tracked generated `dist-pages` tree are separate inventories. The new How AskJamie Works route explains why older 26-page and 192-check claims are stale. The release uses GitHub Actions to prepare and deploy an allowlisted static artifact. There is no application compilation step or server-side application runtime.

All 27 live HTML responses returned 200 and were byte-identical to their source files at the deployed baseline. A nonexistent route returned 404. `/AGENTS.md`, `/scripts/prepare-pages-artifact.py`, and the probed image-directory `.DS_Store` path returned 404. These exact probes support the observed artifact boundary; they are not an exhaustive public-file or historical exposure scan. [HTTP evidence](evidence/hosted-http.json)

GitHub Pages reports `build_type: workflow`, HTTPS enforcement, an approved certificate, and a built site. Both validation and deployment jobs succeeded for the baseline SHA in [run 33979307147](https://github.com/OKHP3/AskJamie/actions/runs/33979307147). Its logs report 200 browser checks without failures, successful JavaScript smoke tests, and 316 packaged files. Fresh local packaging before remediation produced 319 files because it included local-only metadata. File counts measure artifact membership, not visitor transfer size. [Pages settings](evidence/pages-settings.json), [job evidence](evidence/ci-jobs.json)

The referenced OverKill-Hill conversation was not readable on this host. The hierarchy and task scope come from the user's supplied instructions. Neither sibling repository was modified or used as an unquestioned source of current AskJamie behavior.

## Priority decisions

Priority indicates impact and ordering, not a claim of an active exploit or measured lost revenue.

| Priority | Observation | Architectural recommendation | Status |
|---|---|---|---|
| P1 | Light-mode footer links render near white on paper; important contact and navigation links are hard to read. | Correct AskJamie selector precedence and test computed contrast across light, dark, and automatic modes. | Delegated first batch |
| P1 | Four homepage sections have opacity zero with JavaScript disabled, desktop viewport, and normal motion preference. | Make content visible by default; enable animation only when its controller is ready. | Delegated first batch |
| P1 | Packaging recursively replaces its selected output before validating that the destination is safe. Broad directory admission also copies unintended files. | Validate output ownership before deletion; preserve source originals while filtering the release artifact; test refusal cases. | Delegated first batch |
| P1 | The live `.well-known/security.txt` URL returns 404 although the source exists. The intermediate artifact upload omits hidden paths by default. | Explicitly retain intended `.well-known` content through the artifact chain after filtering incidental hidden files. Verify hosted readback after publication. | Delegated first batch; hosted result pending |
| P1 | The search overlay says OverKill Hill and Forge, and suggests content outside AskJamie's portfolio. Dedicated search promises unimplemented keyboard shortcuts. | Give AskJamie its own search strings and implement the visible keyboard contract without changing sibling behavior. | Delegated first batch |
| P1 | `main` has no classic branch protection and the repository ruleset response is empty. | Configure a proportionate ruleset requiring the validation check and an intentional review path, with an explicit owner bypass policy. | Settings proposal |
| P1 | Infrastructure worker identified unsafe lock handling and cross-repository mutation assumptions in the shared synchronization utility. | Retire unsafe apply behavior until process ownership, dirty-tree preservation, target authorization, and hook outcomes are enforced. | Separate bounded tooling package |
| P1 | Four outbound GPT URLs returned 404 in both HTTP probes and a fresh signed-out Chromium context: Starbucks, Costco, LVMH, and Coca-Cola. | Reconcile the current public destination or show an accurate availability state; preserve case-study content. | External availability package |
| P1/P2 | The recurring Builders FirstSource banner implies company adoption while the case study says it is an independent, unaffiliated demonstration. | Align the banner and CTAs with documented prototype status. Require evidence for adoption, training scale, and enterprise-readiness claims. | Editorial decision package |
| P2 | BrandGuard link-card anchors render inline, fragmenting their border/padding. | Give the 13 case links a tested block/flex card layout and stable visual capture. | Focused visual follow-up |
| P2 | Current local browser checks had intermittent timeout failures; static checks cannot detect visual and semantic defects. | Retain failure evidence, isolate third-party effects, require actual browser mode in CI, and add journey-specific tests. | QA package |
| P2 | CI uses Node 20, which is now end of life, and mixes pinned and mutable action references. | Test a supported LTS toolchain, pin action revisions, and document dependency update ownership. | CI maintenance package |
| P2 | Project guidance, the scorecard, and the roadmap contradict current deployed capabilities. | Keep one present-tense status record and link to dated evidence; preserve historical ADR decisions with explicit correction notes. | Delegated first batch |
| P2 | Historical mobile Lighthouse results show weak loading performance. Fresh Lighthouse is unavailable locally. | Establish a repeatable current mobile baseline, then optimize the measured critical path with budgets. | Measurement-first performance package |
| P2 | Ten BrandGuard case pages link to Notion working/source material, according to the source inventory. | Confirm the intended public route for each link and publish approved, source-bounded summaries before replacing links. | Owner/source review package |
| P3 | Shared CSS includes several site families and accumulated overrides. | Separate brand configuration from shared behavior incrementally, backed by cross-brand contract tests in a separately authorized effort. | Architectural follow-up |

## Visitor experience and content direction

### Clarify the first decision

The homepage has an identifiable personality and a legible explanation of the human behind the persona. Preserve those strengths. The first screen also asks visitors to interpret AskJamie, the Lens System, BrandGuard, a build-in-progress notice, the R&D studio, and several CTAs. This is a design judgment, not a measured conversion failure.

Recommend a simple visitor decision: explore an example, understand how the system works, or contact Jamie. Use one primary action per page and a descriptive secondary action. Position support/donation as a supporting route after the visitor has seen useful evidence. Keep the owner's plainspoken voice and vintage imagery. Avoid replacing it with generic consultancy copy.

### Explain what can actually be used

Apply the same availability vocabulary to the hub, case page, card, search excerpt, and outbound CTA: public GPT, public-information demonstration, concept, or unavailable. The 13 BrandGuard pages should not imply 13 publicly launched services. Maintain the existing non-affiliation disclosures and bring any contradictory headline into agreement with them.

The separate public-GPT probe checked 17 configured destinations: 13 returned HTTP 200 and four returned 404. Chromium confirmed the four 404 status responses. HTTP 200 does not prove that a GPT conversation can be started or that the model performs as described. The reason for a 404 is unknown; it does not establish deletion, privacy settings, or withdrawal by the owner. [Probe evidence](evidence/public-gpt-probe.txt), [browser status evidence](evidence/gpt-browser-status.json)

Treat claims of enterprise readiness, scale, company adoption, and outcomes as claims needing evidence. The appropriate remediation may be a narrower sentence rather than a new technical feature. Do not invent client authorization, evaluation results, training corpus size, or commercial offerings to make the portfolio look complete.

### Strengthen complete journeys

Judge success by observable end states: a new visitor understands the offer; a reader can compare lenses; a keyboard user can find and open a result; a mobile visitor can close navigation and recover focus; a reader can identify prototype status before leaving for ChatGPT; a visitor knows that contact opens their mail application. These are useful acceptance criteria without needing a backend.

The source worker's route ledger covers all source HTML paths. Root runtime inspection sampled homepage, Lens System, BrandGuard hub, BFS case, How It Works, Contact, and Universe at 390px and 1280px. All sampled page widths fit their viewport. The full responsive suite covered the 25 sitemap routes at eight widths. It checks overflow, errors and assets, not complete accessibility conformance.

### Accessibility and resilience

Adopt WCAG 2.2 AA as the review target, including focus visibility, focus not obscured, reflow, contrast, keyboard operation, and target size with its spacing exceptions. Do not reduce this to a Lighthouse accessibility score. The first batch addresses observed contrast, search, and missing-content failures. Follow-up work should exercise skip-link focus, search result semantics, reduced motion, text resizing, 400% browser zoom, 320 CSS-pixel reflow, and mobile navigation focus. [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)

Keep useful content, ordinary navigation, contact details, and diagram alternatives available when scripts or external resources fail. Human VoiceOver and NVDA sessions remain required evidence for spoken behavior. Chromium screenshots do not prove it.

## Infrastructure and operating direction

### Release model

Continue using an explicit public artifact. Treat source, generated output, the uploaded artifact, and the deployed site as distinct states. CI should validate once, package the approved source, upload the same artifact, and verify essential hosted paths after deployment. GitHub documents this custom workflow model. [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

The tracked `dist-pages` directory is stale relative to current source and creates a second apparent version of the site. Preserve it during this assessment. Recommend a separate change to remove generated output from version control only after confirming recovery, downstream consumers, and a reproducible replacement. Existing backup refs also stay intact.

### Security boundaries

The response headers observed on the homepage do not include the CSP, anti-framing, or Permissions-Policy values described by `_headers`. The meta CSP is still a real browser policy; `_headers` content is not proof of edge enforcement on GitHub Pages. In particular, `frame-ancestors` cannot be enforced through a meta element. This is a hosting-capability limitation to document or resolve through an explicitly selected edge, not evidence that the whole site is insecure. [HTTP evidence](evidence/hosted-http.json), [MDN frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors)

Prioritize maintainers' execution risks alongside browser risks: artifact deletion boundaries, unsafe synchronization, mutable CI components, and permissive merge paths. Do not add authentication or a server merely to compensate for weaknesses in a static deployment pipeline. GitHub recommends full commit SHA pinning for immutable action references. [GitHub secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

Upgrade CI from Node 20 through a compatibility-tested task. Node's current release table marks v20 EOL and v22/v24 LTS; selecting the supported major and testing the lockfile is more defensible than automatically selecting the newest Current release. This affects QA tooling, not a website server runtime. [Node.js release table](https://nodejs.org/en/about/previous-releases)

The observed unconditional GA4 and external Google Fonts policies are intentional in current project guidance. Preserve them within this assessment. Neither the source nor this review establishes legal compliance or analytics outcomes. Any policy change needs its own business and jurisdictional decision, not an unsolicited consent-platform implementation.

### Performance and asset management

The September 4 mobile Lighthouse summary records performance scores of 60, 71, 70, and 72 for homepage, BrandGuard, Universe, and Search; recorded LCP is approximately 8.94, 7.80, 6.46, and 6.75 seconds. Those are historical local lab results, not fresh field measurements or proof of current visitor experience. The local Lighthouse package is unavailable, so this review does not claim a new score. [Historical report](../../audit/lighthouse-2026-09-04-final4-mobile/summary.json)

The shared CSS is approximately 231 KB uncompressed and includes multiple brand families. Large original images and two PDN design files are also present. Repository or artifact size must not be confused with the bytes loaded by an individual visit. Preserve originals and measure actual critical requests before recommending image changes. Start with homepage LCP attribution, font timing, CSS coverage, and the Universe runtime cost. Use repeatable mobile runs with a documented browser, throttling, cache state, and median of multiple runs.

Proposed field targets are LCP at or below 2.5 seconds, INP at or below 200 ms, and CLS at or below 0.1 at the 75th percentile. Lab measurements guide debugging; real-user evidence is needed for field claims. Retain intentional font choices unless an owner-approved typography decision changes them. [Web Vitals](https://web.dev/articles/vitals)

### Search, SEO, and localization

Sitemap, canonical URLs, structured data, and generated search coverage are already useful foundations. Verify descriptions against each page's actual availability and content. Rich-result eligibility and search rankings cannot be inferred from valid JSON-LD alone. Track indexing through authorized Search Console/Bing access if the owner prioritizes it. [Google structured data guidance](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)

The merged locale-menu foundation and installed translation skills do not establish published translations. Translation remains a content and quality program: an approved locale pair, owned source text, a glossary and voice profile, reviewable drafts, correct navigation and metadata, and drift checks. Do not publish empty language options or claim translated coverage because a skill exists.

The owner's subsequent translation-cleanup request produced a focused follow-up:
duplicate helpers and undiscovered tests were consolidated, inherited locale
claims were corrected, and the detector's stale-record adoption path was
repaired. The detector remains part of the skill-based approach. See the
[cleanup record](../translation-cleanup-2026-09-05/README.md) for final evidence
and the distinction between inactive tooling and published translation coverage.

## Branches, prototypes, and preservation

At inspection there were no open PRs or issues. Remote branches included `main`, the foundation branch, the source-validation fix branch, and the locale-menu branch. Foundation is ancestor-merged. `git cherry` marks the fix and locale commits with `-`, indicating patch equivalence in main even though their original commit IDs are not ancestors. They are not three unfinished feature streams. Deleting them is outside this work. [Git inventory](evidence/git-inventory.json), [open PRs](evidence/open-prs.json)

Two local backup refs preserve earlier reconciliation work. One local worktree exists, and the stash inventory is empty. Those facts do not establish the absence of work on another host or of unreachable recovery objects. No destructive history cleanup or reflog pruning was performed.

The prototype backlog should be driven by visitor value and source evidence. Keep documented concepts visible as concepts. Defer PWA/service-worker work, a prompt library, new lenses, and broader design changes until there is a clear use case and acceptance criteria. They are proposals, not gaps whose mere existence makes the current architecture inadequate.

## Execution model and release decision

This thread serves as Project Architect. A delegated Project Manager assigned two Workers for infrastructure/security and experience/content. The workers assessed independently by domain, proposed a first batch, and received bounded implementation assignments through the manager. The manager owns integration and work packages; the architect reviews cross-domain evidence and the final result. This is an agent hierarchy within this task, not a claim that separate persistent Codex UI tasks were created.

The first batch is local and reviewable. It does not authorize or perform publishing, GitHub settings changes, sibling synchronization, private-source publication, a new dependency, or a framework migration. Larger work packages identify those boundaries explicitly. Copilot can implement narrowly scoped source/test packages from the delivery plan; Replit can explore approved visual alternatives against a preserved baseline; repository settings remain a GitHub owner task. No message was sent to those external services.

Release status and the exact executed tests belong in [validation-and-changes.md](validation-and-changes.md). Architectural acceptance requires preserving the baseline failures, testing changed behavior, reviewing the artifact contents, and confirming the live site after a separately authorized publication. The recommendation is to finish and review the bounded first batch, then address merge protection, the unsafe sync utility, and content credibility before expanding features.

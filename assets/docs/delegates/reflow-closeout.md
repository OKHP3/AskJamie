# Found-Ry enlarged-text reflow closeout

Date: 2026-09-08

The earlier W03 sample found horizontal overflow at 320, 390, and 1280px
when root and body text were enlarged to 32px. The final correction is scoped
to AskJamie in the existing shared stylesheet. Header controls can wrap;
mobile submenus can shrink; grid children, headings, and card copy can wrap
within their available width. Desktop footer column proportions are preserved.
No sibling repository was changed and no new overflow-hiding rule was added.

`tests/test_foundry_reflow.spec.mjs` passes at 320, 390, 768, and 1280px with
16px and 32px root/body text. It checks document overflow and text clipping,
including the open mobile menu. The same regression now runs in Pages CI.
This is synthetic text enlargement, not native browser zoom or human
screen-reader certification. Third-party requests are blocked for repeatability.

Normal-size browser responsive QA passed all 208 route/viewport combinations.
JavaScript smoke, Universe browser, and experience checks also passed. Visual
capture readiness passed on the homepage, Lens hub, BrandGuard detail, and
Universe at 390 and 1280px. The normal viewport and captured content retain the
paper palette, artwork, and layout. External fonts were blocked, so those
captures are not replacements for references captured with different font
conditions. The existing full-page capture can include the off-canvas mobile
menu in its tall image; direct viewport inspection confirmed the closed menu
remains above the visible viewport. Historical committed references were kept.

No performance improvement or field measurement is claimed by this repair.

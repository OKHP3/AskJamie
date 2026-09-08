# W02 Found-Ry Keyboard Accessibility

Scope: `/found-ry/`

Branch: `codex/w02-found-ry-keyboard`

Base SHA: `e9902c5358506252ae0aba8b805c26f7f9d18924`

Allowed write path: `assets/docs/delegates/w02-keyboard.md`

## What I checked

- Keyboard tab order from the page body into the document.
- Skip link behavior.
- Activation of the skip link.
- Presence of the primary navigation landmark and the main landmark.
- Link reachability through the header, page content, and footer.

## Evidence

1. The page exposes a visible skip link with `href="#main"`.
2. A controlled keyboard pass from the page content produced this sequence:
   - `Skip to content`
   - logo/home link
   - `Who's AskJamie™`
3. Activating the skip link moved focus to `<main id="main">` and scrolled the page to the main content.
4. The accessibility tree showed a labeled primary navigation area and a `main` landmark.

## Result

No reproducible keyboard accessibility issue was found on the current `/found-ry/` page.

## Patch

No code patch was justified.

## Notes

- The first uncontrolled tab attempt looked odd because browser focus likely started outside the page. A controlled page-content start confirmed the expected order.
- If a future edit changes header or skip-link styling, rerun the same keyboard pass to make sure the behavior stays intact.

# W06 Found-Ry visitor journey

Date: 2026-09-08. Branch: `codex/w06-foundry-journey`. Base SHA:
`e9902c5358506252ae0aba8b805c26f7f9d18924`.

## Scope

Public-safe synthetic review of the website-to-repository-to-local-start path
for the AskJamie Found-Ry feature page. I checked the public page copy against
the repository README and Replit notes, then looked for a clear next step that
would help a maintainer move from the site to local startup without guessing.

## Observed path

1. The public feature page at `/found-ry/` presents Found-Ry as a private local
   alpha and says there is no public hosted version.
2. The repository docs say the project is a static site and that the local start
   command is `python3 -m http.server 5000 --bind 0.0.0.0`.
3. `replit.md` repeats the same local start command and says the preview serves
   the repository root.

## Availability claims that may confuse visitors

- The page says the workbench is a "Working local alpha" and that a public
  hosted version is not available. That is accurate for a maintainer, but a
  casual visitor can read it as if there is no local way to try the workbench
  at all.
- The page says "Contact Jamie" for discussion, but it does not point a
  maintainer toward the repository docs or the local start command.
- The page avoids any repository link, which is good for privacy, but it also
  means the journey ends at a contact prompt instead of a clear maintainer
  handoff.

## Broken-link check

- I did not find a broken internal link in the Found-Ry page source during this
  review.
- The external links in the page source are syntactically valid, but I did not
  treat live availability as proven because this was a source-level review.

## Concise corrections

1. Keep the privacy boundary, but replace the availability copy with a clearer
   maintainer split. Suggested direction: "This public page explains the
   private workbench. Maintainers can start it locally from the repository."
2. Add one short next-step cue that points to the repo instructions instead of
   only the contact path. Suggested direction: "If you maintain the workbench,
   open the repository README or Replit notes for the local start command."
3. Keep the public page free of private repo links. The correction should be a
   wording change, not a public source disclosure.

## Evidence summary

- Public page inspected: [`found-ry/index.html`](/Users/okh/.codex/worktrees/10c7/AskJamie/found-ry/index.html)
- Repo start command documented in [`README.md`](/Users/okh/.codex/worktrees/10c7/AskJamie/README.md)
- Same start command repeated in [`replit.md`](/Users/okh/.codex/worktrees/10c7/AskJamie/replit.md)

## Recommended disposition

CLEAR for documentation-only follow-up. The issue is not a broken page route.
It is a missing maintainer handoff sentence that would make the private local
path easier to recognize.

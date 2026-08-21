# Provenance, portability, and handoff

## Portability note

The portable core is the ordered check contract, result classification,
artifact-boundary review, and authorization gate. A client needs only a
filesystem, a shell-capable runner, and the repository's declared runtimes.

Adapters are optional:

- **Filesystem adapter:** resolves the repository root and disposable artifact
  directory; it must not accept an unresolved broad path.
- **Browser adapter:** supplies a local server, Playwright, Chromium, and an
  authorized hosted URL. Without it, browser and hosted checks are `not-run`.
- **GitHub Actions adapter:** reads workflow logs and artifact metadata. It
  cannot be inferred from local success.
- **Replit adapter:** may use the configured workflow/preview, but the core
  commands remain ordinary shell commands and do not require Replit APIs.

No host-specific adapter is required for HTML, link, test, index, audit, or
artifact checks.

## Provenance and release note

The procedure was informed by release mechanics observed across AskJamie,
OverKill Hill, and Glee-fully: deterministic validation, generated-file
freshness, responsive checks, and a shared rebuild → validate → artifact
pattern. Reuse is limited to mechanics supported by evidence. Each site keeps
its own appearance, content, brand rules, and site-specific audits.

Current evidence for this repository is recorded in
`assets/docs/site-release-audit-2026-08-21.md`. That report is historical
evidence for the site state it evaluated; it does not benchmark this skill or
prove a later release.

## Handoff checklist

Before a release handoff, include the skill version, command outputs, runtime
versions, changed/generated files, artifact manifest and digest, CI run
reference if available, hosted URL and revision if checked, and all `not-run`
limitations. State that no commit, push, deploy, or external publication was
performed unless separately authorized.
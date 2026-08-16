---
name: Git credential setup for AskJamie repo
description: GITHUB_PAT must be re-applied each session before pushing to origin
---

## Rule
Before any `git push origin main`, run:
```bash
git config credential.helper store
printf 'https://x-oauth-basic:%s@github.com\n' "$GITHUB_PAT" > ~/.git-credentials
```

**Why:** The credential helper does not persist across Replit container restarts. Push fails with "Invalid username or token" without this step. The `GITHUB_PAT` secret is already available in the environment.

## Remote
`https://github.com/OKHP3/AskJamie.git`

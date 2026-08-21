---
name: GitHub Pages artifact publishing
description: Durable constraints for publishing this static site through GitHub Pages
---

GitHub Pages must use workflow publishing, not legacy branch publishing, when the repository contains scripts, tests, task metadata, and development configuration. The validated artifact allowlist must include both runtime assets and all public page trees.

**Why:** Legacy branch publishing exposed repository-only files, while an overly narrow artifact allowlist removed valid nested pages from the published site.

**How to apply:** Keep `package-lock.json` tracked when Actions uses npm cache detection, set the repository Pages build type to workflow, and verify both required routes and repository-only paths on the custom domain after every release.
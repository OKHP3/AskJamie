# Technology review: September 20, 2026

The seven dependency proposals in PRs 47–53 passed Site Validation and were
integrated through PR 54. Main validation and Pages run 35517515822 passed.

The next reviewed changes select Node 24.21.0 LTS in the local manifest,
lockfile, and CI; select the supported `nodejs-24` Replit module; update
Lighthouse to 13.5.0; and update the Node and Pages actions together. The
complete site and browser suite remains the release gate. The additional
Python matrix exercises both 3.11 and 3.14 before deployment.

The [Replit module registry](https://github.com/replit/nixmodules/blob/main/pkgs/modules/default.nix)
lists Node 24 but no Python 3.14 module at this review. The deployment Python
selector and Replit module therefore remain 3.11. Selecting a module in source
does not establish that the running Replit host has adopted it. Python
freshness alerts remain visible; review provider support again by October 20.

Mermaid remains the complete vendored 11.17.2 release. The
[Mermaid 12 migration](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0)
changes layout, appearance, and browser requirements. Its update still needs
the integrity receipt, dependency review, complete bundle replacement, and
desktop/mobile diagram comparisons required by the technology update policy.
The existing version-watch issue and freshness alert remain open for that
work; review by October 20. A newer version alone is not compatibility or
security evidence.

The local Windows Python suite has eight platform-specific fixture failures
(symlink privileges and POSIX shell fixtures). Its UTF-8 run passed 86 tests
and 12 subtests. The full Linux suite passed on PR 54. Candidate runtime
compatibility and hosted behavior require their own new CI evidence.

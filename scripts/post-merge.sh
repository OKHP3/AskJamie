#!/bin/bash
set -e

# AskJamie™ — post-merge setup
# Static HTML site — no build step required.
# Verifies key files exist, rebuilds search index, and runs all local gates.

echo "Post-merge: verifying static site integrity..."

for f in index.html assets/css/theme.css assets/js/app.js; do
  if [ ! -f "$f" ]; then
    echo "ERROR: required file missing: $f" >&2
    exit 1
  fi
done

echo "Post-merge: rebuilding search index..."
python3 scripts/build-search-index.py

echo "Post-merge: running full site auditor..."
python3 scripts/audit-site.py --quiet
if [ $? -ne 0 ]; then
  echo "ERROR: Site audit failed — stale or broken pages detected." >&2
  exit 1
fi

echo "Post-merge: running site validator and link checker..."
python3 scripts/validate-site.py
python3 scripts/check-links.py >/dev/null

echo "Post-merge: all checks passed."

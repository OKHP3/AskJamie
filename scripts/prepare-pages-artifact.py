#!/usr/bin/env python3
"""Prepare the exact public directory uploaded to GitHub Pages.

The repository is a static site, but it also contains scripts, tests, task
metadata, and CI configuration. This helper copies only deployable public
files into a clean directory so publishing cannot accidentally expose the
repository working surface.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "dist-pages"
PUBLIC_ROOT_FILES = {
    "404.html",
    "CNAME",
    "_headers",
    "favicon.ico",
    "humans.txt",
    "index.html",
    "llms.txt",
    "robots.txt",
    "sitemap.xml",
    "site.webmanifest",
    "under-construction.html",
}
PUBLIC_ROOT_DIRS = {"assets", ".well-known"}
PUBLIC_ASSET_DIRS = {"css", "data", "fonts", "img", "js", "vendor"}
PUBLIC_PAGE_DIRS = {
    "about",
    "contact",
    "legal",
    "lens-system",
    "search",
    "universe",
}


def is_public(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if not rel.parts:
        return False
    if rel.parts[0] in PUBLIC_PAGE_DIRS:
        return True
    if rel.parts[0] in PUBLIC_ROOT_DIRS:
        if rel.parts[0] != "assets":
            return True
        return len(rel.parts) > 1 and rel.parts[1] in PUBLIC_ASSET_DIRS
    if len(rel.parts) == 1 and rel.name in PUBLIC_ROOT_FILES:
        return True
    return False


def _digest_files(output: Path, copied: list[str]) -> str:
    digest = hashlib.sha256()
    for rel in copied:
        digest.update(rel.encode())
        digest.update((output / rel).read_bytes())
    return digest.hexdigest()


def prepare(output: Path) -> dict:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    copied = []
    for source in sorted(ROOT.rglob("*")):
        if source == output or output in source.parents or not is_public(source):
            continue
        if source.is_dir():
            continue
        target = output / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(source.relative_to(ROOT).as_posix())

    manifest = {
        "files": len(copied),
        "sha256": _digest_files(output, copied),
        "root_files": sorted(PUBLIC_ROOT_FILES),
        "asset_directories": sorted(PUBLIC_ASSET_DIRS),
    }
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    manifest = prepare(output)
    manifest_path = output.parent / f"{output.name}.manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"✓ Prepared {manifest['files']} public files in {output}")
    print(f"  SHA-256: {manifest['sha256']}")
    print(f"  Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

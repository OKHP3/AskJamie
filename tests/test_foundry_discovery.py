from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FoundryDiscoveryTests(unittest.TestCase):
    def test_foundry_is_linked_indexed_and_canonical(self):
        builder = load_script("build-search-index")

        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        how_it_works = (ROOT / "how-askjamie-works/index.html").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        foundry = (ROOT / "found-ry/index.html").read_text(encoding="utf-8")
        search_index = json.loads((ROOT / "assets/data/search-index.json").read_text(encoding="utf-8"))

        self.assertIn('href="/found-ry/"', homepage)
        self.assertIn('href="/found-ry/"', how_it_works)
        self.assertIn("https://askjamie.bot/found-ry/", llms)
        self.assertIn("<loc>https://askjamie.bot/found-ry/</loc>", sitemap)
        self.assertIn('<link rel="canonical" href="https://askjamie.bot/found-ry/" />', foundry)

        builder_pages = list(builder.collect_pages())
        self.assertTrue(any(page["url"] == "/found-ry/" for page in builder_pages))
        self.assertTrue(any(entry["url"] == "/found-ry/" for entry in search_index["entries"]))

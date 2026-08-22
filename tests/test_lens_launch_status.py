from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


LENS_CONTRACTS = {
    "AJ01": {
        "page": ROOT / "lens-system/resume-representative/index.html",
        "contact_id": "inquiry-paths-aj01",
        "name": "Résumé Representative",
        "url": "https://chatgpt.com/g/g-691fb05c86c881919eec171e62fe1e00-resume-representative-by-askjamietm",
    },
    "AJ02": {
        "page": ROOT / "lens-system/professional-portfolio/index.html",
        "contact_id": "inquiry-paths-aj02",
        "name": "Professional Portfolio",
        "url": "https://chatgpt.com/g/g-691fa5845230819199d4ffb89b13e9ab-professional-portfolio-by-askjamietm",
    },
    "AJ03": {
        "page": ROOT / "lens-system/enterprise-sleuth/index.html",
        "contact_id": "inquiry-paths-aj03",
        "name": "Enterprise Sleuth",
        "url": "https://chatgpt.com/g/g-691f9a52f5088191b4f552770ffb5886-enterprise-sleuth-by-askjamietm",
    },
}


def test_public_lens_pages_have_verified_chatgpt_links():
    contact = (ROOT / "contact/index.html").read_text(encoding="utf-8")

    for lens_id, contract in LENS_CONTRACTS.items():
        page = contract["page"].read_text(encoding="utf-8")
        contact_path = f"/contact/#{contract['contact_id']}"

        assert contract["url"].startswith("https://chatgpt.com/g/")
        assert contract["url"] in page
        assert f'href="{contract["url"]}"' in page
        assert "is in development" not in page
        assert f'id="{contract["contact_id"]}"' in contact
        assert contract["name"] in contact
        assert contract["url"] in contact
        assert "early access" not in page
        assert "early access" not in contact[contact.index(f'id="{contract["contact_id"]}"'):contact.index(f'id="{contract["contact_id"]}"') + 1200]


def test_lens_hub_labels_all_four_lenses():
    hub = (ROOT / "lens-system/index.html").read_text(encoding="utf-8")

    for lens_id, contract in LENS_CONTRACTS.items():
        assert f"GPT‑{lens_id} is live." in hub
        assert contract["url"] in hub
    assert '<strong class="site-status-eyebrow">Live</strong>' in hub
    assert "published BrandGuard GPT case studies" in hub
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


LENS_CONTRACTS = {
    "AJ01": {
        "page": ROOT / "lens-system/resume-representative/index.html",
        "contact_id": "inquiry-paths-aj01",
        "name": "Résumé Representative",
    },
    "AJ02": {
        "page": ROOT / "lens-system/professional-portfolio/index.html",
        "contact_id": "inquiry-paths-aj02",
        "name": "Professional Portfolio",
    },
    "AJ03": {
        "page": ROOT / "lens-system/enterprise-sleuth/index.html",
        "contact_id": "inquiry-paths-aj03",
        "name": "Enterprise Sleuth",
    },
}


def test_deferred_lens_pages_have_honest_status_and_inquiry_path():
    contact = (ROOT / "contact/index.html").read_text(encoding="utf-8")

    for lens_id, contract in LENS_CONTRACTS.items():
        page = contract["page"].read_text(encoding="utf-8")
        contact_path = f"/contact/#{contract['contact_id']}"

        assert "Coming soon" not in page, f"{lens_id} still has indefinite coming-soon copy"
        assert f"{lens_id} is in development" in page
        assert "no public launch date" in page
        assert contact_path in page
        assert f'id="{contract["contact_id"]}"' in contact
        assert contract["name"] in contact


def test_lens_hub_labels_all_four_lenses():
    hub = (ROOT / "lens-system/index.html").read_text(encoding="utf-8")

    for lens_id in LENS_CONTRACTS:
        assert f"GPT‑{lens_id} has no public launch date yet." in hub
    assert '<strong class="site-status-eyebrow">Live</strong>' in hub
    assert "published BrandGuard GPT case studies" in hub
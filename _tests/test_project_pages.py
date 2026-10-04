import pytest
from playwright.sync_api import expect

from conftest import banned_pattern, real_errors

PAGES = {
    "portfolio-agent": {"title": "포트폴리오 Agent", "demo": "live-chatbot"},
    "investment-agent": {"title": "투자 비서 Agent", "demo": "prototype"},
    "ai-companion-agent": {"title": "AI 컴패니언 Agent", "demo": "prototype"},
}

REQUIRED_SECTIONS = ["Overview", "Demo", "Key Features", "Architecture", "Challenges", "Tech Stack"]


@pytest.mark.parametrize("slug", list(PAGES))
def test_page_structure(page, console_errors, base_url, slug):
    spec = PAGES[slug]
    page.goto(f"{base_url}/projects/{slug}/")
    expect(page.locator(".project-hero h1")).to_have_text(spec["title"])
    headings = [h.strip() for h in page.locator(".project-body h2").all_inner_texts()]
    for section in REQUIRED_SECTIONS:
        assert section in headings, f"{slug}: '{section}' 섹션 없음"
    assert "Retrospective" not in headings
    expect(page.locator(".project-body .mermaid svg").first).to_be_visible(timeout=15000)
    assert "Syntax error" not in page.locator(".project-body").inner_text()
    expect(page.locator("#demo-slot .demo-block")).to_have_count(1)
    page.wait_for_load_state("networkidle")
    assert real_errors(console_errors) == []


@pytest.mark.parametrize("slug", [s for s, v in PAGES.items() if v["demo"] == "prototype"])
def test_prototype_embedded(page, base_url, slug):
    page.goto(f"{base_url}/projects/{slug}/")
    expect(page.locator("#demo-slot iframe.demo-frame")).to_have_attribute("src", f"/demos/{slug}/")
    expect(page.locator("#demo-slot .demo-bar a")).to_have_attribute("href", f"/demos/{slug}/")
    frame = page.frame_locator("#demo-slot iframe.demo-frame")
    expect(frame.locator(".preset").first).to_be_visible(timeout=10000)


def test_investment_storage_table(page, base_url):
    page.goto(f"{base_url}/projects/investment-agent/")
    headings = [h.strip() for h in page.locator(".project-body h2").all_inner_texts()]
    assert "Data & Storage" in headings
    table_text = page.locator(".project-body table").first.inner_text()
    for store in ["Elasticsearch", "Redis", "PostgreSQL", "GCS", "Neo4j", "InfluxDB"]:
        assert store in table_text


def test_companion_rendered_text_has_no_private_terms(page, base_url):
    pattern = banned_pattern()
    page.goto(f"{base_url}/projects/ai-companion-agent/")
    text = page.locator(".project-content").inner_text()
    assert not pattern.search(text)
    for keyword in ["Jev", "ComfyUI", "agent_work", "개인 비서", "MCP"]:
        assert keyword in text
    for roadmap_word in ["로드맵", "최종 목표", "향후"]:
        assert roadmap_word not in text


@pytest.mark.parametrize("slug", list(PAGES))
def test_share_description_uses_subtitle(page, base_url, slug):
    page.goto(f"{base_url}/projects/{slug}/")
    subtitle = page.locator(".project-subtitle").inner_text().strip()
    assert page.locator('meta[name="description"]').get_attribute("content") == subtitle
    assert page.locator('meta[property="og:description"]').get_attribute("content") == subtitle

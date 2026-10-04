import urllib.request

import pytest
from playwright.sync_api import expect

from conftest import real_errors

EXPECTED = {
    "AI 컴패니언 Agent": ["/projects/ai-companion-agent/", "/demos/ai-companion-agent/"],
    "투자 비서 Agent": ["/projects/investment-agent/", "/demos/investment-agent/"],
    "포트폴리오 Agent": ["/projects/portfolio-agent/", "/projects/portfolio-agent/#demo"],
}


def _side_items(page):
    return page.locator("#side-project + .card > .item")


def test_companion_card_is_first(page, base_url):
    page.goto(base_url + "/")
    expect(_side_items(page).first.locator(".role")).to_have_text("AI 컴패니언 Agent")


@pytest.mark.parametrize("role", list(EXPECTED))
def test_card_actions(page, base_url, role):
    page.goto(base_url + "/")
    item = _side_items(page).filter(has=page.locator(".role", has_text=role))
    expect(item).to_have_count(1)
    hrefs = [a.get_attribute("href") for a in item.locator(".project-actions a").all()]
    assert hrefs == EXPECTED[role]
    for href in hrefs:
        with urllib.request.urlopen(base_url + href.split("#")[0], timeout=10) as resp:
            assert resp.status == 200


def test_other_cards_have_no_actions(page, base_url):
    page.goto(base_url + "/")
    item = _side_items(page).filter(has=page.locator(".role", has_text="DSTC-9"))
    expect(item.locator(".project-actions")).to_have_count(0)


def test_demo_anchor_scrolls_to_demo(page, base_url):
    page.goto(base_url + "/projects/portfolio-agent/#demo")
    expect(page.locator("#demo-slot .demo-live")).to_be_in_viewport()


def test_index_no_console_errors(page, console_errors, base_url):
    page.goto(base_url + "/")
    page.wait_for_load_state("networkidle")
    assert real_errors(console_errors) == []


def test_companion_card_matches_other_cards_structure(page, base_url):
    page.goto(base_url + "/")
    item = _side_items(page).first
    assert item.locator("ul.list-tight > li > ul").count() >= 3
    text = item.inner_text()
    for keyword in ["Knowledge Graph", "MCP", "Jev", "ComfyUI"]:
        assert keyword in text
    assert "확장 중" not in text


SLUGS = {
    "AI 컴패니언 Agent": "ai-companion-agent",
    "투자 비서 Agent": "investment-agent",
    "포트폴리오 Agent": "portfolio-agent",
}


@pytest.mark.parametrize("role", list(SLUGS))
def test_card_keywords_match_detail_page(page, base_url, role):
    page.goto(base_url + "/")
    item = _side_items(page).filter(has=page.locator(".role", has_text=role))
    card = [t.strip() for t in item.locator(".pills em").all_inner_texts()]
    page.goto(f"{base_url}/projects/{SLUGS[role]}/")
    hero = [t.strip() for t in page.locator(".project-hero .pills em").all_inner_texts()]
    assert len(card) == 10
    assert len(set(card)) == 10
    assert card == hero


def test_companion_card_top_bullets_have_single_topic(page, base_url):
    page.goto(base_url + "/")
    tops = _side_items(page).first.locator("ul.list-tight > li")
    expect(tops).to_have_count(5)
    efficiency = tops.filter(has_text="LLM 판단 효율화")
    channels = tops.filter(has_text="멀티모달")
    expect(efficiency).to_have_count(1)
    expect(channels).to_have_count(1)
    assert "ComfyUI" not in efficiency.inner_text()
    assert "Jev" not in channels.inner_text()

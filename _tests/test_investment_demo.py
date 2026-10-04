import re

import pytest
from playwright.sync_api import expect

from conftest import real_errors

FAST = "/demos/investment-agent/?speed=40"
SLOW = "/demos/investment-agent/?speed=1"


def _play(page, idx: int) -> None:
    page.locator(".preset").nth(idx).click()
    expect(page.locator("body")).to_have_attribute("data-state", "done", timeout=20000)


def test_presets_render_idle(page, base_url):
    page.goto(base_url + FAST)
    expect(page.locator(".preset")).to_have_count(3)
    expect(page.locator("body")).to_have_attribute("data-state", "idle")
    expect(page.locator("#chat .empty")).to_have_count(1)


@pytest.mark.parametrize("idx", [0, 1, 2])
def test_scenario_plays_to_completion(page, base_url, idx):
    page.goto(base_url + FAST)
    _play(page, idx)
    chat = page.locator("#chat")
    expect(chat.locator(".msg-user")).to_have_count(1)
    assert chat.locator(".sys").count() >= 3
    expect(chat.locator(".card.plan")).to_have_count(1)
    assert chat.locator(".ledger").count() >= 3
    assert chat.locator(".ledger .result").count() >= 2
    assert chat.locator(".url").count() >= 3
    assert chat.locator(".chart svg polyline").count() >= 1
    answer = chat.locator(".answer")
    expect(answer).to_have_count(1)
    expect(answer).not_to_have_class(re.compile(r"\bstreaming\b"))
    assert answer.locator("h3").count() >= 1
    assert "**" not in answer.inner_text()


def test_dependency_check_is_visualized(page, base_url):
    page.goto(base_url + FAST)
    _play(page, 1)
    blocked = page.locator("#chat .ledger.blocked")
    expect(blocked).to_have_count(1)
    expect(blocked).to_contain_text("의존성")


def test_presets_disabled_while_running(page, base_url):
    page.goto(base_url + SLOW)
    page.locator(".preset").first.click()
    expect(page.locator("body")).to_have_attribute("data-state", "running")
    for i in range(3):
        expect(page.locator(".preset").nth(i)).to_be_disabled()


def test_double_click_plays_once(page, base_url):
    page.goto(base_url + FAST)
    page.locator(".preset").first.dblclick()
    expect(page.locator("body")).to_have_attribute("data-state", "done", timeout=20000)
    expect(page.locator("#chat .msg-user")).to_have_count(1)
    expect(page.locator("#chat .answer")).to_have_count(1)


def test_reset_cancels_playback(page, base_url):
    page.goto(base_url + SLOW)
    page.locator(".preset").first.click()
    expect(page.locator("#chat .msg-user")).to_have_count(1)
    page.locator("#reset").click()
    expect(page.locator("body")).to_have_attribute("data-state", "idle")
    page.wait_for_timeout(3000)
    expect(page.locator("#chat .msg-user")).to_have_count(0)
    expect(page.locator("#chat .sys")).to_have_count(0)
    expect(page.locator("#chat .empty")).to_have_count(1)
    for i in range(3):
        expect(page.locator(".preset").nth(i)).to_be_enabled()


def test_no_horizontal_scroll_at_360(browser, base_url):
    ctx = browser.new_context(viewport={"width": 360, "height": 740})
    pg = ctx.new_page()
    pg.goto(base_url + FAST)
    _play(pg, 0)
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    ctx.close()


def test_no_console_errors_and_no_api_calls(page, console_errors, base_url):
    requests: list[str] = []
    page.on("request", lambda r: requests.append(r.url))
    page.goto(base_url + FAST)
    _play(page, 0)
    assert real_errors(console_errors) == []
    assert all(u.startswith(base_url) or u.startswith("https://cdn.jsdelivr.net/") for u in requests), requests


@pytest.mark.parametrize("idx", [0, 1, 2])
def test_streaming_finishes_before_done(page, base_url, idx):
    page.goto(base_url + FAST)
    _play(page, idx)
    assert page.locator("#chat .streaming").count() == 0
    assert "실제와 무관합니다" in page.locator("#chat .answer").inner_text()


def test_stalled_marked_cdn_does_not_block_demo(page, base_url):
    page.route(re.compile(r".*marked.*"), lambda route: None)  # 응답하지 않는 CDN
    page.goto(base_url + FAST, wait_until="commit")
    expect(page.locator(".preset")).to_have_count(3, timeout=3000)

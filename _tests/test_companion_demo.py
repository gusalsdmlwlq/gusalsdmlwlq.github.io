import pytest
from playwright.sync_api import expect

from conftest import real_errors

FAST = "/demos/ai-companion-agent/?speed=40"
SLOW = "/demos/ai-companion-agent/?speed=1"


def _play(page, scenario: str) -> None:
    page.locator(f'.preset[data-scenario="{scenario}"]').click()
    expect(page.locator("body")).to_have_attribute("data-state", "done", timeout=20000)


def test_initial_state(page, base_url):
    page.goto(base_url + FAST)
    expect(page.locator(".preset")).to_have_count(4)
    expect(page.locator("body")).to_have_attribute("data-state", "idle")
    expect(page.locator("#emotion")).to_have_text("평온")
    expect(page.locator("#affection-value")).to_have_text("58")
    expect(page.locator("#flow")).to_have_text("대기 중")
    expect(page.locator("#logs .log")).to_have_count(0)


def test_recall_scenario(page, base_url):
    page.goto(base_url + FAST)
    _play(page, "recall")
    expect(page.locator("#chat .msg-user")).to_have_count(1)
    expect(page.locator("#chat .msg-ai")).to_have_count(1)
    assert page.locator("#memories .memory-card.highlight").count() >= 1
    assert page.locator("#logs .badge.jev").count() >= 2
    expect(page.locator("#emotion")).to_have_text("기쁨")
    expect(page.locator("#affection-value")).to_have_text("60")
    expect(page.locator("#flow")).to_have_text("대기 중")


def test_proactive_scenario(page, base_url):
    page.goto(base_url + FAST)
    _play(page, "proactive")
    expect(page.locator("#chat .msg-user")).to_have_count(0)
    expect(page.locator("#chat .jump")).to_have_count(1)
    expect(page.locator("#chat .msg-ai .channel")).to_contain_text("텔레그램")
    expect(page.locator("#clock")).to_contain_text("21:20")


def test_reminder_scenario(page, base_url):
    page.goto(base_url + FAST)
    _play(page, "reminder")
    expect(page.locator("#chat .msg-ai")).to_have_count(2)
    expect(page.locator("#reminders .reminder.done")).to_have_count(1)
    expect(page.locator("#chat .jump")).to_have_count(1)


def test_tool_scenario(page, base_url):
    page.goto(base_url + FAST)
    _play(page, "tool")
    expect(page.locator('#chat .tool-call[data-tool="investment_agent"]')).to_have_count(1)
    expect(page.locator('#chat .tool-call[data-tool="agent_work"]')).to_have_count(1)
    expect(page.locator("#chat .roadmap")).to_have_count(0)


def test_reset_restores_initial_state(page, base_url):
    page.goto(base_url + FAST)
    _play(page, "recall")
    page.locator("#reset").click()
    expect(page.locator("body")).to_have_attribute("data-state", "idle")
    expect(page.locator("#emotion")).to_have_text("평온")
    expect(page.locator("#affection-value")).to_have_text("58")
    expect(page.locator("#memories .memory-card")).to_have_count(0)
    expect(page.locator("#logs .log")).to_have_count(0)
    expect(page.locator("#chat .empty")).to_have_count(1)


def test_presets_disabled_while_running(page, base_url):
    page.goto(base_url + SLOW)
    page.locator('.preset[data-scenario="recall"]').click()
    expect(page.locator("body")).to_have_attribute("data-state", "running")
    for i in range(4):
        expect(page.locator(".preset").nth(i)).to_be_disabled()


def test_double_click_plays_once(page, base_url):
    page.goto(base_url + FAST)
    page.locator('.preset[data-scenario="recall"]').dblclick()
    expect(page.locator("body")).to_have_attribute("data-state", "done", timeout=20000)
    expect(page.locator("#chat .msg-user")).to_have_count(1)
    expect(page.locator("#chat .msg-ai")).to_have_count(1)


def test_reset_cancels_playback(page, base_url):
    page.goto(base_url + SLOW)
    page.locator('.preset[data-scenario="recall"]').click()
    expect(page.locator("#chat .msg-user")).to_have_count(1)
    page.locator("#reset").click()
    page.wait_for_timeout(3000)
    expect(page.locator("#chat .msg-user")).to_have_count(0)
    expect(page.locator("#logs .log")).to_have_count(0)
    expect(page.locator("#emotion")).to_have_text("평온")


@pytest.mark.parametrize("scenario", ["recall", "tool"])
def test_no_horizontal_scroll_at_360(browser, base_url, scenario):
    ctx = browser.new_context(viewport={"width": 360, "height": 740})
    pg = ctx.new_page()
    pg.goto(base_url + FAST)
    _play(pg, scenario)
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    ctx.close()


def test_no_console_errors_and_no_external_calls(page, console_errors, base_url):
    requests: list[str] = []
    page.on("request", lambda r: requests.append(r.url))
    page.goto(base_url + FAST)
    _play(page, "tool")
    assert real_errors(console_errors) == []
    assert all(u.startswith(base_url) for u in requests), requests


@pytest.mark.parametrize("scenario", ["recall", "proactive", "reminder", "tool"])
def test_streaming_finishes_before_done(page, base_url, scenario):
    page.goto(base_url + FAST)
    _play(page, scenario)
    assert page.locator("#chat .streaming").count() == 0
    last = page.locator("#chat > *").last
    if scenario == "tool":
        assert "msg-ai" in last.get_attribute("class")
        assert page.locator("#chat .msg-ai").last.inner_text().strip().endswith("(데모용 예시 요약이야)")

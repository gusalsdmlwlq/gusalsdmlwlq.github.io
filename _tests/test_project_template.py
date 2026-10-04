import re

from playwright.sync_api import expect

from conftest import real_errors

URL = "/projects/portfolio-agent/"


def test_hero_and_back_link(page, base_url):
    page.goto(base_url + URL)
    expect(page.locator(".project-hero h1")).to_have_text("포트폴리오 Agent")
    assert page.locator(".project-hero .pills em").count() >= 5
    expect(page.locator("a.back-link")).to_have_attribute("href", "/#side-project")


def test_toc_lists_every_h2_with_unique_ids(page, base_url):
    page.goto(base_url + URL)
    headings = page.locator(".project-body h2")
    links = page.locator("#project-toc a.toc-link")
    assert headings.count() >= 6
    expect(links).to_have_count(headings.count())
    ids = [headings.nth(i).get_attribute("id") for i in range(headings.count())]
    assert all(ids) and len(set(ids)) == len(ids)
    for i, hid in enumerate(ids):
        assert links.nth(i).get_attribute("href") == f"#{hid}"


def test_scroll_spy_marks_current_section(page, base_url):
    page.goto(base_url + URL)
    page.evaluate("document.getElementById('challenges').scrollIntoView({block: 'start'})")
    expect(page.locator('#project-toc a[href="#challenges"]')).to_have_class(re.compile(r"\bactive\b"))
    assert page.locator("#project-toc a.toc-link.active").count() == 1


def test_mermaid_rendered(page, base_url):
    page.goto(base_url + URL)
    expect(page.locator(".project-body .mermaid svg").first).to_be_visible(timeout=15000)
    assert page.locator(".project-body .language-mermaid").count() == 0
    assert "Syntax error" not in page.locator(".project-body").inner_text()


def test_mermaid_cdn_failure_keeps_code_and_toc(page, base_url):
    page.route(re.compile(r".*mermaid.*\.js.*"), lambda route: route.abort())
    page.goto(base_url + URL)
    expect(page.locator("#project-toc a.toc-link").first).to_be_visible()
    expect(page.locator("#demo-slot .demo-live")).to_have_count(1)
    assert "flowchart" in page.locator(".project-body").inner_text()


def test_live_chatbot_demo_block(page, base_url):
    page.goto(base_url + URL)
    expect(page.locator("#demo-slot .demo-live")).to_have_count(1)
    assert page.locator("#demo-slot .demo-question").count() == 3


def test_open_chat_before_widget_ready(page, base_url):
    page.goto(base_url + URL, wait_until="domcontentloaded")
    page.locator("#demo-slot .demo-open-chat").click()
    expect(page.locator("#pm-chat-popup")).to_have_class(re.compile(r"\bpm-open\b"))


def test_question_fills_chat_input_without_sending(page, base_url):
    requests: list[str] = []
    page.on("request", lambda r: requests.append(r.url))
    page.goto(base_url + URL)
    chip = page.locator("#demo-slot .demo-question").first
    question = chip.get_attribute("data-question")
    chip.click()
    expect(page.locator("#pm-chat-popup")).to_have_class(re.compile(r"\bpm-open\b"))
    expect(page.locator("#pm-chat-input")).to_have_value(question)
    assert not any("portfolio.jhm9507.com" in u for u in requests)


def test_narrow_layout_moves_toc_above_content(browser, base_url):
    ctx = browser.new_context(viewport={"width": 800, "height": 900})
    pg = ctx.new_page()
    pg.goto(base_url + URL)
    toc = pg.locator("aside.toc").bounding_box()
    body = pg.locator(".project-content").bounding_box()
    assert toc["y"] + toc["height"] <= body["y"] + 1
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    ctx.close()


def test_no_console_errors(page, console_errors, base_url):
    page.goto(base_url + URL)
    page.wait_for_load_state("networkidle")
    assert real_errors(console_errors) == []


def test_stalled_mermaid_does_not_block_toc_demo_or_chat(page, base_url):
    page.route(re.compile(r".*mermaid.*\.js.*"), lambda route: None)  # 응답하지 않는 CDN
    page.goto(base_url + URL, wait_until="commit")
    expect(page.locator("#project-toc a.toc-link").first).to_be_visible(timeout=3000)
    expect(page.locator("#demo-slot .demo-live")).to_have_count(1, timeout=3000)
    expect(page.locator("#pm-chat-fab")).to_be_attached(timeout=3000)


def test_mermaid_keeps_readable_size_on_narrow_screen(browser, base_url):
    ctx = browser.new_context(viewport={"width": 360, "height": 740})
    pg = ctx.new_page()
    pg.goto(base_url + URL)
    svg = pg.locator(".project-body .mermaid svg").first
    expect(svg).to_be_visible(timeout=15000)
    scale = pg.evaluate("""() => {
        const s = document.querySelector('.project-body .mermaid svg');
        return s.getBoundingClientRect().width / s.viewBox.baseVal.width;
    }""")
    assert scale > 0.9, scale
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    ctx.close()

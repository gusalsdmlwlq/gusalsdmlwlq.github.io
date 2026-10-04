import os
import re
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("SITE_BASE_URL", "http://localhost:4000").rstrip("/")


BANNED_TERMS_FILE = Path(__file__).with_name(".banned_terms")  # gitignore 대상 — 저장소에 커밋하지 않는다


def banned_pattern() -> re.Pattern:
    """공개 범위 금지어 정규식. 금지어 목록은 로컬 전용 파일에만 두고, 없으면 테스트를 skip한다."""
    if not BANNED_TERMS_FILE.exists():
        pytest.skip("_tests/.banned_terms 없음 (로컬 전용 파일)")
    terms = [
        t.strip()
        for t in BANNED_TERMS_FILE.read_text(encoding="utf-8").splitlines()
        if t.strip() and not t.strip().startswith("#")
    ]
    return re.compile("|".join(re.escape(t) for t in terms), re.IGNORECASE)


def real_errors(errors: list[str]) -> list[str]:
    """브라우저가 자동 요청하는 favicon 404처럼 페이지와 무관한 오류를 뺀다."""
    return [e for e in errors if "favicon" not in e]


def _server_up() -> bool:
    try:
        with urllib.request.urlopen(BASE_URL + "/", timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


@pytest.fixture(scope="session")
def base_url() -> str:
    if not _server_up():
        pytest.fail(f"Jekyll 서버가 {BASE_URL}에서 응답하지 않습니다. SITE에서 `docker compose up -d`를 먼저 실행하세요.")
    return BASE_URL


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        yield b
        b.close()


@pytest.fixture
def context(browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    yield ctx
    ctx.close()


@pytest.fixture
def console_errors() -> list[str]:
    return []


@pytest.fixture
def page(context, console_errors):
    pg = context.new_page()
    pg.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    pg.on("pageerror", lambda exc: console_errors.append(str(exc)))
    return pg

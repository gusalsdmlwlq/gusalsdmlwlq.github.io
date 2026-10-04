import urllib.request

import pytest

ROUTES = ["/", "/projects/portfolio-agent/", "/demos/investment-agent/", "/projects/investment-agent/", "/demos/ai-companion-agent/", "/projects/ai-companion-agent/"]


@pytest.mark.parametrize("path", ROUTES)
def test_route_ok(base_url, path):
    with urllib.request.urlopen(base_url + path, timeout=10) as resp:
        assert resp.status == 200

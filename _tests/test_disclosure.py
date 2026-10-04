import subprocess
from pathlib import Path

from conftest import banned_pattern

ROOT = Path(__file__).resolve().parents[1]


def _tracked_text_files() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [p.decode("utf-8") for p in out.split(b"\0") if p]


def test_tracked_files_have_no_banned_terms():
    pattern = banned_pattern()
    hits: dict[str, list[str]] = {}
    for rel in _tracked_text_files():
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        found = sorted({m.group(0) for m in pattern.finditer(text)})
        if found:
            hits[rel] = found
    assert hits == {}, hits

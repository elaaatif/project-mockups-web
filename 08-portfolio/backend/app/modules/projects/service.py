"""Projects + a live status probe that checks whether each demo's API is running locally."""
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen

from app.modules.projects.models import projects


def _is_up(port: int) -> bool:
    try:
        with urlopen(f"http://127.0.0.1:{port}/api/health", timeout=0.6) as r:
            return r.status == 200
    except OSError:
        return False


def status() -> dict[str, bool]:
    rows = projects.all()
    with ThreadPoolExecutor(max_workers=len(rows)) as pool:
        results = pool.map(lambda p: _is_up(p["api_port"]), rows)
    return {p["slug"]: up for p, up in zip(rows, results)}


def detail(slug: str) -> dict:
    p = projects.get_or_404(slug)
    i = projects.all().index(p)
    nxt = projects.all()[(i + 1) % len(projects.all())]
    return p | {"next": {"slug": nxt["slug"], "title": nxt["title"]}}

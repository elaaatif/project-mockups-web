"""Internal CRM: one inbox for quote requests, contact messages and job applications."""
from collections import Counter

from app.core.common import rng
from app.modules.careers.models import applications
from app.modules.company.models import messages
from app.modules.quotes.models import rfqs

_TRAFFIC = [round(1800 + i * 45 + rng.uniform(-250, 300)) for i in range(30)]


def overview() -> dict:
    leads = rfqs.all()
    open_leads = [r for r in leads if r["stage"] not in ("won", "lost")]
    won = [r for r in leads if r["stage"] == "won"]
    sources = Counter(r["source"] for r in leads)
    return {
        "kpis": {"rfqs": len(leads), "hot": sum(1 for r in leads if r["priority"] == "hot"),
                 "pipeline": sum(r["value"] for r in open_leads), "won_value": sum(r["value"] for r in won),
                 "messages": sum(1 for m in messages.all() if m["status"] == "new"),
                 "applications": sum(1 for a in applications.all() if a["status"] == "new"),
                 "conversion": round(sum(_TRAFFIC[-7:]) and len(leads) / sum(_TRAFFIC[-7:]) * 100, 2)},
        "traffic": {"labels": [f"D{i + 1}" for i in range(30)], "visits": _TRAFFIC, "leads": [max(0, round(v / 400 + rng.uniform(-2, 2))) for v in _TRAFFIC]},
        "sources": {"labels": list(sources), "values": list(sources.values())},
    }


def update(repo, key, fields: dict) -> dict:
    row = repo.get_or_404(key)
    row.update({k: v for k, v in fields.items() if v is not None})
    return row

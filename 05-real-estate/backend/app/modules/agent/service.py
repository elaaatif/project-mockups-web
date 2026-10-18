"""Agent dashboard: pipeline, appointments and performance."""
from app.core.common import TODAY, rng
from app.modules.leads.models import STAGES, leads, viewings
from app.modules.listings.models import agents, properties

_MONTHLY = [rng.randint(6, 18) for _ in range(12)]


def overview() -> dict:
    active = [l for l in leads.all() if l["stage"] not in ("won", "lost")]
    won = [l for l in leads.all() if l["stage"] == "won"]
    sale_value = sum(p["price"] for p in properties.all() if p["purpose"] == "sale" and p["status"] == "available")
    return {
        "kpis": {"active_leads": len(active), "viewings_week": len(viewings.all()), "pipeline_value": sum(l["budget"] for l in active if l["purpose"] == "sale"),
                 "conversion": round(len(won) / max(1, len(leads.all())) * 100), "listings": len(properties.all()), "stock_value": sale_value},
        "deals_by_month": {"labels": ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"], "values": _MONTHLY},
        "sources": _count("source"),
        "top_listings": sorted(properties.all(), key=lambda p: -p["views"])[:5],
    }


def _count(field: str) -> dict:
    counts: dict[str, int] = {}
    for l in leads.all():
        counts[l[field]] = counts.get(l[field], 0) + 1
    return {"labels": list(counts), "values": list(counts.values())}


def pipeline() -> dict:
    agent_names = {a["id"]: a["name"] for a in agents.all()}
    return {"stages": STAGES, "leads": [l | {"agent": agent_names.get(l["agent_id"])} for l in leads.all()]}


def move(lead_id: int, stage: str) -> dict:
    lead = leads.get_or_404(lead_id)
    lead["stage"] = stage
    return lead


def appointments() -> list[dict]:
    today = TODAY.isoformat()
    return sorted([v for v in viewings.all() if v["date"] >= today], key=lambda v: (v["date"], v["time"]))

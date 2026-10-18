from fastapi import HTTPException

from app.core.common import days
from app.modules.contact.models import ADDONS, PROJECT_TYPES, EstimateIn, MessageIn, messages


def estimate(data: EstimateIn) -> dict:
    if data.project_type not in PROJECT_TYPES:
        raise HTTPException(400, "Unknown project type")
    label, price, weeks = PROJECT_TYPES[data.project_type]
    picked = [ADDONS[a] for a in data.addons if a in ADDONS]
    price += sum(p for _, p, _ in picked)
    weeks += sum(w for _, _, w in picked)
    if data.urgency == "fast":
        price, weeks = price * 1.25, max(1, round(weeks * 0.7))
    return {"label": label, "addons": [n for n, _, _ in picked], "low": round(price * 0.9, -2), "high": round(price * 1.2, -2),
            "weeks": weeks, "monthly_care": 149 if price < 5000 else 290}


def options() -> dict:
    return {"types": [{"key": k, "label": v[0], "from": v[1]} for k, v in PROJECT_TYPES.items()],
            "addons": [{"key": k, "label": v[0], "price": v[1]} for k, v in ADDONS.items()]}


def send(data: MessageIn) -> dict:
    m = messages.add({"id": len(messages.rows) + 1, **data.model_dump(), "created": days(0), "status": "new"})
    return {"id": m["id"], "ok": True}


def set_status(message_id: int, status: str) -> dict:
    m = messages.get_or_404(message_id)
    m["status"] = status
    return m

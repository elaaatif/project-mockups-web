"""Business-owner dashboard: KPIs, day schedule per staff member and booking list."""
from datetime import date, timedelta

from app.modules.bookings.models import bookings
from app.modules.businesses.models import businesses
from app.modules.businesses.service import to_minutes


def overview(slug: str, day: str | None = None) -> dict:
    b = businesses.get_or_404(slug)
    day = day or date.today().isoformat()
    mine = [x for x in bookings.all() if x["business_slug"] == slug]
    today = [x for x in mine if x["date"] == day and x["status"] != "cancelled"]
    week_start = (date.fromisoformat(day) - timedelta(days=6)).isoformat()
    past_week = [x for x in mine if week_start <= x["date"] <= day and x["status"] in ("completed", "confirmed", "checked_in")]
    finished = [x for x in mine if x["status"] in ("completed", "no_show")]
    open_minutes = (to_minutes(b["close"]) - to_minutes(b["open"])) * len(b["staff"])
    trend = []
    for i in range(13, -1, -1):
        d = (date.fromisoformat(day) - timedelta(days=i - 7)).isoformat()
        trend.append({"date": d, "count": sum(1 for x in mine if x["date"] == d and x["status"] != "cancelled")})
    return {
        "business": {k: b[k] for k in ("slug", "name", "kind", "open", "close", "image")} | {"staff": b["staff"], "services": b["services"]},
        "date": day,
        "kpis": {"today": len(today), "revenue_week": sum(x["price"] for x in past_week),
                 "occupancy": round(sum(x["minutes"] for x in today) / open_minutes * 100) if open_minutes else 0,
                 "no_show_rate": round(sum(1 for x in finished if x["status"] == "no_show") / len(finished) * 100, 1) if finished else 0},
        "schedule": sorted(today, key=lambda x: x["time"]),
        "trend": trend,
    }


def list_bookings(slug: str, status: str | None = None) -> list[dict]:
    rows = [x for x in bookings.all() if x["business_slug"] == slug and (not status or x["status"] == status)]
    return sorted(rows, key=lambda x: (x["date"], x["time"]), reverse=True)[:120]

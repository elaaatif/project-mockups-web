"""Business directory + slot availability engine."""
from datetime import date, datetime, timedelta

from fastapi import HTTPException

from app.modules.bookings.models import bookings
from app.modules.businesses.models import businesses


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def to_hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def summary(b: dict) -> dict:
    return {k: b[k] for k in ("slug", "name", "category", "kind", "image", "area", "rating", "reviews", "open", "close")} | {
        "from_price": min((s["price"] for s in b["services"] if s["price"]), default=0), "services_count": len(b["services"])}


def list_businesses(category: str | None = None, q: str | None = None) -> list[dict]:
    rows = businesses.all()
    if category:
        rows = [b for b in rows if b["category"] == category]
    if q:
        rows = [b for b in rows if q.lower() in (b["name"] + b["area"] + " ".join(s["name"] for s in b["services"])).lower()]
    return [summary(b) for b in rows]


def service_of(b: dict, service_id: int) -> dict:
    s = next((s for s in b["services"] if s["id"] == service_id), None)
    if not s:
        raise HTTPException(404, "Service not found")
    return s


def is_free(slug: str, staff_id: int, day: str, start: int, minutes: int, ignore_code: str | None = None) -> bool:
    for bk in bookings.all():
        if bk["business_slug"] != slug or bk["staff_id"] != staff_id or bk["date"] != day or bk["status"] == "cancelled" or bk["code"] == ignore_code:
            continue
        b_start = to_minutes(bk["time"])
        if start < b_start + bk["minutes"] and b_start < start + minutes:
            return False
    return True


def eligible_staff(b: dict, party_size: int) -> list[dict]:
    if b["kind"] == "table":
        return [s for s in b["staff"] if (s["max_party"] or 0) >= party_size]
    return b["staff"]


def availability(slug: str, service_id: int, day: str, staff_id: int | None = None, party_size: int = 2) -> dict:
    b = businesses.get_or_404(slug)
    svc = service_of(b, service_id)
    target = date.fromisoformat(day)
    if target < date.today():
        raise HTTPException(400, "Pick today or a future date")
    staff = [s for s in eligible_staff(b, party_size) if staff_id in (None, s["id"])]
    open_m, close_m = to_minutes(b["open"]), to_minutes(b["close"])
    now_m = datetime.now().hour * 60 + datetime.now().minute if target == date.today() else -1
    slots = []
    for start in range(open_m, close_m - svc["minutes"] + 1, b["slot_minutes"]):
        if start <= now_m + 30:
            continue
        free = [s["id"] for s in staff if is_free(slug, s["id"], day, start, svc["minutes"])]
        slots.append({"time": to_hhmm(start), "staff_ids": free, "available": bool(free)})
    return {"date": day, "service": svc, "slots": slots, "staff": staff}


def week_days(n: int = 14) -> list[dict]:
    today = date.today()
    return [{"date": (today + timedelta(days=i)).isoformat(), "weekday": (today + timedelta(days=i)).strftime("%a"),
             "day": (today + timedelta(days=i)).day} for i in range(n)]

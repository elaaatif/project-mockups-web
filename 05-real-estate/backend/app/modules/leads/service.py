"""Lead generation: enquiries, viewing bookings and instant valuations all become CRM leads."""
from datetime import date

from fastapi import HTTPException

from app.core.common import days
from app.modules.leads.models import VIEWING_TIMES, EnquiryIn, ValuationIn, ViewingIn, leads, viewings
from app.modules.listings.models import DISTRICTS
from app.modules.listings.service import by_id

TYPE_FACTOR = {"apartment": 1.0, "house": 1.08, "penthouse": 1.25, "villa": 1.18}
CONDITION_FACTOR = {"needs_work": 0.86, "good": 1.0, "excellent": 1.1}


def _add_lead(name, email, phone, source, prop: dict | None, message="", budget=None, score=60) -> dict:
    return leads.add({
        "id": max((x["id"] for x in leads.all()), default=0) + 1, "name": name, "email": email, "phone": phone, "source": source,
        "property_id": prop["id"] if prop else None, "property_title": prop["title"] if prop else "Valuation",
        "budget": budget or (prop["price"] if prop else 0), "purpose": prop["purpose"] if prop else "sale",
        "agent_id": prop["agent_id"] if prop else 1, "stage": "new", "score": score, "created": days(0), "message": message,
    })


def enquire(data: EnquiryIn) -> dict:
    prop = by_id(data.property_id) if data.property_id else None
    return _add_lead(data.name, data.email, data.phone, "Website enquiry", prop, data.message, score=72)


def free_slots(property_id: int, day: str) -> list[dict]:
    p = by_id(property_id)
    if date.fromisoformat(day).weekday() == 6:
        return []  # no viewings on Sundays
    taken = {v["time"] for v in viewings.all() if v["date"] == day and v["agent_id"] == p["agent_id"] and v["status"] != "cancelled"}
    return [{"time": t, "available": t not in taken} for t in VIEWING_TIMES]


def book_viewing(data: ViewingIn) -> dict:
    p = by_id(data.property_id)
    if not any(s["time"] == data.time and s["available"] for s in free_slots(data.property_id, data.date)):
        raise HTTPException(409, "That viewing slot is no longer available")
    v = viewings.add({"id": len(viewings.rows) + 1, "property_id": p["id"], "property_title": p["title"], "address": p["address"],
                      "agent_id": p["agent_id"], "date": data.date, "time": data.time, "name": data.name, "email": data.email,
                      "phone": data.phone, "status": "confirmed"})
    lead = _add_lead(data.name, data.email, data.phone, "Viewing request", p, f"Viewing booked {data.date} {data.time}", score=88)
    lead["stage"] = "viewing"
    return v


def valuation(data: ValuationIn) -> dict:
    if data.district not in DISTRICTS:
        raise HTTPException(400, "Unknown district")
    per_sqm = DISTRICTS[data.district][0] * TYPE_FACTOR[data.type] * CONDITION_FACTOR[data.condition]
    estimate = round(per_sqm * data.area_sqm, -3)
    _add_lead(data.name, data.email, data.phone, "Valuation request", None, f"{data.beds}-bed {data.type} in {data.district}, {data.area_sqm} m²",
              budget=estimate, score=91)
    return {"estimate": estimate, "low": round(estimate * 0.93, -3), "high": round(estimate * 1.07, -3),
            "per_sqm": round(per_sqm), "rent_estimate": round(estimate * 0.035 / 12, -1), "district_avg_per_sqm": DISTRICTS[data.district][0]}

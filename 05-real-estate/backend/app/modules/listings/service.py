from fastapi import HTTPException

from app.modules.listings.models import agents, properties

SORTS = {"newest": lambda p: p["listed_days"], "price_asc": lambda p: p["price"], "price_desc": lambda p: -p["price"],
         "featured": lambda p: (not p["featured"], p["listed_days"])}


def search(purpose: str | None = None, type: str | None = None, district: str | None = None, min_beds: int = 0,
           max_price: int | None = None, q: str | None = None, sort: str = "featured") -> list[dict]:
    rows = properties.all()
    if purpose:
        rows = [p for p in rows if p["purpose"] == purpose]
    if type:
        rows = [p for p in rows if p["type"] == type]
    if district:
        rows = [p for p in rows if p["district"] == district]
    if min_beds:
        rows = [p for p in rows if p["beds"] >= min_beds]
    if max_price:
        rows = [p for p in rows if p["price"] <= max_price]
    if q:
        rows = [p for p in rows if q.lower() in (p["title"] + p["address"]).lower()]
    return sorted(rows, key=SORTS.get(sort, SORTS["featured"]))


def by_id(property_id: int) -> dict:
    p = next((p for p in properties.all() if p["id"] == property_id), None)
    if not p:
        raise HTTPException(404, "Property not found")
    return p


def detail(slug: str) -> dict:
    p = properties.get_or_404(slug)
    p["views"] += 1
    similar = [s for s in properties.all() if s["purpose"] == p["purpose"] and s["slug"] != slug][:3]
    return {**p, "agent": agents.get(p["agent_id"]), "similar": similar,
            "price_per_sqm": round(p["price"] / p["area_sqm"]) if p["purpose"] == "sale" else None}

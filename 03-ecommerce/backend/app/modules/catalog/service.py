from fastapi import HTTPException

from app.modules.catalog.models import WHOLESALE_TIERS, products

SORTS = {
    "featured": lambda p: (p["badge"] is None, -p["reviews"]),
    "price_asc": lambda p: p["price"],
    "price_desc": lambda p: -p["price"],
    "rating": lambda p: -p["rating"],
}


def tiers_for(product: dict) -> list[dict]:
    return [{"min_qty": q, "discount": d, "unit_price": round(product["price"] * (1 - d), 2)} for q, d in WHOLESALE_TIERS]


def unit_price(product: dict, qty: int, wholesale: bool = False) -> float:
    if not wholesale:
        return product["price"]
    discount = max((d for q, d in WHOLESALE_TIERS if qty >= q), default=0)
    return round(product["price"] * (1 - discount), 2)


def list_products(q: str | None = None, category: str | None = None, sort: str = "featured",
                  max_price: float | None = None, in_stock: bool = False) -> list[dict]:
    rows = products.all()
    if q:
        rows = [p for p in rows if q.lower() in (p["name"] + p["description"]).lower()]
    if category:
        rows = [p for p in rows if p["category"] == category]
    if max_price:
        rows = [p for p in rows if p["price"] <= max_price]
    if in_stock:
        rows = [p for p in rows if p["stock"] > 0]
    return sorted(rows, key=SORTS.get(sort, SORTS["featured"]))


def detail(slug: str) -> dict:
    p = products.get_or_404(slug)
    related = [r for r in products.all() if r["category"] == p["category"] and r["slug"] != slug][:4]
    return {**p, "tiers": tiers_for(p), "related": related}


def by_id(product_id: int) -> dict:
    p = next((p for p in products.all() if p["id"] == product_id), None)
    if not p:
        raise HTTPException(404, f"Product {product_id} not found")
    return p

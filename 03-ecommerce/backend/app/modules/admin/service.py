"""Store admin dashboard — aggregates catalog, orders and quotes."""
from collections import Counter

from app.core.common import rng
from app.modules.catalog.models import products
from app.modules.orders.models import orders
from app.modules.quotes.models import quotes

_DAILY = [round(2400 + i * 120 + rng.uniform(-700, 900)) for i in range(14)]


def overview() -> dict:
    all_orders = orders.all()
    revenue = sum(o["total"] for o in all_orders)
    sold = Counter()
    for o in all_orders:
        for line in o["items"]:
            sold[line["name"]] += line["qty"]
    return {
        "kpis": {"revenue": round(revenue, 2), "orders": len(all_orders), "aov": round(revenue / len(all_orders), 2),
                 "open_quotes": sum(1 for q in quotes.all() if q["status"] == "new"),
                 "low_stock": sum(1 for p in products.all() if p["stock"] < 15)},
        "daily": {"labels": [f"Day {i + 1}" for i in range(14)], "values": _DAILY},
        "channels": {"labels": ["Retail", "Wholesale"], "values": [sum(1 for o in all_orders if o["channel"] == c) for c in ("retail", "wholesale")]},
        "top_products": [{"name": n, "qty": q} for n, q in sold.most_common(5)],
    }


def inventory() -> list[dict]:
    return sorted(products.all(), key=lambda p: p["stock"])


def restock(slug: str, qty: int) -> dict:
    p = products.get_or_404(slug)
    p["stock"] += qty
    return p

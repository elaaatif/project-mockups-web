from fastapi import HTTPException

from app.core.common import days, rng
from app.modules.catalog import service as catalog
from app.modules.orders.models import FREE_SHIPPING_OVER, SHIPPING, STAGE_LABELS, STAGES, TAX_RATE, OrderIn, orders


def present(order: dict) -> dict:
    timeline = [{"key": s, "label": STAGE_LABELS[s], "done": i <= order["stage"],
                 "at": order["history"][i] if i < len(order["history"]) else None} for i, s in enumerate(STAGES)]
    return {**order, "status": STAGES[order["stage"]], "timeline": timeline}


def build_lines(items, wholesale: bool = False) -> list[dict]:
    lines = []
    for line in items:
        p = catalog.by_id(line.product_id)
        if p["stock"] < line.qty:
            raise HTTPException(409, f"Only {p['stock']} × {p['name']} left in stock")
        lines.append({"product_id": p["id"], "name": p["name"], "image": p["image"], "qty": line.qty,
                      "unit_price": catalog.unit_price(p, line.qty, wholesale)})
    return lines


def reserve_stock(lines: list[dict]) -> None:
    for line in lines:
        catalog.by_id(line["product_id"])["stock"] -= line["qty"]


def create(data: OrderIn) -> dict:
    lines = build_lines(data.items)
    subtotal = round(sum(x["qty"] * x["unit_price"] for x in lines), 2)
    shipping = 0 if subtotal >= FREE_SHIPPING_OVER and data.shipping == "standard" else SHIPPING[data.shipping]
    reserve_stock(lines)
    order = {
        "id": f"MC-{48210 + len(orders.rows)}", "channel": "retail", "customer": data.customer.model_dump(), "items": lines,
        "subtotal": subtotal, "shipping_cost": shipping, "tax": round(subtotal * TAX_RATE / (1 + TAX_RATE), 2),
        "total": round(subtotal + shipping, 2), "shipping": data.shipping, "payment": data.payment,
        "stage": 0 if data.payment == "cod" else 1, "created": days(0), "history": [days(0)] * (1 if data.payment == "cod" else 2),
        "carrier": "DHL Express" if data.shipping == "express" else "Royal Mail", "tracking_no": f"JD0146{rng.randint(10000000, 99999999)}",
    }
    return present(orders.add(order))


def track(order_id: str, email: str) -> dict:
    order = orders.get(order_id.strip().upper())
    if not order or order["customer"]["email"].lower() != email.strip().lower():
        raise HTTPException(404, "No order matches that number and email")
    return present(order)


def list_orders() -> list[dict]:
    return [present(o) for o in orders.all()]


def advance(order_id: str) -> dict:
    order = orders.get_or_404(order_id)
    if order["stage"] >= len(STAGES) - 1:
        raise HTTPException(400, "Order already delivered")
    order["stage"] += 1
    order["history"].append(days(0))
    return present(order)

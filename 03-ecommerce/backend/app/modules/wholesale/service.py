from fastapi import HTTPException

from app.core.common import days
from app.modules.catalog import service as catalog
from app.modules.catalog.models import products
from app.modules.orders import service as orders_service
from app.modules.orders.models import orders
from app.modules.wholesale.models import MIN_ORDER_VALUE, PAYMENT_TERMS, WholesaleOrderIn


def price_list() -> dict:
    rows = [{k: p[k] for k in ("id", "sku", "name", "category", "price", "stock", "image", "moq_wholesale")} | {"tiers": catalog.tiers_for(p)}
            for p in products.all()]
    return {"products": rows, "min_order_value": MIN_ORDER_VALUE, "payment_terms": PAYMENT_TERMS}


def place(data: WholesaleOrderIn) -> dict:
    for line in data.items:
        if line.qty < catalog.by_id(line.product_id)["moq_wholesale"]:
            raise HTTPException(400, "Each wholesale line needs at least 10 units")
    lines = orders_service.build_lines(data.items, wholesale=True)
    subtotal = round(sum(x["qty"] * x["unit_price"] for x in lines), 2)
    if subtotal < MIN_ORDER_VALUE:
        raise HTTPException(400, f"Minimum wholesale order is ${MIN_ORDER_VALUE}")
    retail = sum(x["qty"] * catalog.by_id(x["product_id"])["price"] for x in lines)
    orders_service.reserve_stock(lines)
    order = orders.add({
        "id": f"WS-{9100 + len(orders.rows)}", "channel": "wholesale", "items": lines,
        "customer": {"name": data.company, "email": data.email, "address": data.vat_number, "city": "", "country": ""},
        "subtotal": subtotal, "shipping_cost": 0, "tax": 0, "total": subtotal, "shipping": "freight", "payment": PAYMENT_TERMS,
        "po_reference": data.po_reference, "stage": 0, "created": days(0), "history": [days(0)], "carrier": "Pallet freight", "tracking_no": "—",
    })
    return {**orders_service.present(order), "savings": round(retail - subtotal, 2), "due_date": days(30)}

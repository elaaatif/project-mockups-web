from fastapi import HTTPException

from app.core.common import days
from app.modules.inventory import service as inventory
from app.modules.inventory.models import items
from app.modules.purchasing.models import FLOW, PoIn, orders


def suggestions() -> list[dict]:
    return [{**i, "suggested_qty": max(i["reorder_level"] * 2 - i["qty"], 10)} for i in inventory.low_stock()]


def create(data: PoIn) -> dict:
    lines = []
    for line in data.lines:
        item = items.get_or_404(line.sku)
        lines.append({"sku": item["sku"], "name": item["name"], "qty": line.qty, "unit_cost": item["unit_cost"]})
    return orders.add({
        "id": f"PO-{3001 + len(orders.rows)}", "supplier": data.supplier, "created": days(0), "expected": days(10),
        "lines": lines, "total": round(sum(x["qty"] * x["unit_cost"] for x in lines), 2),
        "status": "pending_approval",
    })


def advance(po_id: str) -> dict:
    po = orders.get_or_404(po_id)
    idx = FLOW.index(po["status"])
    if idx == len(FLOW) - 1:
        raise HTTPException(400, "Order already received")
    po["status"] = FLOW[idx + 1]
    if po["status"] == "received":  # goods receipt updates stock
        for line in po["lines"]:
            inventory.adjust(line["sku"], line["qty"])
    return po

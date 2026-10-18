from app.modules.inventory.models import ItemIn, items


def list_items(q: str | None = None, category: str | None = None) -> list[dict]:
    rows = items.all()
    if q:
        rows = [r for r in rows if q.lower() in (r["name"] + r["sku"]).lower()]
    if category:
        rows = [r for r in rows if r["category"] == category]
    return rows


def low_stock() -> list[dict]:
    return [i for i in items.all() if i["qty"] <= i["reorder_level"]]


def stock_value() -> float:
    return round(sum(i["qty"] * i["unit_cost"] for i in items.all()), 2)


def create_item(data: ItemIn) -> dict:
    return items.add({"sku": f"SKU-{1001 + len(items.rows)}", **data.model_dump()})


def adjust(sku: str, delta: int) -> dict:
    item = items.get_or_404(sku)
    item["qty"] = max(0, item["qty"] + delta)
    return item

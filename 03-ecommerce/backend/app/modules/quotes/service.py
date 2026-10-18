from app.core.common import days
from app.modules.catalog import service as catalog
from app.modules.quotes.models import QuoteIn, QuoteResponse, quotes


def with_estimate(q: dict) -> dict:
    """Adds an indicative list value using wholesale tiers so sales can price quickly."""
    estimate = 0.0
    for line in q["items"]:
        p = catalog.by_id(line["product_id"])
        estimate += catalog.unit_price(p, line["qty"], wholesale=True) * line["qty"]
    return {**q, "estimate": round(estimate, 2)}


def list_quotes() -> list[dict]:
    return [with_estimate(q) for q in quotes.all()]


def create(data: QuoteIn) -> dict:
    items = [{"product_id": i.product_id, "name": catalog.by_id(i.product_id)["name"], "qty": i.qty} for i in data.items]
    q = quotes.add({"id": max(x["id"] for x in quotes.all()) + 1, **data.model_dump(exclude={"items"}), "items": items,
                    "created": days(0), "status": "new", "quoted_total": None})
    return with_estimate(q)


def respond(quote_id: int, data: QuoteResponse) -> dict:
    q = quotes.get_or_404(quote_id)
    q["status"] = data.status
    if data.quoted_total is not None:
        q["quoted_total"] = data.quoted_total
    return with_estimate(q)

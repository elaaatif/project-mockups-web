"""RFQ intake with automatic lead scoring so sales can prioritise."""
from app.core.common import days
from app.modules.products.models import products
from app.modules.quotes.models import QuoteIn, rfqs

BUDGET_POINTS = {"< £10k": 5, "£10k–£50k": 15, "£50k–£250k": 25, "£250k+": 35}
TIMELINE_POINTS = {"asap": 25, "1-3 months": 20, "3-6 months": 10, "6+ months": 3}
BUDGET_VALUE = {"< £10k": 6000, "£10k–£50k": 28000, "£50k–£250k": 120000, "£250k+": 380000}
FREE_MAIL = ("gmail.", "hotmail.", "yahoo.", "outlook.")


def score(r: dict) -> int:
    s = BUDGET_POINTS[r["budget"]] + TIMELINE_POINTS[r["timeline"]]
    s += 15 if not any(d in r["email"] for d in FREE_MAIL) else 0   # business email
    s += min(15, 5 * len(r["lines"])) + 5 * len(r["services"])     # breadth of need
    s += 5 if r.get("phone") else 0
    return min(100, s)


def enrich(r: dict) -> dict:
    for line in r["lines"]:
        p = next((x for x in products.all() if x["id"] == line["product_id"]), None)
        line["name"] = p["name"] if p else "Unknown"
    r["score"] = score(r)
    r["value"] = r["value"] or BUDGET_VALUE[r["budget"]]
    r["priority"] = "hot" if r["score"] >= 70 else "warm" if r["score"] >= 45 else "cold"
    return r


for _r in rfqs.all():
    enrich(_r)


def create(data: QuoteIn) -> dict:
    r = data.model_dump()
    r.update(id=f"RFQ-{24100 + len(rfqs.rows)}", stage="new", value=0, created=days(0), source="Website quote form")
    enrich(r)
    rfqs.add(r)
    return {"reference": r["id"], "score": r["score"], "priority": r["priority"],
            "response_time": "within 4 business hours" if r["priority"] == "hot" else "within 1 business day"}

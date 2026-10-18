from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng
from app.modules.inventory.models import items


class PoLine(BaseModel):
    sku: str
    qty: int = Field(gt=0)


class PoIn(BaseModel):
    supplier: str
    lines: list[PoLine] = Field(min_length=1)


FLOW = ["draft", "pending_approval", "approved", "received"]


def _seed(i: int) -> dict:
    picks = rng.sample(items.all(), 2)
    lines = [{"sku": p["sku"], "name": p["name"], "qty": rng.randint(10, 120), "unit_cost": p["unit_cost"]}
             for p in picks]
    return {
        "id": f"PO-{3000 + i}", "supplier": picks[0]["supplier"], "created": days(-rng.randint(1, 30)),
        "expected": days(rng.randint(2, 20)), "lines": lines,
        "total": round(sum(line["qty"] * line["unit_cost"] for line in lines), 2), "status": FLOW[i % 4],
    }


orders = Repository([_seed(i) for i in range(10, 0, -1)])

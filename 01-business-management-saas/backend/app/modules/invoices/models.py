from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng


class InvoiceLine(BaseModel):
    description: str
    qty: float = Field(gt=0)
    price: float = Field(ge=0)


class InvoiceIn(BaseModel):
    client: str
    due_in_days: int = 30
    tax_rate: float = 0.1
    lines: list[InvoiceLine] = Field(min_length=1)


CLIENTS = ["Northwind Traders", "Acme Logistics", "Bluewave Retail", "Cedar Health",
           "Summit Foods", "Orion Builders", "Helix Pharma", "Atlas Motors"]


def _seed(i: int) -> dict:
    issued = -rng.randint(0, 75)
    subtotal = round(rng.uniform(800, 14000), 2)
    return {
        "id": f"INV-2026-{100 + i:04d}", "client": rng.choice(CLIENTS),
        "issue_date": days(issued), "due_date": days(issued + 30),
        "lines": [{"description": "Professional services", "qty": 1, "price": subtotal}],
        "subtotal": subtotal, "tax": round(subtotal * 0.1, 2), "total": round(subtotal * 1.1, 2),
        "paid": rng.random() < 0.55,
    }


invoices = Repository([_seed(i) for i in range(18, 0, -1)])

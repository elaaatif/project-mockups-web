"""Dashboard aggregates data from other modules' services — it owns no data itself."""
from app.core.common import rng
from app.modules.documents import service as documents
from app.modules.fleet import service as fleet
from app.modules.hr.models import employees, leaves
from app.modules.inventory import service as inventory
from app.modules.invoices import service as invoices
from app.modules.purchasing.models import orders

MONTHS = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
_REVENUE = [round(42000 + i * 2600 + rng.uniform(-5000, 6000)) for i in range(12)]
_EXPENSES = [round(r * rng.uniform(0.55, 0.75)) for r in _REVENUE]


def overview() -> dict:
    inv = invoices.summary()
    low = inventory.low_stock()
    pending = (sum(1 for x in leaves.all() if x["status"] == "pending")
               + sum(1 for d in documents.list_documents() if d["status"] in ("submitted", "in_review"))
               + sum(1 for o in orders.all() if o["status"] == "pending_approval"))
    alerts = [{"type": "stock", "message": f"{i['name']} low — {i['qty']} left"} for i in low[:4]]
    alerts += [{"type": "invoice", "message": f"{r['id']} from {r['client']} is overdue"}
               for r in invoices.list_invoices("overdue")[:3]]
    alerts += fleet.alerts()[:4]
    return {
        "kpis": {"revenue": _REVENUE[-1], "revenue_delta": round((_REVENUE[-1] / _REVENUE[-2] - 1) * 100, 1),
                 "outstanding": round(inv["pending"] + inv["overdue"], 2), "stock_value": inventory.stock_value(),
                 "low_stock": len(low), "employees": len(employees.all()), "pending_approvals": pending},
        "revenue_series": {"labels": MONTHS, "revenue": _REVENUE, "expenses": _EXPENSES},
        "expense_breakdown": {"labels": ["Payroll", "Inventory", "Fleet", "Rent", "Software"],
                              "values": [46, 24, 14, 10, 6]},
        "alerts": alerts,
    }

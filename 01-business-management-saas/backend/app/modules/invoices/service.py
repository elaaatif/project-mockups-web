from app.core.common import TODAY, days
from app.modules.invoices.models import InvoiceIn, invoices


def _status(inv: dict) -> str:
    if inv["paid"]:
        return "paid"
    return "overdue" if inv["due_date"] < TODAY.isoformat() else "pending"


def present(inv: dict) -> dict:
    return {**inv, "status": _status(inv)}


def list_invoices(status: str | None = None) -> list[dict]:
    rows = [present(i) for i in invoices.all()]
    return [r for r in rows if r["status"] == status] if status else rows


def summary() -> dict:
    rows = list_invoices()

    def total(s: str) -> float:
        return round(sum(r["total"] for r in rows if r["status"] == s), 2)

    return {"paid": total("paid"), "pending": total("pending"), "overdue": total("overdue"), "count": len(rows)}


def create(data: InvoiceIn) -> dict:
    subtotal = round(sum(line.qty * line.price for line in data.lines), 2)
    tax = round(subtotal * data.tax_rate, 2)
    inv = {
        "id": f"INV-2026-{101 + len(invoices.rows):04d}", "client": data.client,
        "issue_date": days(0), "due_date": days(data.due_in_days),
        "lines": [line.model_dump() for line in data.lines],
        "subtotal": subtotal, "tax": tax, "total": round(subtotal + tax, 2), "paid": False,
    }
    return present(invoices.add(inv))


def mark_paid(invoice_id: str) -> dict:
    inv = invoices.get_or_404(invoice_id)
    inv["paid"] = True
    return present(inv)

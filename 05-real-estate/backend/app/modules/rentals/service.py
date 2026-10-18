from app.core.common import days
from app.modules.rentals.models import TicketIn, payments, tickets, units


def overview() -> dict:
    occupied = [u for u in units.all() if u["status"] == "occupied"]
    current = [p for p in payments.all() if p["month"] == max(x["month"] for x in payments.all())]
    return {
        "kpis": {"units": len(units.all()), "occupancy": round(len(occupied) / len(units.all()) * 100),
                 "monthly_rent": sum(u["rent"] for u in occupied),
                 "collected": sum(p["amount"] for p in current if p["status"] == "paid"),
                 "arrears": sum(p["amount"] for p in current if p["status"] == "late"),
                 "open_tickets": sum(1 for t in tickets.all() if t["status"] != "completed")},
        "units": units.all(),
        "payments": sorted(payments.all(), key=lambda p: (p["month"], p["unit_id"]), reverse=True),
        "tickets": tickets.all(),
    }


def mark_paid(payment_id: int) -> dict:
    p = payments.get_or_404(payment_id)
    p["status"] = "paid"
    return p


def open_ticket(data: TicketIn) -> dict:
    unit = units.get_or_404(data.unit_id)
    return tickets.add({"id": len(tickets.rows) + 1, "unit_id": unit["id"], "address": unit["address"], "title": data.title,
                        "priority": data.priority, "status": "open", "created": days(0), "contractor": None})


def set_ticket_status(ticket_id: int, status: str) -> dict:
    t = tickets.get_or_404(ticket_id)
    t["status"] = status
    if status == "in_progress" and not t["contractor"]:
        t["contractor"] = "Haven Maintenance Team"
    return t

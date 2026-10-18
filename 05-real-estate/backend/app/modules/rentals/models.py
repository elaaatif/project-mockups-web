from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import TODAY, Repository, days, rng


class TicketIn(BaseModel):
    unit_id: int
    title: str = Field(min_length=3)
    priority: Literal["low", "medium", "urgent"] = "medium"


class TicketStatusIn(BaseModel):
    status: Literal["open", "in_progress", "completed"]


_UNITS = [("Flat 1, 14 Mill Lane, Islington", 2150, "Hannah Weber"), ("Flat 3, 14 Mill Lane, Islington", 2300, "Tom Becker"),
          ("12 Rose Terrace, Clapham", 3900, "The Ahmed family"), ("Apt 1204, One Canada Sq, Canary Wharf", 2600, "Kenji Ito"),
          ("Apt 807, Riverside Quay, Greenwich", 2150, None), ("7 Queens Gardens, Notting Hill", 5400, "Laura & Ben Hart"),
          ("Flat 2, 40 Park Road, Richmond", 1950, "Priya Nair"), ("Studio 5, Kings Yard, Hampstead", 1650, None)]

units = Repository([
    {"id": i + 1, "address": a, "rent": rent, "tenant": t, "status": "occupied" if t else "vacant",
     "lease_start": days(-rng.randint(60, 500)) if t else None, "lease_end": days(rng.randint(20, 400)) if t else None,
     "deposit": rent * 5 // 4 if t else 0}
    for i, (a, rent, t) in enumerate(_UNITS)
])

MONTHS = [(TODAY.replace(day=1).month - k - 1) % 12 + 1 for k in range(3)][::-1]
payments = Repository([])
for u in units.all():
    if not u["tenant"]:
        continue
    for k, m in enumerate(MONTHS):
        current = k == len(MONTHS) - 1
        state = rng.choice(["paid", "paid", "pending", "late"]) if current else "paid"
        payments.add({"id": len(payments.rows) + 1, "unit_id": u["id"], "address": u["address"], "tenant": u["tenant"],
                      "month": f"{TODAY.year if m <= TODAY.month else TODAY.year - 1}-{m:02d}", "amount": u["rent"], "status": state,
                      "due": f"{TODAY.year if m <= TODAY.month else TODAY.year - 1}-{m:02d}-01"})

tickets = Repository([
    {"id": 1, "unit_id": 3, "address": _UNITS[2][0], "title": "Boiler not heating water", "priority": "urgent", "status": "in_progress", "created": days(-1), "contractor": "HeatFix Ltd"},
    {"id": 2, "unit_id": 1, "address": _UNITS[0][0], "title": "Kitchen tap dripping", "priority": "low", "status": "open", "created": days(-4), "contractor": None},
    {"id": 3, "unit_id": 6, "address": _UNITS[5][0], "title": "Annual gas safety check", "priority": "medium", "status": "open", "created": days(-2), "contractor": None},
    {"id": 4, "unit_id": 4, "address": _UNITS[3][0], "title": "Replace hallway smoke alarm", "priority": "medium", "status": "completed", "created": days(-12), "contractor": "SafeHome"},
])

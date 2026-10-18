from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng


class CustomerIn(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    phone: str = ""


class BookingIn(BaseModel):
    business_slug: str
    service_id: int
    staff_id: int | None = None  # None = first available
    date: str
    time: str = Field(pattern=r"^\d{2}:\d{2}$")
    party_size: int = Field(default=1, ge=1, le=12)
    customer: CustomerIn
    notes: str = ""


class StatusIn(BaseModel):
    status: Literal["confirmed", "checked_in", "completed", "no_show", "cancelled"]


bookings = Repository([], key="code")

_CUSTOMERS = ["Emma Wilson", "Karim Aziz", "Lena Fischer", "Diego Ramos", "Aisha Bello", "Tom Becker", "Yuki Tanaka",
              "Sara Costa", "Ivan Petrov", "Nora Lindqvist", "Ben Carter", "Priya Nair", "Jack Moore", "Zoe Adams"]


def seed(businesses: list[dict]) -> None:
    """Fill the next 7 days (and the last 7) with realistic bookings so calendars look alive."""
    from app.modules.businesses.service import is_free, to_hhmm, to_minutes

    n = 1000
    for b in businesses:
        for offset in range(-7, 8):
            for staff in b["staff"]:
                for _ in range(rng.randint(1, 5)):
                    svc = rng.choice(b["services"])
                    start = rng.randrange(to_minutes(b["open"]), to_minutes(b["close"]) - svc["minutes"], b["slot_minutes"])
                    day = days(offset)
                    if not is_free(b["slug"], staff["id"], day, start, svc["minutes"]):
                        continue
                    name = rng.choice(_CUSTOMERS)
                    party = rng.randint(2, staff["max_party"]) if staff["max_party"] else 1
                    status = ("completed" if rng.random() > 0.08 else "no_show") if offset < 0 else "confirmed"
                    bookings.add({
                        "code": f"BK-{n}", "business_slug": b["slug"], "business_name": b["name"], "service_id": svc["id"],
                        "service_name": svc["name"], "staff_id": staff["id"], "staff_name": staff["name"], "date": day,
                        "time": to_hhmm(start), "minutes": svc["minutes"], "party_size": party,
                        "price": svc["price"] * (party if svc["per_person"] else 1), "deposit": svc["deposit"],
                        "customer": {"name": name, "email": name.split()[0].lower() + "@example.com", "phone": ""},
                        "notes": "", "status": status, "created": days(min(offset, 0) - 2),
                    })
                    n += 1

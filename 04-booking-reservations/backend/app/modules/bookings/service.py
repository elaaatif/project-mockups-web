from fastapi import HTTPException

from app.core.common import days, rng
from app.modules.bookings.models import BookingIn, bookings, seed
from app.modules.businesses import service as directory
from app.modules.businesses.models import businesses

seed(businesses.all())


def create(data: BookingIn) -> dict:
    b = businesses.get_or_404(data.business_slug)
    svc = directory.service_of(b, data.service_id)
    start = directory.to_minutes(data.time)
    candidates = [s for s in directory.eligible_staff(b, data.party_size) if data.staff_id in (None, s["id"])]
    staff = next((s for s in candidates if directory.is_free(b["slug"], s["id"], data.date, start, svc["minutes"])), None)
    if not staff:
        raise HTTPException(409, "Sorry — that slot was just taken. Please pick another time.")
    booking = {
        "code": f"BK-{rng.randint(2000, 9999)}", "business_slug": b["slug"], "business_name": b["name"],
        "service_id": svc["id"], "service_name": svc["name"], "staff_id": staff["id"], "staff_name": staff["name"],
        "date": data.date, "time": data.time, "minutes": svc["minutes"], "party_size": data.party_size,
        "price": svc["price"] * (data.party_size if svc["per_person"] else 1), "deposit": svc["deposit"] * (data.party_size if svc["per_person"] else 1),
        "customer": data.customer.model_dump(), "notes": data.notes, "status": "confirmed", "created": days(0),
    }
    return bookings.add(booking)


def lookup(email: str) -> list[dict]:
    rows = [b for b in bookings.all() if b["customer"]["email"].lower() == email.strip().lower()]
    return sorted(rows, key=lambda b: (b["date"], b["time"]), reverse=True)


def set_status(code: str, status: str) -> dict:
    booking = bookings.get_or_404(code)
    if booking["status"] == "cancelled":
        raise HTTPException(400, "Booking is already cancelled")
    booking["status"] = status
    return booking

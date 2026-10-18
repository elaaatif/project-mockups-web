from fastapi import APIRouter

from app.modules.bookings import service
from app.modules.bookings.models import BookingIn, StatusIn

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", status_code=201)
def book(body: BookingIn):
    return service.create(body)


@router.get("/lookup")
def lookup(email: str):
    return service.lookup(email)


@router.post("/{code}/cancel")
def cancel(code: str):
    return service.set_status(code, "cancelled")


@router.patch("/{code}/status")
def set_status(code: str, body: StatusIn):
    return service.set_status(code, body.status)

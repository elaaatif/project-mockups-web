from fastapi import APIRouter

from app.modules.rentals import service
from app.modules.rentals.models import TicketIn, TicketStatusIn

router = APIRouter(prefix="/rentals", tags=["Rental Management"])


@router.get("")
def overview():
    return service.overview()


@router.post("/payments/{payment_id}/paid")
def mark_paid(payment_id: int):
    return service.mark_paid(payment_id)


@router.post("/tickets", status_code=201)
def open_ticket(body: TicketIn):
    return service.open_ticket(body)


@router.patch("/tickets/{ticket_id}")
def set_ticket_status(ticket_id: int, body: TicketStatusIn):
    return service.set_ticket_status(ticket_id, body.status)

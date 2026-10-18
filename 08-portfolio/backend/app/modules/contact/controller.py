from fastapi import APIRouter

from app.modules.contact import service
from app.modules.contact.models import EstimateIn, MessageIn, StatusIn, messages

router = APIRouter(prefix="/contact", tags=["Contact & Estimates"])


@router.get("/options")
def options():
    return service.options()


@router.post("/estimate")
def estimate(body: EstimateIn):
    return service.estimate(body)


@router.post("", status_code=201)
def send(body: MessageIn):
    return service.send(body)


@router.get("/messages")
def inbox():
    return messages.all()


@router.patch("/messages/{message_id}")
def set_status(message_id: int, body: StatusIn):
    return service.set_status(message_id, body.status)

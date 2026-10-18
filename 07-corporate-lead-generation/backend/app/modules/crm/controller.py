from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.careers.models import applications
from app.modules.company.models import messages
from app.modules.crm import service
from app.modules.quotes.models import rfqs

router = APIRouter(prefix="/crm", tags=["Leads CRM"])


class RfqUpdate(BaseModel):
    stage: Literal["new", "qualified", "quoted", "negotiation", "won", "lost"] | None = None
    value: float | None = None


class StatusUpdate(BaseModel):
    status: str


@router.get("/overview")
def overview():
    return service.overview()


@router.get("/rfqs")
def list_rfqs():
    return sorted(rfqs.all(), key=lambda r: (-r["score"], r["created"]))


@router.patch("/rfqs/{rfq_id}")
def update_rfq(rfq_id: str, body: RfqUpdate):
    return service.update(rfqs, rfq_id, body.model_dump())


@router.get("/messages")
def list_messages():
    return messages.all()


@router.patch("/messages/{message_id}")
def update_message(message_id: int, body: StatusUpdate):
    return service.update(messages, message_id, body.model_dump())


@router.get("/applications")
def list_applications():
    return applications.all()


@router.patch("/applications/{application_id}")
def update_application(application_id: int, body: StatusUpdate):
    return service.update(applications, application_id, body.model_dump())

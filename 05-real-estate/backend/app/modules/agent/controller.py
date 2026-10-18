from fastapi import APIRouter

from app.modules.agent import service
from app.modules.leads.models import StageIn

router = APIRouter(prefix="/agent", tags=["Agent Dashboard"])


@router.get("/overview")
def overview():
    return service.overview()


@router.get("/pipeline")
def pipeline():
    return service.pipeline()


@router.patch("/leads/{lead_id}")
def move(lead_id: int, body: StageIn):
    return service.move(lead_id, body.stage)


@router.get("/appointments")
def appointments():
    return service.appointments()

from fastapi import APIRouter

from app.modules.training import service
from app.modules.training.models import AssignIn

router = APIRouter(prefix="/training", tags=["Employee Training"])


@router.get("")
def overview():
    return service.overview()


@router.post("/assign", status_code=201)
def assign(body: AssignIn):
    return service.assign(body)


@router.post("/assignments/{assignment_id}/remind")
def remind(assignment_id: int):
    return service.remind(assignment_id)

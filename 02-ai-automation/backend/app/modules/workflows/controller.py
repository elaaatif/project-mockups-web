from fastapi import APIRouter

from app.modules.workflows import service
from app.modules.workflows.models import CATALOG, WorkflowIn, workflows

router = APIRouter(prefix="/workflows", tags=["Email & WhatsApp Workflows"])


@router.get("")
def index():
    return {"workflows": workflows.all(), "catalog": CATALOG}


@router.post("", status_code=201)
def store(body: WorkflowIn):
    return service.create(body)


@router.patch("/{workflow_id}/toggle")
def toggle(workflow_id: int):
    return service.toggle(workflow_id)


@router.post("/{workflow_id}/test")
def test(workflow_id: int):
    return service.test_run(workflow_id)

from fastapi import APIRouter

from app.modules.documents import service
from app.modules.documents.models import DOC_TYPES, Decision, DocumentIn

router = APIRouter(prefix="/documents", tags=["Documents & Approvals"])


@router.get("")
def index():
    return {"documents": service.list_documents(), "types": DOC_TYPES}


@router.post("", status_code=201)
def store(body: DocumentIn):
    return service.create(body)


@router.post("/{doc_id}/decision")
def decide(doc_id: int, body: Decision):
    return service.decide(doc_id, body)

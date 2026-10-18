from fastapi import HTTPException

from app.core.common import days
from app.modules.documents.models import Decision, DocumentIn, documents, make_steps


def status_of(doc: dict) -> str:
    states = [s["status"] for s in doc["steps"]]
    if "rejected" in states:
        return "rejected"
    if all(s == "approved" for s in states):
        return "approved"
    return "in_review" if "approved" in states else "submitted"


def present(doc: dict) -> dict:
    return {**doc, "status": status_of(doc)}


def list_documents() -> list[dict]:
    return [present(d) for d in documents.all()]


def create(data: DocumentIn) -> dict:
    return present(documents.add({"id": len(documents.rows) + 1, **data.model_dump(), "created": days(0),
                                  "size_kb": 240, "steps": make_steps(0)}))


def decide(doc_id: int, data: Decision) -> dict:
    doc = documents.get_or_404(doc_id)
    if status_of(doc) in ("approved", "rejected"):
        raise HTTPException(400, "Workflow already completed")
    step = next(s for s in doc["steps"] if s["status"] == "pending")
    step.update(status="approved" if data.decision == "approve" else "rejected", at=days(0), comment=data.comment)
    return present(doc)

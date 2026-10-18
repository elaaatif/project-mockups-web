from fastapi import APIRouter

from app.core.common import days
from app.modules.company.models import CASE_STUDIES, COMPANY, INDUSTRIES, SERVICES, ContactIn, messages

router = APIRouter(prefix="/company", tags=["Company Website"])


@router.get("")
def overview():
    return COMPANY | {"services": SERVICES, "industries": INDUSTRIES, "case_studies": CASE_STUDIES}


@router.get("/services/{slug}")
def service(slug: str):
    from fastapi import HTTPException
    s = next((s for s in SERVICES if s["slug"] == slug), None)
    if not s:
        raise HTTPException(404, "Service not found")
    return s


@router.post("/contact", status_code=201)
def contact(body: ContactIn):
    return messages.add({"id": len(messages.rows) + 1, **body.model_dump(), "created": days(0), "status": "new"})

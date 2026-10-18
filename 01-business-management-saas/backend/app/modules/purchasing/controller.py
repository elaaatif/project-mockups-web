from fastapi import APIRouter

from app.modules.purchasing import service
from app.modules.purchasing.models import FLOW, PoIn, orders

router = APIRouter(prefix="/purchasing", tags=["Purchasing"])


@router.get("")
def index():
    return {"orders": orders.all(), "flow": FLOW, "suggestions": service.suggestions()}


@router.post("", status_code=201)
def store(body: PoIn):
    return service.create(body)


@router.patch("/{po_id}/advance")
def advance(po_id: str):
    return service.advance(po_id)

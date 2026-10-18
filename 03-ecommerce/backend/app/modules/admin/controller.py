from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.modules.admin import service

router = APIRouter(prefix="/admin", tags=["Store Admin"])


class RestockIn(BaseModel):
    qty: int = Field(gt=0)


@router.get("/overview")
def overview():
    return service.overview()


@router.get("/inventory")
def inventory():
    return service.inventory()


@router.post("/inventory/{slug}/restock")
def restock(slug: str, body: RestockIn):
    return service.restock(slug, body.qty)

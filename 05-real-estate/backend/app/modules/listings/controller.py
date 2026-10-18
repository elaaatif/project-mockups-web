from fastapi import APIRouter

from app.modules.listings import service
from app.modules.listings.models import DISTRICTS, agents

router = APIRouter(prefix="/listings", tags=["Property Listings"])


@router.get("")
def search(purpose: str | None = None, type: str | None = None, district: str | None = None, min_beds: int = 0,
           max_price: int | None = None, q: str | None = None, sort: str = "featured"):
    return service.search(purpose, type, district, min_beds, max_price, q, sort)


@router.get("/meta")
def meta():
    return {"districts": list(DISTRICTS), "types": ["apartment", "house", "penthouse", "villa"], "agents": agents.all()}


@router.get("/{slug}")
def detail(slug: str):
    return service.detail(slug)

from fastapi import APIRouter

from app.modules.businesses import service
from app.modules.businesses.models import CATEGORIES, businesses

router = APIRouter(prefix="/businesses", tags=["Businesses & Availability"])


@router.get("/categories")
def categories():
    return [c | {"count": sum(1 for b in businesses.all() if b["category"] == c["slug"])} for c in CATEGORIES]


@router.get("")
def index(category: str | None = None, q: str | None = None):
    return service.list_businesses(category, q)


@router.get("/{slug}")
def show(slug: str):
    return businesses.get_or_404(slug) | {"days": service.week_days()}


@router.get("/{slug}/availability")
def availability(slug: str, service_id: int, date: str, staff_id: int | None = None, party_size: int = 2):
    return service.availability(slug, service_id, date, staff_id, party_size)

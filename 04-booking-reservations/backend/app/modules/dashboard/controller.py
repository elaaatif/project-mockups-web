from fastapi import APIRouter

from app.modules.dashboard import service

router = APIRouter(prefix="/dashboard", tags=["Business Dashboard"])


@router.get("/{slug}")
def overview(slug: str, date: str | None = None):
    return service.overview(slug, date)


@router.get("/{slug}/bookings")
def bookings(slug: str, status: str | None = None):
    return service.list_bookings(slug, status)

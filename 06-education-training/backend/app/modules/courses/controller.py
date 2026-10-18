from fastapi import APIRouter

from app.modules.courses import service
from app.modules.courses.models import CATEGORIES

router = APIRouter(prefix="/courses", tags=["Course Catalog"])


@router.get("/categories")
def categories():
    return CATEGORIES


@router.get("")
def catalog(q: str | None = None, category: str | None = None, level: str | None = None):
    return service.catalog(q, category, level)


@router.get("/{slug}")
def detail(slug: str):
    return service.detail(slug)

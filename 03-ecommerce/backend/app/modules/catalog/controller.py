from fastapi import APIRouter

from app.modules.catalog import service
from app.modules.catalog.models import CATEGORIES

router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/categories")
def categories():
    return CATEGORIES


@router.get("/products")
def products(q: str | None = None, category: str | None = None, sort: str = "featured",
             max_price: float | None = None, in_stock: bool = False):
    return service.list_products(q, category, sort, max_price, in_stock)


@router.get("/products/{slug}")
def product(slug: str):
    return service.detail(slug)

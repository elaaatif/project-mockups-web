from fastapi import APIRouter

from app.modules.products.models import CATEGORIES, products

router = APIRouter(prefix="/products", tags=["Product Catalog"])


@router.get("/categories")
def categories():
    return [c | {"count": sum(1 for p in products.all() if p["category"] == c["slug"])} for c in CATEGORIES]


@router.get("")
def index(category: str | None = None, q: str | None = None):
    rows = products.all()
    if category:
        rows = [p for p in rows if p["category"] == category]
    if q:
        rows = [p for p in rows if q.lower() in (p["name"] + p["summary"] + " ".join(p["applications"])).lower()]
    return rows


@router.get("/{slug}")
def show(slug: str):
    p = products.get_or_404(slug)
    return p | {"related": [r for r in products.all() if r["category"] == p["category"] and r["id"] != p["id"]][:3]}

from fastapi import APIRouter

from app.modules.inventory import service
from app.modules.inventory.models import CATEGORIES, ItemIn, StockAdjust

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("")
def index(q: str | None = None, category: str | None = None):
    return {"items": service.list_items(q, category), "categories": CATEGORIES,
            "low_stock": len(service.low_stock()), "stock_value": service.stock_value()}


@router.post("", status_code=201)
def store(body: ItemIn):
    return service.create_item(body)


@router.patch("/{sku}/adjust")
def adjust(sku: str, body: StockAdjust):
    return service.adjust(sku, body.delta)

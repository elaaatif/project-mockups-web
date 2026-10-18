from fastapi import APIRouter

from app.modules.orders import service
from app.modules.orders.models import OrderIn

router = APIRouter(prefix="/orders", tags=["Orders & Tracking"])


@router.post("", status_code=201)
def checkout(body: OrderIn):
    return service.create(body)


@router.get("/track")
def track(order_id: str, email: str):
    return service.track(order_id, email)


@router.get("")
def index():
    return service.list_orders()


@router.patch("/{order_id}/advance")
def advance(order_id: str):
    return service.advance(order_id)

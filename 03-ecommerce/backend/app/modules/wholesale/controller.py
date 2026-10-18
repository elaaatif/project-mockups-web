from fastapi import APIRouter

from app.modules.wholesale import service
from app.modules.wholesale.models import WholesaleOrderIn

router = APIRouter(prefix="/wholesale", tags=["Wholesale Portal"])


@router.get("/price-list")
def price_list():
    return service.price_list()


@router.post("/orders", status_code=201)
def place(body: WholesaleOrderIn):
    return service.place(body)

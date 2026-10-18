from fastapi import APIRouter

from app.modules.leads import service
from app.modules.leads.models import EnquiryIn, ValuationIn, ViewingIn

router = APIRouter(prefix="/leads", tags=["Lead Generation"])


@router.post("/enquiry", status_code=201)
def enquiry(body: EnquiryIn):
    return service.enquire(body)


@router.get("/viewing-slots")
def viewing_slots(property_id: int, date: str):
    return service.free_slots(property_id, date)


@router.post("/viewings", status_code=201)
def book_viewing(body: ViewingIn):
    return service.book_viewing(body)


@router.post("/valuation")
def valuation(body: ValuationIn):
    return service.valuation(body)

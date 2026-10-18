from fastapi import APIRouter

from app.modules.quotes import service
from app.modules.quotes.models import QuoteIn

router = APIRouter(prefix="/quotes", tags=["Quote Requests (RFQ)"])


@router.post("", status_code=201)
def request_quote(body: QuoteIn):
    return service.create(body)

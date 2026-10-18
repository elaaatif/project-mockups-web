from fastapi import APIRouter

from app.modules.quotes import service
from app.modules.quotes.models import QuoteIn, QuoteResponse

router = APIRouter(prefix="/quotes", tags=["Quotation Requests"])


@router.post("", status_code=201)
def request_quote(body: QuoteIn):
    return service.create(body)


@router.get("")
def index():
    return service.list_quotes()


@router.patch("/{quote_id}")
def respond(quote_id: int, body: QuoteResponse):
    return service.respond(quote_id, body)

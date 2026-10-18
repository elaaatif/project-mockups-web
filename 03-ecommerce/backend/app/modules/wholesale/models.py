from pydantic import BaseModel, Field

from app.modules.orders.models import LineIn


class WholesaleOrderIn(BaseModel):
    company: str = Field(min_length=2)
    vat_number: str = ""
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    po_reference: str = ""
    items: list[LineIn] = Field(min_length=1)


MIN_ORDER_VALUE = 500
PAYMENT_TERMS = "Net 30"

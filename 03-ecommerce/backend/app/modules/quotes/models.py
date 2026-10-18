from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository, days
from app.modules.orders.models import LineIn


class QuoteIn(BaseModel):
    company: str = Field(min_length=2)
    contact: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    phone: str = ""
    needed_by: str | None = None
    notes: str = ""
    items: list[LineIn] = Field(min_length=1)


class QuoteResponse(BaseModel):
    status: Literal["quoted", "won", "lost"]
    quoted_total: float | None = None
    message: str = ""


quotes = Repository([
    {"id": 301, "company": "Hotel Lumière", "contact": "Claire Martin", "email": "claire@lumiere.fr", "phone": "+33 1 42 00 00",
     "items": [{"product_id": 13, "name": "Arc Floor Lamp", "qty": 120}, {"product_id": 14, "name": "Oak Bar Stool", "qty": 60}],
     "notes": "Fit-out for 60 rooms, delivery in two phases.", "needed_by": days(45), "created": days(-2), "status": "new", "quoted_total": None},
    {"id": 302, "company": "Peak Fitness Clubs", "contact": "Marcus Lee", "email": "marcus@peakfit.com", "phone": "",
     "items": [{"product_id": 7, "name": "Orbit Smartwatch S2", "qty": 300}], "notes": "Staff incentive programme, custom engraving?",
     "needed_by": days(30), "created": days(-5), "status": "quoted", "quoted_total": 54600},
    {"id": 303, "company": "Studio Nord Architects", "contact": "Ingrid Holm", "email": "ingrid@studionord.no", "phone": "+47 22 00 00",
     "items": [{"product_id": 15, "name": "Emerald Velvet Sofa", "qty": 8}], "notes": "", "needed_by": None, "created": days(-9), "status": "won", "quoted_total": 8900},
])

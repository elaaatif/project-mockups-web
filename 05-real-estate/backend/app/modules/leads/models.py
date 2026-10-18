from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng
from app.modules.listings.models import properties

EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
STAGES = ["new", "contacted", "viewing", "negotiation", "won", "lost"]


class EnquiryIn(BaseModel):
    property_id: int | None = None
    name: str = Field(min_length=2)
    email: str = Field(pattern=EMAIL)
    phone: str = ""
    message: str = ""


class ViewingIn(BaseModel):
    property_id: int
    date: str
    time: str = Field(pattern=r"^\d{2}:\d{2}$")
    name: str = Field(min_length=2)
    email: str = Field(pattern=EMAIL)
    phone: str = ""


class ValuationIn(BaseModel):
    district: str
    type: Literal["apartment", "house", "penthouse", "villa"]
    beds: int = Field(ge=0, le=12)
    area_sqm: int = Field(gt=10, le=5000)
    condition: Literal["needs_work", "good", "excellent"] = "good"
    name: str = Field(min_length=2)
    email: str = Field(pattern=EMAIL)
    phone: str = ""


class StageIn(BaseModel):
    stage: Literal["new", "contacted", "viewing", "negotiation", "won", "lost"]


VIEWING_TIMES = ["09:30", "10:30", "11:30", "13:00", "14:00", "15:00", "16:00", "17:30"]

_NAMES = ["Oliver Grant", "Amelia Hughes", "Harry Patel", "Isla Murphy", "George Wright", "Mia Thompson", "Arjun Mehta",
          "Freya Collins", "Leo Fischer", "Chloe Evans", "Ethan Brooks", "Ruby Ahmed", "Samuel Price", "Grace Kim"]
_SOURCES = ["Website enquiry", "Viewing request", "Valuation request", "Rightmove", "Zoopla", "Walk-in", "Referral"]

leads = Repository([
    {"id": i + 1, "name": n, "email": n.split()[0].lower() + "@example.com", "phone": f"+44 7700 9{rng.randint(10000, 99999)}",
     "source": rng.choice(_SOURCES), "property_id": (p := rng.choice(properties.all()))["id"], "property_title": p["title"],
     "budget": p["price"], "purpose": p["purpose"], "agent_id": p["agent_id"], "stage": STAGES[i % 6] if i % 6 != 5 or i > 10 else "new",
     "score": rng.randint(35, 98), "created": days(-rng.randint(0, 25)), "message": "Is this still available? Keen to arrange a viewing."}
    for i, n in enumerate(_NAMES)
])
viewings = Repository([
    {"id": i + 1, "property_id": (p := rng.choice(properties.all()))["id"], "property_title": p["title"], "address": p["address"],
     "agent_id": p["agent_id"], "date": days(rng.randint(0, 6)), "time": rng.choice(VIEWING_TIMES), "name": rng.choice(_NAMES),
     "email": "viewer@example.com", "phone": "", "status": "confirmed"}
    for i in range(12)
])

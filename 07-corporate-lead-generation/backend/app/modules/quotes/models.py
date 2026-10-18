from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng


class QuoteLine(BaseModel):
    product_id: int
    qty: int = Field(gt=0, le=10000)
    notes: str = ""


class QuoteIn(BaseModel):
    lines: list[QuoteLine] = Field(min_length=1)
    industry: str
    timeline: Literal["asap", "1-3 months", "3-6 months", "6+ months"]
    budget: Literal["< £10k", "£10k–£50k", "£50k–£250k", "£250k+"]
    services: list[str] = []
    company: str = Field(min_length=2)
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    phone: str = ""
    country: str = "United Kingdom"
    message: str = ""


_COMPANIES = [("Northline Foods", "Food & beverage"), ("Aquaterra Water", "Water treatment"), ("Kestrel Automotive", "Automotive"),
              ("Helix Pharma", "Pharmaceutical"), ("Solent Energy", "Energy & utilities"), ("Brightwell Brewery", "Food & beverage"),
              ("Meridian Aerospace", "Aerospace"), ("Ridgeway Water", "Water treatment")]
_STAGES = ["new", "qualified", "quoted", "negotiation", "won", "lost"]

rfqs = Repository([
    {"id": f"RFQ-{24100 + i}", "company": c, "industry": ind, "name": rng.choice(["Sarah Lane", "Tom Fisher", "Ana Gómez", "Raj Patel", "Ewan Ross"]),
     "email": f"buyer@{c.split()[0].lower()}.com", "phone": "", "country": rng.choice(["United Kingdom", "Ireland", "Germany", "Netherlands"]),
     "lines": [{"product_id": pid, "name": "", "qty": rng.choice([2, 4, 10, 25, 60])} for pid in rng.sample(range(1, 11), 2)],
     "timeline": rng.choice(["asap", "1-3 months", "3-6 months"]), "budget": rng.choice(["£10k–£50k", "£50k–£250k", "£250k+"]),
     "services": rng.sample(["Installation", "Maintenance contract", "Engineering design", "Training"], 1), "message": "",
     "score": 0, "stage": _STAGES[i % 6], "value": 0, "created": days(-rng.randint(0, 20)), "source": rng.choice(["Product page", "Google Ads", "LinkedIn", "Trade show", "Organic search"])}
    for i, (c, ind) in enumerate(_COMPANIES)
])

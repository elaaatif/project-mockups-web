from fastapi import APIRouter

router = APIRouter(prefix="/plans", tags=["Listing Plans"])

LISTING_PLANS = [
    {"name": "Basic listing", "price": 49, "period": "one-off · 60 days", "features": ["Listed on Haven.estate", "10 photos", "Enquiry inbox"]},
    {"name": "Featured", "price": 149, "period": "one-off · 90 days", "popular": True,
     "features": ["Top of search results", "Featured badge & homepage slot", "Unlimited photos + floor plan", "Viewing booking calendar"]},
    {"name": "Agency subscription", "price": 299, "period": "per month", "features": ["Unlimited listings", "Agent CRM & pipeline", "Rental management", "Lead fees from £15 per qualified lead"]},
]


@router.get("")
def plans():
    return LISTING_PLANS

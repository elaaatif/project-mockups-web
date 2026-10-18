from fastapi import APIRouter

router = APIRouter(prefix="/plans", tags=["Business Plans"])

PLANS = [
    {"name": "Pay as you go", "price": "$0", "period": "/mo", "fee": "$0.79 per booking",
     "features": ["Online booking page", "Email confirmations", "1 staff calendar"]},
    {"name": "Business", "price": "$39", "period": "/mo", "fee": "No booking fees", "popular": True,
     "features": ["Unlimited bookings", "Up to 10 staff", "SMS & WhatsApp reminders", "Deposits & no-show protection", "Reports"]},
    {"name": "Multi-location", "price": "$119", "period": "/mo", "fee": "No booking fees",
     "features": ["Everything in Business", "Unlimited locations", "Custom domain & branding", "API & POS integrations", "Priority support"]},
]


@router.get("")
def plans():
    return PLANS

from fastapi import APIRouter

router = APIRouter(prefix="/plans", tags=["Plans & Licences"])

PLANS = [
    {"name": "Single course", "price": "from $39", "period": "one-off", "audience": "Individuals",
     "features": ["Lifetime access to one course", "Assessment & certificate", "Mobile & offline viewing"]},
    {"name": "All-access", "price": "$29", "period": "/month", "audience": "Individuals", "popular": True,
     "features": ["Every course in the catalogue", "Unlimited certificates", "New courses monthly", "Cancel anytime"]},
    {"name": "Teams", "price": "$12", "period": "/seat/month", "audience": "Companies",
     "features": ["Assign & track employee training", "Compliance dashboard & reminders", "SSO & HRIS sync", "Min. 10 seats"]},
    {"name": "Institution licence", "price": "Custom", "period": "annual", "audience": "Schools & training centres",
     "features": ["Cohorts, timetable & attendance", "Student fees & invoicing", "White-label portal", "Dedicated success manager"]},
]


@router.get("")
def plans():
    return PLANS

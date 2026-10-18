from fastapi import APIRouter

from app.modules.pricing.models import PLANS

router = APIRouter(prefix="/pricing", tags=["Pricing"])


@router.get("")
def plans():
    return PLANS

from fastapi import APIRouter

from app.modules.billing import service

router = APIRouter(prefix="/billing", tags=["Billing & Plans"])


@router.get("/plans")
def plans():
    return service.catalog()

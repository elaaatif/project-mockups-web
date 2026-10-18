from fastapi import APIRouter

from app.modules.overview import service

router = APIRouter(prefix="/overview", tags=["Overview"])


@router.get("")
def overview():
    return service.overview()

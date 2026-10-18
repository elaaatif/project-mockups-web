from fastapi import APIRouter

from app.modules.dashboard import service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def overview():
    return service.overview()

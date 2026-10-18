from fastapi import APIRouter

from app.modules.projects import service
from app.modules.projects.models import projects

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("")
def index():
    return projects.all()


@router.get("/status")
def status():
    return service.status()


@router.get("/{slug}")
def show(slug: str):
    return service.detail(slug)

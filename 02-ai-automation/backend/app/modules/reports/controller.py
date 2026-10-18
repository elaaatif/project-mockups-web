from fastapi import APIRouter

from app.modules.reports import service
from app.modules.reports.models import TEMPLATES, ReportIn, ScheduleIn

router = APIRouter(prefix="/reports", tags=["Automated Reporting"])


@router.get("/templates")
def templates():
    return [{k: t[k] for k in ("id", "name", "description", "icon")} for t in TEMPLATES]


@router.post("/generate")
def generate(body: ReportIn):
    return service.generate(body)


@router.get("/schedules")
def schedules():
    return service.list_schedules()


@router.post("/schedules", status_code=201)
def create_schedule(body: ScheduleIn):
    return service.create_schedule(body)


@router.delete("/schedules/{schedule_id}", status_code=204)
def delete_schedule(schedule_id: int):
    service.delete_schedule(schedule_id)

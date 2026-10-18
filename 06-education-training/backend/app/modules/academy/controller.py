from fastapi import APIRouter

from app.modules.academy import service
from app.modules.academy.models import AttendanceIn, StudentIn

router = APIRouter(prefix="/academy", tags=["Training Centre Administration"])


@router.get("")
def overview():
    return service.overview()


@router.post("/students", status_code=201)
def add_student(body: StudentIn):
    return service.add_student(body)


@router.post("/students/{student_id}/payment")
def record_payment(student_id: int):
    return service.record_payment(student_id)


@router.post("/attendance")
def mark_attendance(body: AttendanceIn):
    return service.mark_attendance(body)

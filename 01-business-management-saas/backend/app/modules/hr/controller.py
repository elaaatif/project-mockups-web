from fastapi import APIRouter

from app.modules.hr import service
from app.modules.hr.models import LEAVE_TYPES, LeaveDecision, LeaveIn, PayrollIn, employees, leaves, payroll_runs

router = APIRouter(prefix="/hr", tags=["HR & Payroll"])


@router.get("/employees")
def list_employees():
    return employees.all()


@router.get("/leaves")
def list_leaves():
    return {"leaves": leaves.all(), "types": LEAVE_TYPES}


@router.post("/leaves", status_code=201)
def create_leave(body: LeaveIn):
    return service.request_leave(body)


@router.patch("/leaves/{leave_id}")
def decide(leave_id: int, body: LeaveDecision):
    return service.decide_leave(leave_id, body.status)


@router.get("/payroll")
def list_runs():
    return payroll_runs.all()


@router.post("/payroll/run", status_code=201)
def run(body: PayrollIn):
    return service.run_payroll(body.month)

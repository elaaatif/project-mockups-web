from datetime import date

from fastapi import HTTPException

from app.modules.hr.models import LeaveIn, employees, leaves, payroll_runs


def decide_leave(leave_id: int, status: str) -> dict:
    leave = leaves.get_or_404(leave_id)
    if leave["status"] != "pending":
        raise HTTPException(400, "Request already decided")
    leave["status"] = status
    if status == "approved":
        emp = employees.get_or_404(leave["employee_id"])
        emp["leave_balance"] = max(0, emp["leave_balance"] - leave["days"])
    return leave


def request_leave(data: LeaveIn) -> dict:
    emp = employees.get_or_404(data.employee_id)
    n = (date.fromisoformat(data.end) - date.fromisoformat(data.start)).days + 1
    if n < 1:
        raise HTTPException(400, "End date must be after start date")
    return leaves.add({"id": 101 + len(leaves.rows), "employee_id": emp["id"], "name": emp["name"],
                       "type": data.type, "start": data.start, "end": data.end, "days": n,
                       "reason": data.reason, "status": "pending"})


def _income_tax(gross: float) -> float:
    """Simple progressive monthly brackets (demo only)."""
    brackets = [(2000, 0.0), (5000, 0.15), (float("inf"), 0.25)]
    tax, lower = 0.0, 0.0
    for upper, rate in brackets:
        if gross > lower:
            tax += (min(gross, upper) - lower) * rate
        lower = upper
    return round(tax, 2)


def run_payroll(month: str) -> dict:
    slips = []
    for e in employees.all():
        gross = float(e["salary"])
        tax, social = _income_tax(gross), round(gross * 0.07, 2)
        slips.append({"employee": e["name"], "role": e["role"], "gross": gross, "tax": tax,
                      "social": social, "net": round(gross - tax - social, 2)})
    run = {"id": len(payroll_runs.rows) + 1, "month": month, "slips": slips,
           "totals": {k: round(sum(s[k] for s in slips), 2) for k in ("gross", "tax", "social", "net")}}
    return payroll_runs.add(run)

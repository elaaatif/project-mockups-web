from typing import Literal

from pydantic import BaseModel

from app.core.common import Repository, days, rng


class LeaveDecision(BaseModel):
    status: Literal["approved", "rejected"]


class LeaveIn(BaseModel):
    employee_id: int
    type: str
    start: str
    end: str
    reason: str = ""


class PayrollIn(BaseModel):
    month: str  # YYYY-MM


_PEOPLE = [
    ("Amira Haddad", "Operations Manager", "Operations"), ("Lucas Moreau", "Accountant", "Finance"),
    ("Sofia Rossi", "HR Specialist", "People"), ("Daniel Kim", "Warehouse Lead", "Operations"),
    ("Noah Becker", "Fleet Coordinator", "Logistics"), ("Layla Nasser", "Procurement Officer", "Finance"),
    ("Ethan Clarke", "Driver", "Logistics"), ("Maya Patel", "Sales Executive", "Sales"),
    ("Omar Saleh", "IT Administrator", "IT"), ("Chloe Martin", "Customer Success", "Sales"),
    ("Yusuf Demir", "Driver", "Logistics"), ("Hana Sato", "Payroll Officer", "Finance"),
]
employees = Repository([
    {"id": i + 1, "name": n, "role": r, "department": d, "email": n.split()[0].lower() + "@opsflow.io",
     "salary": rng.randrange(2800, 9200, 50), "leave_balance": rng.randint(4, 24),
     "joined": days(-rng.randint(90, 2200)), "status": "on_leave" if i in (4, 9) else "active"}
    for i, (n, r, d) in enumerate(_PEOPLE)
])

LEAVE_TYPES = ["Annual", "Sick", "Parental", "Unpaid"]


def _leave(i: int, emp: dict) -> dict:
    start, length = rng.randint(-10, 30), rng.randint(1, 6)
    return {"id": 100 + i, "employee_id": emp["id"], "name": emp["name"], "type": rng.choice(LEAVE_TYPES),
            "start": days(start), "end": days(start + length - 1), "days": length,
            "reason": "Family travel" if i % 2 else "Medical appointment",
            "status": ["pending", "pending", "approved", "rejected"][i % 4]}


leaves = Repository([_leave(i, e) for i, e in enumerate(rng.sample(employees.all(), 8))])
payroll_runs = Repository([])

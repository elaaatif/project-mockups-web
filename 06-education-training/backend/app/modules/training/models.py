from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng
from app.modules.courses.models import courses


class AssignIn(BaseModel):
    course_id: int
    team: str | None = None          # assign to a whole team…
    employee_ids: list[int] = []     # …or to specific people
    due_in_days: int = Field(default=30, ge=1, le=365)


TEAMS = ["Sales", "Operations", "Engineering", "Finance", "Customer Success"]
_NAMES = ["Ava Turner", "Ben Cole", "Chloe Park", "Dev Shah", "Ella Ross", "Finn Doyle", "Gia Lopez", "Hugo Brandt", "Isla Reid",
          "Jay Kim", "Kara Nolan", "Liam Ortiz", "Mila Novak", "Nate Price", "Owen Hale", "Pia Larsen", "Quinn Alvarez", "Rosa Diaz"]

employees = Repository([{"id": i + 1, "name": n, "team": TEAMS[i % len(TEAMS)], "email": n.split()[0].lower() + "@northwind.co"} for i, n in enumerate(_NAMES)])

MANDATORY = [7, 8]  # GDPR + Cyber security are mandatory compliance courses
assignments = Repository([])
for e in employees.all():
    for cid in MANDATORY + ([rng.choice([1, 3, 5])] if rng.random() > 0.4 else []):
        c = next(x for x in courses.all() if x["id"] == cid)
        progress = rng.choice([0, 25, 60, 100, 100, 100, 100, 100, 100])
        assignments.add({"id": len(assignments.rows) + 1, "employee_id": e["id"], "employee": e["name"], "team": e["team"],
                         "course_id": cid, "course": c["title"], "mandatory": cid in MANDATORY, "progress": progress,
                         "due": days(rng.randint(-10, 40)), "completed": days(-rng.randint(1, 30)) if progress == 100 else None})

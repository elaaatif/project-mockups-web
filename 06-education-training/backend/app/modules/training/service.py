"""Corporate training: assign courses to teams/people and track compliance."""
from fastapi import HTTPException

from app.core.common import TODAY, days
from app.modules.courses.service import by_id
from app.modules.training.models import MANDATORY, TEAMS, AssignIn, assignments, employees


def status(a: dict) -> str:
    if a["progress"] == 100:
        return "completed"
    if a["due"] < TODAY.isoformat():
        return "overdue"
    return "in_progress" if a["progress"] else "not_started"


def overview() -> dict:
    rows = [a | {"status": status(a)} for a in assignments.all()]
    mandatory = [a for a in rows if a["mandatory"]]
    teams = []
    for t in TEAMS:
        tm = [a for a in mandatory if a["team"] == t]
        teams.append({"team": t, "compliance": round(sum(a["status"] == "completed" for a in tm) / len(tm) * 100) if tm else 0,
                      "overdue": sum(a["status"] == "overdue" for a in tm), "people": sum(1 for e in employees.all() if e["team"] == t)})
    return {
        "kpis": {"employees": len(employees.all()), "assignments": len(rows),
                 "compliance": round(sum(a["status"] == "completed" for a in mandatory) / len(mandatory) * 100),
                 "overdue": sum(a["status"] == "overdue" for a in rows),
                 "hours_learned": round(sum(a["progress"] for a in rows) / 100 * 4.5)},
        "teams": teams, "assignments": sorted(rows, key=lambda a: (a["status"] != "overdue", a["due"])),
        "employees": employees.all(), "mandatory_course_ids": MANDATORY,
    }


def assign(data: AssignIn) -> dict:
    course = by_id(data.course_id)
    targets = [e for e in employees.all() if (data.team and e["team"] == data.team) or e["id"] in data.employee_ids]
    if not targets:
        raise HTTPException(400, "Choose a team or at least one employee")
    created = 0
    for e in targets:
        if any(a["employee_id"] == e["id"] and a["course_id"] == course["id"] for a in assignments.all()):
            continue
        assignments.add({"id": len(assignments.rows) + 1, "employee_id": e["id"], "employee": e["name"], "team": e["team"],
                         "course_id": course["id"], "course": course["title"], "mandatory": course["id"] in MANDATORY,
                         "progress": 0, "due": days(data.due_in_days), "completed": None})
        created += 1
    return {"created": created, "skipped": len(targets) - created, "course": course["title"]}


def remind(assignment_id: int) -> dict:
    a = assignments.get_or_404(assignment_id)
    return {"sent_to": a["employee"], "course": a["course"]}

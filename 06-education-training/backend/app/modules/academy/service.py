from fastapi import HTTPException

from app.core.common import days
from app.modules.academy.models import AttendanceIn, StudentIn, attendance_log, cohorts, students


def overview() -> dict:
    all_students = students.all()
    rows = []
    for c in cohorts.all():
        members = [s for s in all_students if s["cohort_id"] == c["id"]]
        rows.append({k: v for k, v in c.items() if k != "sessions"} | {
            "sessions": [{"day": d, "start": s, "end": e} for d, s, e in c["sessions"]], "enrolled": len(members),
            "attendance": round(sum(s["attendance"] for s in members) / len(members)) if members else 0})
    return {
        "kpis": {"students": len(all_students), "cohorts": len(rows), "revenue": sum(s["paid"] for s in all_students),
                 "outstanding": sum(s["fee"] - s["paid"] for s in all_students),
                 "attendance": round(sum(s["attendance"] for s in all_students) / len(all_students))},
        "cohorts": rows, "students": all_students,
    }


def add_student(data: StudentIn) -> dict:
    c = cohorts.get_or_404(data.cohort_id)
    if sum(1 for s in students.all() if s["cohort_id"] == c["id"]) >= c["capacity"]:
        raise HTTPException(409, f"{c['name']} is full")
    return students.add({"id": max(s["id"] for s in students.all()) + 1, "name": data.name, "email": data.email, "cohort_id": c["id"],
                         "paid": 0, "fee": c["fee"], "attendance": 100, "enrolled": days(0)})


def record_payment(student_id: int) -> dict:
    s = students.get_or_404(student_id)
    s["paid"] = s["fee"]
    return s


def mark_attendance(data: AttendanceIn) -> dict:
    s = students.get_or_404(data.student_id)
    attendance_log.add({"student_id": s["id"], "date": days(0), "status": data.status})
    delta = {"present": 1, "late": 0, "absent": -4}[data.status]
    s["attendance"] = max(0, min(100, s["attendance"] + delta))
    return s

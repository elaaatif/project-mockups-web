"""Training-centre administration: students, cohorts, timetable, attendance and fees."""
from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng


class StudentIn(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    cohort_id: int


class AttendanceIn(BaseModel):
    student_id: int
    status: Literal["present", "absent", "late"]


cohorts = Repository([
    {"id": 1, "name": "Data Analytics · Evening", "room": "Lab 1", "trainer": "Dr. Maya Chen", "fee": 1200, "capacity": 18, "starts": days(-21), "weeks": 10,
     "sessions": [("Mon", "18:00", "20:30"), ("Wed", "18:00", "20:30")]},
    {"id": 2, "name": "Python Bootcamp · Full-time", "room": "Lab 2", "trainer": "Priya Raman", "fee": 3400, "capacity": 20, "starts": days(-7), "weeks": 8,
     "sessions": [("Mon", "09:30", "16:30"), ("Tue", "09:30", "16:30"), ("Thu", "09:30", "16:30")]},
    {"id": 3, "name": "Leadership Programme", "room": "Room A", "trainer": "Marcus Webb", "fee": 1800, "capacity": 14, "starts": days(-35), "weeks": 6,
     "sessions": [("Fri", "10:00", "13:00")]},
    {"id": 4, "name": "UX Design · Weekend", "room": "Studio", "trainer": "Priya Raman", "fee": 1500, "capacity": 16, "starts": days(7), "weeks": 8,
     "sessions": [("Sat", "10:00", "15:00")]},
])

_NAMES = ["Aria Bell", "Bilal Khan", "Cora Wu", "Dario Russo", "Esme Clarke", "Felix Grant", "Gemma Shaw", "Hamza Ali", "Iris Moore",
          "Jonah Fox", "Keira Lane", "Luca Romano", "Maya Singh", "Noel Hart", "Olivia Ng", "Pablo Vega", "Rhea Kapoor", "Sami Haddad",
          "Tara Quinn", "Umar Farouk", "Vera Ivanova", "Will Turner"]
def _student(i: int, name: str) -> dict:
    cohort = cohorts.all()[i % len(cohorts.all())]
    return {"id": i + 1, "name": name, "email": name.split()[0].lower() + "@mail.com", "cohort_id": cohort["id"],
            "paid": cohort["fee"] if i % 5 else cohort["fee"] // 2, "fee": cohort["fee"],
            "attendance": rng.randint(72, 100), "enrolled": days(-rng.randint(10, 60))}


students = Repository([_student(i, n) for i, n in enumerate(_NAMES)])
attendance_log = Repository([])

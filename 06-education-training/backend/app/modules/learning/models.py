from pydantic import BaseModel, Field

from app.core.common import Repository, days


class EnrollIn(BaseModel):
    name: str = Field(min_length=2, default="Alex Morgan")


class QuizSubmission(BaseModel):
    answers: list[int]


PASS_MARK = 70

# The demo learner's enrollments, keyed by course slug. completed = lesson ids.
enrollments = Repository([
    {"slug": "excel-data-analysis-masterclass", "learner": "Alex Morgan", "enrolled": days(-12), "completed": [1, 2, 3, 4], "quiz": None},
    {"slug": "gdpr-data-protection-essentials", "learner": "Alex Morgan", "enrolled": days(-30), "completed": [1, 2, 3, 4, 5, 6], "quiz": {"score": 100, "passed": True}},
], key="slug")

certificates = Repository([
    {"id": "BP-7F3K-2026", "learner": "Alex Morgan", "course": "GDPR & Data Protection Essentials", "slug": "gdpr-data-protection-essentials",
     "score": 100, "issued": days(-28), "instructor": "Thomas Keller", "hours": 4.5},
])

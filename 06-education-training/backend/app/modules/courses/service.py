from fastapi import HTTPException

from app.modules.courses.models import courses, instructors


def card(c: dict) -> dict:
    return {k: v for k, v in c.items() if k not in ("lessons", "outcomes")} | {
        "lessons_count": len(c["lessons"]), "instructor": instructors.get(c["instructor_id"])["name"]}


def catalog(q: str | None = None, category: str | None = None, level: str | None = None) -> list[dict]:
    rows = courses.all()
    if q:
        rows = [c for c in rows if q.lower() in (c["title"] + c["category"]).lower()]
    if category:
        rows = [c for c in rows if c["category"] == category]
    if level:
        rows = [c for c in rows if c["level"] == level]
    return [card(c) for c in rows]


def detail(slug: str) -> dict:
    c = courses.get_or_404(slug)
    return c | {"instructor": instructors.get(c["instructor_id"])}


def by_id(course_id: int) -> dict:
    c = next((c for c in courses.all() if c["id"] == course_id), None)
    if not c:
        raise HTTPException(404, "Course not found")
    return c

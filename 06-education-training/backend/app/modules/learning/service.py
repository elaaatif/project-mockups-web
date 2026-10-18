"""Learner flow: enroll → complete lessons → pass the assessment → certificate."""
import secrets

from fastapi import HTTPException

from app.core.common import days
from app.modules.courses.models import QUIZZES, courses, instructors
from app.modules.learning.models import PASS_MARK, certificates, enrollments


def progress(e: dict) -> dict:
    c = courses.get_or_404(e["slug"])
    pct = round(len(e["completed"]) / len(c["lessons"]) * 100)
    cert = next((x for x in certificates.all() if x["slug"] == e["slug"]), None)
    return e | {"title": c["title"], "image": c["image"], "category": c["category"], "lessons_total": len(c["lessons"]),
                "progress": pct, "certificate_id": cert["id"] if cert else None}


def my_courses() -> list[dict]:
    return [progress(e) for e in enrollments.all()]


def enroll(slug: str, name: str) -> dict:
    courses.get_or_404(slug)
    existing = enrollments.get(slug)
    if existing:
        return progress(existing)
    return progress(enrollments.add({"slug": slug, "learner": name, "enrolled": days(0), "completed": [], "quiz": None}))


def _enrollment(slug: str) -> dict:
    e = enrollments.get(slug)
    if not e:
        raise HTTPException(403, "Enroll in this course first")
    return e


def complete_lesson(slug: str, lesson_id: int) -> dict:
    e = _enrollment(slug)
    if lesson_id not in e["completed"]:
        e["completed"].append(lesson_id)
    return progress(e)


def quiz(slug: str) -> dict:
    c = courses.get_or_404(slug)
    return {"pass_mark": PASS_MARK, "questions": [{"id": i, "q": q, "options": opts} for i, (q, opts, _) in enumerate(QUIZZES[c["category"]])]}


def submit_quiz(slug: str, answers: list[int]) -> dict:
    e = _enrollment(slug)
    c = courses.get_or_404(slug)
    if len(e["completed"]) < len(c["lessons"]):
        raise HTTPException(400, "Finish all lessons before taking the assessment")
    key = QUIZZES[c["category"]]
    if len(answers) != len(key):
        raise HTTPException(400, "Answer every question")
    results = [{"correct": a == k[2], "answer": k[2]} for a, k in zip(answers, key)]
    score = round(sum(r["correct"] for r in results) / len(key) * 100)
    passed = score >= PASS_MARK
    e["quiz"] = {"score": score, "passed": passed}
    cert = None
    if passed:
        cert = next((x for x in certificates.all() if x["slug"] == slug), None) or certificates.add({
            "id": f"BP-{secrets.token_hex(2).upper()}-2026", "learner": e["learner"], "course": c["title"], "slug": slug,
            "score": score, "issued": days(0), "instructor": instructors.get(c["instructor_id"])["name"], "hours": c["hours"]})
    return {"score": score, "passed": passed, "pass_mark": PASS_MARK, "results": results, "certificate": cert}


def verify(cert_id: str) -> dict:
    cert = certificates.get(cert_id.strip().upper())
    if not cert:
        raise HTTPException(404, "No certificate with that ID")
    return cert

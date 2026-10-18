from fastapi import APIRouter

from app.modules.learning import service
from app.modules.learning.models import EnrollIn, QuizSubmission

router = APIRouter(prefix="/learning", tags=["Learning, Assessments & Certificates"])


@router.get("/my-courses")
def my_courses():
    return service.my_courses()


@router.post("/{slug}/enroll")
def enroll(slug: str, body: EnrollIn):
    return service.enroll(slug, body.name)


@router.get("/{slug}/progress")
def progress(slug: str):
    return service.progress(service._enrollment(slug))


@router.post("/{slug}/lessons/{lesson_id}/complete")
def complete(slug: str, lesson_id: int):
    return service.complete_lesson(slug, lesson_id)


@router.get("/{slug}/quiz")
def quiz(slug: str):
    return service.quiz(slug)


@router.post("/{slug}/quiz")
def submit(slug: str, body: QuizSubmission):
    return service.submit_quiz(slug, body.answers)


@router.get("/certificates/{cert_id}")
def verify(cert_id: str):
    return service.verify(cert_id)

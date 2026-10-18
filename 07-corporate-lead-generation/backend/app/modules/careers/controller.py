from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.common import days
from app.modules.careers.models import applications, jobs

router = APIRouter(prefix="/careers", tags=["Recruitment Portal"])
ALLOWED = (".pdf", ".doc", ".docx")


@router.get("/jobs")
def list_jobs(department: str | None = None, q: str | None = None):
    rows = jobs.all()
    if department:
        rows = [j for j in rows if j["department"] == department]
    if q:
        rows = [j for j in rows if q.lower() in (j["title"] + j["location"]).lower()]
    return {"jobs": rows, "departments": sorted({j["department"] for j in jobs.all()})}


@router.get("/jobs/{slug}")
def job(slug: str):
    return jobs.get_or_404(slug)


@router.post("/jobs/{slug}/apply", status_code=201)
async def apply(slug: str, name: str = Form(min_length=2), email: str = Form(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"),
                phone: str = Form(""), linkedin: str = Form(""), cover: str = Form(""), cv: UploadFile = File(...)):
    j = jobs.get_or_404(slug)
    if not (cv.filename or "").lower().endswith(ALLOWED):
        raise HTTPException(400, "CV must be a PDF or Word document")
    content = await cv.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(413, "CV must be under 5 MB")
    a = applications.add({"id": len(applications.rows) + 1, "job_id": j["id"], "job_title": j["title"], "name": name, "email": email,
                          "phone": phone, "linkedin": linkedin, "cover": cover, "cv_name": cv.filename, "status": "new", "created": days(0), "rating": None})
    return {"reference": f"APP-{a['id']:04d}", "job": j["title"]}

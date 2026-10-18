from fastapi import APIRouter, HTTPException, UploadFile

from app.modules.extraction import service
from app.modules.extraction.models import SAMPLES, history

router = APIRouter(prefix="/extraction", tags=["Document Extraction"])
MAX_BYTES = 15 * 1024 * 1024


@router.get("/samples")
def samples():
    return {"samples": SAMPLES, "history": history.all()}


@router.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(413, "File larger than 15 MB")
    return service.extract(file.filename or "document.pdf", content)


@router.post("/sample/{name}")
def run_sample(name: str):
    sample = next((s for s in SAMPLES if s["name"] == name), None)
    if not sample:
        raise HTTPException(404, "Unknown sample")
    return service.extract(sample["name"], size_kb=sample["size_kb"])

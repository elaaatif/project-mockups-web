"""Vertex API — entry point. Modules register themselves in app/modules/__init__.py."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules import ROUTERS

app = FastAPI(title="Vertex Industrial — Corporate API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

for router in ROUTERS:
    app.include_router(router, prefix="/api")


@app.get("/api/health", tags=["System"])
def health():
    return {"status": "ok"}

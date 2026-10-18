"""Smoke-test a backend: imports the app and calls every GET route without path params.

Usage:  .venv\\Scripts\\python.exe tools\\smoke_test.py 01-business-management-saas
"""
import sys
from pathlib import Path

project = Path(__file__).resolve().parent.parent / sys.argv[1] / "backend"
sys.path.insert(0, str(project))

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

client = TestClient(app)
failed = 0
for path, ops in app.openapi()["paths"].items():
    if "get" in ops and "{" not in path:
        r = client.get(path)
        if r.status_code == 422:  # route needs query params — not a failure
            print(f"SKIP {path} (requires parameters)")
            continue
        ok = r.status_code == 200
        failed += not ok
        print(f"{'OK ' if ok else 'ERR'} {r.status_code} {path}" + ("" if ok else f"  {r.text[:200]}"))
print("FAILED" if failed else "ALL GOOD")
sys.exit(1 if failed else 0)

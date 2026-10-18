"""Runs tools/smoke_test.py against every project backend. Usage: python tools/smoke_all.py"""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
failed = []
for project in sorted(p.name for p in root.iterdir() if p.is_dir() and p.name[:2].isdigit() and (p / "backend").exists()):
    r = subprocess.run([sys.executable, "-W", "ignore", str(root / "tools" / "smoke_test.py"), project], capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or ["no output"])[-1]
    print(f"{project:34} {last}")
    if r.returncode:
        failed.append(project)
        print(r.stdout + r.stderr)
sys.exit(1 if failed else 0)

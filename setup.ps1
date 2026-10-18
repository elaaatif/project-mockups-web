# One-time setup: Python virtualenv for all FastAPI backends + npm workspaces for all Vue frontends.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path ".venv")) { python -m venv .venv }
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
npm install
Write-Host "`nSetup complete. Run .\start.ps1 1  (or 2..7, or 'all')" -ForegroundColor Green

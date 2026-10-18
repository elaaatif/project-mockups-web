# Autom8 — AI automation platform

AI customer support, PDF data extraction, automated reports and email/WhatsApp workflows in one console.

**Problem:** Teams lose hundreds of hours a month answering the same questions, retyping documents and assembling reports.

**Revenue model:** Setup fee + monthly platform subscription

## Features
- Live chatbot with intent detection, entity extraction & human handoff
- Drag-and-drop document extraction with confidence scores, CSV & JSON
- Generated KPI reports with charts and a written AI summary
- Scheduled delivery by email, Slack or WhatsApp
- Visual workflow builder with step-by-step test runs
- ROI dashboard (hours saved vs. cost)

## Run it
```powershell
# from the repository root (after .\setup.ps1)
.\start.ps1 2
```
- Website: http://localhost:5172  (admin dashboard at `/app`)
- API docs (Swagger): http://localhost:8002/docs

Or manually:
```powershell
cd backend;  ..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8002
cd frontend; npm run dev
```

## Modular MVC structure
```
backend/
  main.py                  app factory — registers every module router under /api
  app/core/common.py       shared helpers + in-memory Repository (swap for a real DB here)
  app/modules/<feature>/
    models.py              MODEL      — Pydantic schemas + seed data/repository
    service.py             business logic (no HTTP)
    controller.py          CONTROLLER — FastAPI routes calling the service
frontend/src/
  core/                    http client, toasts, resource helpers, formatting
  components/ui/           shared UI kit (Modal, StatCard, StatusBadge…)
  layouts/                 SiteLayout (public) · AppLayout (dashboard)
  router/                  auto-loads every modules/*/routes.js
  modules/<feature>/       VIEW — views/*.vue, <feature>.service.js, routes.js
```
Backend modules: `overview`, `chatbot`, `extraction`, `reports`, `workflows`, `pricing`

### Add a feature
1. Backend: create `app/modules/<name>/{models,service,controller}.py` and add the router to `app/modules/__init__.py`.
2. Frontend: create `src/modules/<name>/routes.js` (+ views and a service). Routes register automatically;
   add `meta: { layout: 'app', nav: { label, icon, order } }` to show it in the dashboard sidebar.

> Demo data lives in memory and resets when the API restarts.

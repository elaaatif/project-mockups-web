# Brightpath — Education & training platform

Online courses with a lesson player, graded assessments and verifiable certificates — plus corporate and school admin.

**Problem:** Training providers need to sell courses, prove completion and administer cohorts without three separate tools.

**Revenue model:** Course sales, subscriptions and institutional licences

## Features
- Course catalogue, detail pages and enrolment
- Lesson player with progress tracking
- Graded final assessment with pass mark
- Printable certificates with public verification ID
- Employee training: assign by team, compliance %, reminders
- Training-centre admin: timetable, attendance & fees

## Run it
```powershell
# from the repository root (after .\setup.ps1)
.\start.ps1 6
```
- Website: http://localhost:5176  (admin dashboard at `/app`)
- API docs (Swagger): http://localhost:8006/docs

Or manually:
```powershell
cd backend;  ..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8006
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
Backend modules: `catalog`, `learning`, `training`, `academy`

### Add a feature
1. Backend: create `app/modules/<name>/{models,service,controller}.py` and add the router to `app/modules/__init__.py`.
2. Frontend: create `src/modules/<name>/routes.js` (+ views and a service). Routes register automatically;
   add `meta: { layout: 'app', nav: { label, icon, order } }` to show it in the dashboard sidebar.

> Demo data lives in memory and resets when the API restarts.

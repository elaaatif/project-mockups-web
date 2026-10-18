# Vertex Industrial — Corporate lead-generation website

An industrial manufacturer's website with a spec-sheet catalogue, multi-step RFQ, careers portal and a leads CRM.

**Problem:** B2B websites often look like brochures and generate few, unqualified enquiries.

**Revenue model:** One-time project + hosting, maintenance & SEO retainers

## Features
- Product catalogue with technical specs & certifications
- 3-step quote wizard with automatic lead scoring
- Recruitment portal with CV upload
- CRM: RFQs, contact inbox & applicant pipeline
- Per-page SEO, JSON-LD (Organization/Product/JobPosting) and a live sitemap.xml

## Run it
```powershell
# from the repository root (after .\setup.ps1)
.\start.ps1 7
```
- Website: http://localhost:5177  (admin dashboard at `/app`)
- API docs (Swagger): http://localhost:8007/docs

Or manually:
```powershell
cd backend;  ..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8007
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
Backend modules: `site`, `products`, `quote`, `careers`, `crm`

### Add a feature
1. Backend: create `app/modules/<name>/{models,service,controller}.py` and add the router to `app/modules/__init__.py`.
2. Frontend: create `src/modules/<name>/routes.js` (+ views and a service). Routes register automatically;
   add `meta: { layout: 'app', nav: { label, icon, order } }` to show it in the dashboard sidebar.

> Demo data lives in memory and resets when the API restarts.

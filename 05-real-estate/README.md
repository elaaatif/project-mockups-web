# Haven — Real estate platform

Property listings with an interactive map, viewing bookings, instant valuations, an agent CRM and rental management.

**Problem:** Agencies juggle portals, spreadsheets and phone calls to turn browsers into qualified leads.

**Revenue model:** Paid listings, agency subscriptions and lead fees

## Features
- Search with filters and a synced Leaflet price-pin map
- Property pages with gallery, mortgage & stamp-duty calculator
- Viewing booking against the agent's real availability
- Instant valuation that creates a scored CRM lead
- Drag-and-drop lead pipeline for agents
- Rent ledger, arrears and maintenance tickets for landlords

## Run it
```powershell
# from the repository root (after .\setup.ps1)
.\start.ps1 5
```
- Website: http://localhost:5175  (admin dashboard at `/app`)
- API docs (Swagger): http://localhost:8005/docs

Or manually:
```powershell
cd backend;  ..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8005
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
Backend modules: `listings`, `valuation`, `agent`, `rentals`

### Add a feature
1. Backend: create `app/modules/<name>/{models,service,controller}.py` and add the router to `app/modules/__init__.py`.
2. Frontend: create `src/modules/<name>/routes.js` (+ views and a service). Routes register automatically;
   add `meta: { layout: 'app', nav: { label, icon, order } }` to show it in the dashboard sidebar.

> Demo data lives in memory and resets when the API restarts.

# Bookly — Booking & reservation platform

A marketplace for clinics, dentists, restaurants, salons, repair shops and trainers with real-time availability.

**Problem:** Phone-based booking wastes staff time, causes double bookings and no-shows.

**Revenue model:** Business subscriptions or a per-booking fee

## Features
- Slot engine that respects opening hours, durations and staff conflicts
- Restaurant table booking by party size & seating area
- Deposits for high-value services
- Customer self-service: view, add to calendar (.ics), cancel
- Owner calendar by staff column with live 'now' line
- Check-in / complete / no-show workflow & KPIs

## Run it
```powershell
# from the repository root (after .\setup.ps1)
.\start.ps1 4
```
- Website: http://localhost:5174  (admin dashboard at `/app`)
- API docs (Swagger): http://localhost:8004/docs

Or manually:
```powershell
cd backend;  ..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8004
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
Backend modules: `marketplace`, `bookings`, `owner`, `plans`

### Add a feature
1. Backend: create `app/modules/<name>/{models,service,controller}.py` and add the router to `app/modules/__init__.py`.
2. Frontend: create `src/modules/<name>/routes.js` (+ views and a service). Routes register automatically;
   add `meta: { layout: 'app', nav: { label, icon, order } }` to show it in the dashboard sidebar.

> Demo data lives in memory and resets when the API restarts.

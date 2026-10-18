# Mercato — E-commerce store & wholesale portal

A design-led online shop with cart & checkout, order tracking, a tiered wholesale portal and quotation requests.

**Problem:** Brands need to sell to consumers and businesses from one catalogue without running two systems.

**Revenue model:** Build fee, maintenance retainer and integrations

## Features
- Catalogue with filters, sorting & product pages
- Persistent cart drawer and 3-step checkout
- Order tracking timeline by order number + email
- Wholesale price list with 15/25/35% tiers and Net 30 terms
- B2B quote requests with instant tier estimate
- Admin: orders pipeline, inventory & restocking

## Run it
```powershell
# from the repository root (after .\setup.ps1)
.\start.ps1 3
```
- Website: http://localhost:5173  (admin dashboard at `/app`)
- API docs (Swagger): http://localhost:8003/docs

Or manually:
```powershell
cd backend;  ..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8003
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
Backend modules: `catalog`, `cart`, `orders`, `wholesale`, `quotes`, `admin`

### Add a feature
1. Backend: create `app/modules/<name>/{models,service,controller}.py` and add the router to `app/modules/__init__.py`.
2. Frontend: create `src/modules/<name>/routes.js` (+ views and a service). Routes register automatically;
   add `meta: { layout: 'app', nav: { label, icon, order } }` to show it in the dashboard sidebar.

> Demo data lives in memory and resets when the API restarts.

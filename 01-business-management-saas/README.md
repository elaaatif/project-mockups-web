# OpsFlow — Business management system (B2B SaaS)

An operations platform that replaces spreadsheets for inventory, invoicing, purchasing, HR, payroll, fleet and document approvals.

**Problem:** SMEs run recurring operations across disconnected spreadsheets — stock-outs, late invoices, lost approvals and manual payroll.

**Revenue model:** Monthly or annual subscriptions, setup fees and support contracts

## Features
- Live stock levels with reorder alerts
- Purchase orders that update stock on receipt
- Invoices with overdue tracking & preview
- Leave approvals + one-click payroll with tax & social deductions
- Fleet service intervals & insurance renewals
- 3-step document approval chain with audit trail
- Monthly/annual plans, setup fees & support contracts

## Run it
```powershell
# from the repository root (after .\setup.ps1)
.\start.ps1 1
```
- Website: http://localhost:5171  (admin dashboard at `/app`)
- API docs (Swagger): http://localhost:8001/docs

Or manually:
```powershell
cd backend;  ..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8001
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
Backend modules: `dashboard`, `inventory`, `invoices`, `purchasing`, `hr`, `fleet`, `documents`, `billing`

### Add a feature
1. Backend: create `app/modules/<name>/{models,service,controller}.py` and add the router to `app/modules/__init__.py`.
2. Frontend: create `src/modules/<name>/routes.js` (+ views and a service). Routes register automatically;
   add `meta: { layout: 'app', nav: { label, icon, order } }` to show it in the dashboard sidebar.

> Demo data lives in memory and resets when the API restarts.

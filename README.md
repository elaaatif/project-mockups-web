# MOCKETS — 7 business website demos + a portfolio

Eight working web apps, all built on **one stack**: **Vue 3 + Vite + Tailwind CSS** on the front end and **FastAPI** on the back end.
They share one modular MVC structure, so each project is easy to understand, extend and reuse for clients.

| # | Folder | Brand | What it demonstrates | Revenue model |
|---|--------|-------|----------------------|---------------|
| 1 | `01-business-management-saas` | **OpsFlow** | Inventory, invoicing, purchasing, HR & leave, payroll, fleet/maintenance/insurance, document approvals | Subscriptions, setup fees, support contracts |
| 2 | `02-ai-automation` | **Autom8** | AI support chatbot, PDF/document extraction, automated reports, email & WhatsApp workflows | Setup fee + monthly platform |
| 3 | `03-ecommerce` | **Mercato** | Online shop, cart & checkout, order tracking, wholesale portal, quotation requests, inventory | Build fee, maintenance, integrations |
| 4 | `04-booking-reservations` | **Bookly** | Clinics/dentists, restaurants, salons, repair shops, trainers: live slots, deposits, staff calendar | Subscription or per-booking fee |
| 5 | `05-real-estate` | **Haven** | Listings + map, viewings, instant valuation (lead gen), agent CRM pipeline, rental management | Paid listings, subscriptions, lead fees |
| 6 | `06-education-training` | **Brightpath** | Courses, lesson player, assessments, verifiable certificates, employee training, school admin | Course sales, subscriptions, licences |
| 7 | `07-corporate-lead-generation` | **Vertex Industrial** | Company site, industrial catalogue, RFQ wizard with lead scoring, recruitment portal, CRM, SEO | Project + hosting/maintenance/SEO |
| 8 | `08-portfolio` | **Your portfolio** | Showcases all seven, with live status, case studies, packages, estimate calculator, contact inbox | — |

## Quick start (Windows / PowerShell)

Requirements: **Python 3.11+** and **Node 18+**.

```powershell
.\setup.ps1          # once: creates .venv, installs FastAPI deps and all npm workspaces
.\start.ps1 all      # starts all 8 APIs + websites and opens the portfolio
.\start.ps1 3        # …or just one project (here: e-commerce)
```

| Project | Website | API docs |
|---|---|---|
| 01 SaaS | http://localhost:5171 | http://localhost:8001/docs |
| 02 AI | http://localhost:5172 | http://localhost:8002/docs |
| 03 E-commerce | http://localhost:5173 | http://localhost:8003/docs |
| 04 Booking | http://localhost:5174 | http://localhost:8004/docs |
| 05 Real estate | http://localhost:5175 | http://localhost:8005/docs |
| 06 Education | http://localhost:5176 | http://localhost:8006/docs |
| 07 Corporate | http://localhost:5177 | http://localhost:8007/docs |
| **08 Portfolio** | **http://localhost:5178** | http://localhost:8008/docs |

Every site has a public side plus an admin/dashboard side at **`/app`**.

## Architecture: modular MVC

```
NN-project/
├─ backend/                        FastAPI
│  ├─ main.py                      app factory, mounts every module under /api
│  └─ app/
│     ├─ core/common.py            shared helpers + in-memory Repository
│     └─ modules/<feature>/
│        ├─ models.py              M — Pydantic schemas + data/repository
│        ├─ service.py             business rules (pricing, slots, scoring…)
│        └─ controller.py          C — HTTP routes
└─ frontend/                       Vue 3 + Vite + Tailwind v4
   └─ src/
      ├─ app.config.js             brand name, logo, demo user — per project
      ├─ core/                     http client, toasts, useResource/act, formatting
      ├─ components/ui/            shared UI kit
      ├─ layouts/                  SiteLayout (public) · AppLayout (dashboard)
      ├─ router/                   auto-registers every modules/*/routes.js
      └─ modules/<feature>/        V — views/, <feature>.service.js, routes.js
```

**Adding a feature** takes two folders: `backend/app/modules/<name>/` (then register its router in `app/modules/__init__.py`) and
`frontend/src/modules/<name>/routes.js`. Frontend routes load automatically. Set `meta.layout: 'app'` and `meta.nav` to put a page in the dashboard sidebar.

**Going to production:** each module's data lives in a `Repository` inside `models.py`. Replace it with SQLAlchemy/PostgreSQL and the services and controllers stay unchanged.

## Libraries used
Vue 3 · Vue Router · Tailwind CSS v4 · Chart.js (vue-chartjs) · Lucide icons · Leaflet (real-estate map) · FastAPI · Pydantic · Uvicorn · python-multipart (file uploads)

## Personalise the portfolio
Edit **`08-portfolio/backend/app/modules/profile/models.py`**: name, headline, email, links, skills, packages and testimonials.
Screenshots live in `08-portfolio/frontend/public/screens/`.

## Tooling
```powershell
npm run build:all     # production build of every frontend
npm run smoke:all     # calls every GET endpoint of every backend
```
`tools/` also contains `scaffold.sh` (copies the shared core into a new project) and `shoot.sh` (headless-Chrome screenshots).

> All data is demo data held in memory, so it resets when an API restarts. Photos are loaded from Unsplash; map tiles come from OpenStreetMap.

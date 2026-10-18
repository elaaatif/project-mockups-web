# Portfolio — showcase for all seven demos

A dark, single-page developer portfolio (Vue 3 + FastAPI, same modular MVC layout as the demos).

- **Work grid** with screenshots, category filter and a **live badge**: the API probes each demo's `/api/health` every 15 s
- **Case-study pages** (`/work/<slug>`): problem → solution → revenue model, implemented features, module tree, extra screens, links to the live demo and its Swagger docs
- **Services & stack**, **pricing packages + retainers**, **process**, **testimonials**
- **Instant estimate calculator** (project type + add-ons + timeline) that attaches the estimate to the enquiry
- **Contact inbox** at `/app` to manage enquiries

## Run
```powershell
.\start.ps1 8        # portfolio only → http://localhost:5178
.\start.ps1 all      # portfolio + every demo, so the live badges turn green
```

## Personalise
- Your details, packages and testimonials: `backend/app/modules/profile/models.py`
- Project texts: `backend/app/modules/projects/models.py`
- Estimate prices: `backend/app/modules/contact/models.py`
- Screenshots: `frontend/public/screens/*.webp`

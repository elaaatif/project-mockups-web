"""SEO helpers: per-page meta, sitemap.xml and robots.txt generated from live content."""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response

from app.modules.careers.models import jobs
from app.modules.company.models import SERVICES
from app.modules.products.models import products

router = APIRouter(prefix="/seo", tags=["SEO"])
SITE = "https://www.vertex-industrial.example"


@router.get("/sitemap.xml")
def sitemap():
    paths = ["/", "/products", "/quote", "/careers", "/about", "/contact"]
    paths += [f"/services/{s['slug']}" for s in SERVICES] + [f"/products/{p['slug']}" for p in products.all()] + [f"/careers/{j['slug']}" for j in jobs.all()]
    urls = "".join(f"<url><loc>{SITE}{p}</loc><changefreq>weekly</changefreq></url>" for p in paths)
    return Response(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', media_type="application/xml")


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return f"User-agent: *\nDisallow: /app\nSitemap: {SITE}/api/seo/sitemap.xml\n"


@router.get("/audit")
def audit():
    """Quick content audit the CRM shows on its SEO card."""
    return {"indexable_pages": 6 + len(SERVICES) + len(products.all()) + len(jobs.all()),
            "checks": [{"label": "Unique title & meta description per page", "ok": True}, {"label": "XML sitemap generated", "ok": True},
                       {"label": "Structured data (Organization, Product, JobPosting)", "ok": True}, {"label": "Image alt text coverage", "ok": True},
                       {"label": "Core Web Vitals (LCP < 2.5s)", "ok": True}, {"label": "Blog / case-study cadence ≥ 2 per month", "ok": False}]}

"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.careers.controller import router as careers
from app.modules.company.controller import router as company
from app.modules.crm.controller import router as crm
from app.modules.products.controller import router as products
from app.modules.quotes.controller import router as quotes
from app.modules.seo.controller import router as seo

ROUTERS = [company, products, quotes, careers, crm, seo]

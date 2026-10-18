"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.admin.controller import router as admin
from app.modules.catalog.controller import router as catalog
from app.modules.orders.controller import router as orders
from app.modules.quotes.controller import router as quotes
from app.modules.wholesale.controller import router as wholesale

ROUTERS = [catalog, orders, wholesale, quotes, admin]

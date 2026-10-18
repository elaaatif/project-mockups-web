"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.billing.controller import router as billing
from app.modules.dashboard.controller import router as dashboard
from app.modules.documents.controller import router as documents
from app.modules.fleet.controller import router as fleet
from app.modules.hr.controller import router as hr
from app.modules.inventory.controller import router as inventory
from app.modules.invoices.controller import router as invoices
from app.modules.purchasing.controller import router as purchasing

ROUTERS = [dashboard, inventory, invoices, purchasing, hr, fleet, documents, billing]

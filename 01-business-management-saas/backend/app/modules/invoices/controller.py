from fastapi import APIRouter

from app.modules.invoices import service
from app.modules.invoices.models import CLIENTS, InvoiceIn

router = APIRouter(prefix="/invoices", tags=["Invoicing"])


@router.get("")
def index(status: str | None = None):
    return {"invoices": service.list_invoices(status), "summary": service.summary(), "clients": CLIENTS}


@router.post("", status_code=201)
def store(body: InvoiceIn):
    return service.create(body)


@router.patch("/{invoice_id}/pay")
def pay(invoice_id: str):
    return service.mark_paid(invoice_id)

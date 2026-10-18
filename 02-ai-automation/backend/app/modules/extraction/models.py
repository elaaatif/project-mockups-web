from app.core.common import Repository

DOC_TYPES = {
    "invoice": ["vendor", "invoice_number", "invoice_date", "due_date", "subtotal", "tax", "total", "iban"],
    "receipt": ["merchant", "date", "payment_method", "subtotal", "tax", "total"],
    "contract": ["party_a", "party_b", "effective_date", "term", "governing_law", "renewal"],
    "purchase_order": ["buyer", "supplier", "po_number", "delivery_date", "total"],
}
LABELS = {
    "vendor": "Vendor", "invoice_number": "Invoice #", "invoice_date": "Invoice date", "due_date": "Due date",
    "subtotal": "Subtotal", "tax": "Tax", "total": "Total", "iban": "IBAN", "merchant": "Merchant", "date": "Date",
    "payment_method": "Payment method", "party_a": "Party A", "party_b": "Party B", "effective_date": "Effective date",
    "term": "Term", "governing_law": "Governing law", "renewal": "Auto-renewal", "buyer": "Buyer",
    "supplier": "Supplier", "po_number": "PO #", "delivery_date": "Delivery date",
}
SAMPLES = [
    {"name": "acme-invoice-0042.pdf", "type": "invoice", "size_kb": 184},
    {"name": "uber-receipt-oct.pdf", "type": "receipt", "size_kb": 62},
    {"name": "msa-northwind-2026.pdf", "type": "contract", "size_kb": 940},
    {"name": "po-77812-metalco.pdf", "type": "purchase_order", "size_kb": 211},
]
history = Repository([])

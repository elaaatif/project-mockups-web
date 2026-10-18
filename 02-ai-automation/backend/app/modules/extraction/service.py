"""Document extraction pipeline (simulated OCR + field extraction).

Text-based files are scanned with regexes for real values; binary files get deterministic
synthetic values seeded by the file name, so the same file always returns the same result."""
import hashlib
import re
from random import Random

from app.core.common import days
from app.modules.extraction.models import DOC_TYPES, LABELS, history

COMPANIES = ["Acme Industrial GmbH", "Northwind Traders", "Metalco Supply Ltd", "Bluewave Retail", "Helix Pharma AG"]


def detect_type(filename: str, text: str) -> str:
    probe = (filename + " " + text[:2000]).lower()
    for key, words in {"receipt": ["receipt", "uber", "pos"], "contract": ["contract", "agreement", "msa", "nda"],
                       "purchase_order": ["po-", "purchase order", "po_"]}.items():
        if any(w in probe for w in words):
            return key
    return "invoice"


def _synthetic(field: str, r: Random) -> str:
    amount = r.uniform(400, 18000)
    values = {
        "vendor": r.choice(COMPANIES), "merchant": r.choice(["Uber BV", "Starbucks", "Shell", "Amazon EU"]),
        "invoice_number": f"INV-{r.randint(1000, 9999)}", "po_number": f"PO-{r.randint(70000, 79999)}",
        "invoice_date": days(-r.randint(2, 20)), "date": days(-r.randint(1, 9)), "due_date": days(r.randint(10, 40)),
        "delivery_date": days(r.randint(5, 30)), "effective_date": days(-r.randint(10, 60)),
        "subtotal": f"${amount:,.2f}", "tax": f"${amount * 0.2:,.2f}", "total": f"${amount * 1.2:,.2f}",
        "iban": f"DE{r.randint(10, 99)} 5001 0517 {r.randint(1000, 9999)} {r.randint(1000, 9999)} 00",
        "payment_method": r.choice(["Visa •••• 4242", "Mastercard •••• 8812", "Apple Pay"]),
        "party_a": "Northstar Ltd", "party_b": r.choice(COMPANIES), "term": r.choice(["12 months", "24 months", "36 months"]),
        "governing_law": r.choice(["England & Wales", "Germany", "Delaware, USA"]), "renewal": r.choice(["Yes, 60-day notice", "No"]),
        "buyer": "Northstar Ltd", "supplier": r.choice(COMPANIES),
    }
    return values[field]


def _from_text(field: str, text: str) -> str | None:
    patterns = {
        "total": r"total[^\d$€£]*([$€£]?\s?[\d,]+\.\d{2})", "invoice_number": r"(inv[-\s#]?\d{3,})",
        "invoice_date": r"(\d{4}-\d{2}-\d{2})", "date": r"(\d{4}-\d{2}-\d{2})", "iban": r"\b([A-Z]{2}\d{2}(?:\s?\d{4}){3,})",
    }
    if field in patterns and (m := re.search(patterns[field], text, re.I)):
        return m.group(1)
    return None


def extract(filename: str, content: bytes = b"", size_kb: int | None = None) -> dict:
    text = content.decode("utf-8", errors="ignore") if content else ""
    seed = int(hashlib.md5(filename.encode()).hexdigest(), 16)
    r = Random(seed)
    doc_type = detect_type(filename, text)
    fields = []
    for key in DOC_TYPES[doc_type]:
        found = _from_text(key, text) if text else None
        fields.append({"key": key, "label": LABELS[key], "value": found or _synthetic(key, r),
                       "confidence": round(r.uniform(0.97, 0.995) if found else r.uniform(0.82, 0.99), 3)})
    by_key = {f["key"]: f for f in fields}
    if "total" in by_key and "subtotal" in by_key and by_key["total"]["confidence"] > 0.97:  # real total → derive the rest
        total = float(re.sub(r"[^\d.]", "", by_key["total"]["value"]) or 0)
        by_key["subtotal"]["value"] = f"${total / 1.2:,.2f}"
        by_key["tax"]["value"] = f"${total - total / 1.2:,.2f}"
    line_items = []
    if doc_type in ("invoice", "purchase_order", "receipt"):
        for desc in r.sample(["Consulting hours", "Steel brackets", "Shipping & handling", "Software licence", "On-site support", "Packaging"], 3):
            qty, price = r.randint(1, 40), round(r.uniform(12, 480), 2)
            line_items.append({"description": desc, "qty": qty, "unit_price": price, "amount": round(qty * price, 2)})
    result = {
        "id": len(history.rows) + 1, "filename": filename, "doc_type": doc_type, "pages": r.randint(1, 6),
        "size_kb": size_kb or max(1, len(content) // 1024), "processing_ms": r.randint(900, 2600),
        "fields": fields, "line_items": line_items,
        "avg_confidence": round(sum(f["confidence"] for f in fields) / len(fields), 3),
        "needs_review": [f["label"] for f in fields if f["confidence"] < 0.88],
    }
    history.add({k: result[k] for k in ("id", "filename", "doc_type", "pages", "avg_confidence")} | {"processed_at": days(0)})
    return result

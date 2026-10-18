from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng


class DocumentIn(BaseModel):
    title: str = Field(min_length=3)
    type: str
    owner: str = "You"


class Decision(BaseModel):
    decision: Literal["approve", "reject"]
    comment: str = ""


DOC_TYPES = ["Contract", "Policy", "Purchase Request", "Expense Claim"]
APPROVAL_CHAIN = [("Department Head", "Amira Haddad"), ("Finance", "Lucas Moreau"), ("Director", "Grace Liu")]


def make_steps(progress: int, rejected: bool = False) -> list[dict]:
    steps = []
    for i, (role, person) in enumerate(APPROVAL_CHAIN):
        status = "approved" if i < progress else "pending"
        if rejected and i == progress:
            status = "rejected"
        steps.append({"role": role, "approver": person, "status": status,
                      "at": days(-progress + i) if status != "pending" else None, "comment": ""})
    return steps


_TITLES = [("Supplier Agreement — Metalco", "Contract"), ("Remote Work Policy v3", "Policy"),
           ("New Forklift Purchase", "Purchase Request"), ("Q3 Travel Expenses — Sales", "Expense Claim"),
           ("NDA — Helix Pharma", "Contract"), ("Warehouse Safety Policy", "Policy"),
           ("Laptop Refresh 2026", "Purchase Request")]
documents = Repository([
    {"id": i + 1, "title": t, "type": k, "owner": rng.choice(["Maya Patel", "Daniel Kim", "Layla Nasser"]),
     "created": days(-rng.randint(1, 40)), "size_kb": rng.randint(80, 2400),
     "steps": make_steps(p, rejected=(i == 4))}
    for i, ((t, k), p) in enumerate(zip(_TITLES, [0, 1, 2, 3, 1, 3, 0]))
])

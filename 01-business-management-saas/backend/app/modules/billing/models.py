PLANS = [
    {"id": "starter", "name": "Starter", "monthly": 49, "users": "Up to 5 users", "setup_fee": 0,
     "features": ["Inventory & invoicing", "Basic HR & leave", "Email support", "1 warehouse"]},
    {"id": "growth", "name": "Growth", "monthly": 129, "users": "Up to 25 users", "setup_fee": 490, "popular": True,
     "features": ["Everything in Starter", "Purchasing & approvals", "Payroll workflows", "Fleet tracking",
                  "Priority support"]},
    {"id": "enterprise", "name": "Enterprise", "monthly": 349, "users": "Unlimited users", "setup_fee": 1900,
     "features": ["Everything in Growth", "SSO & audit logs", "Custom workflows", "Dedicated success manager",
                  "99.9% SLA"]},
]
SUPPORT_CONTRACTS = [
    {"name": "Standard", "price": 0, "response": "Next business day", "channels": "Email"},
    {"name": "Business", "price": 199, "response": "4 hours", "channels": "Email + Chat"},
    {"name": "Premium", "price": 599, "response": "1 hour, 24/7", "channels": "Phone + Dedicated engineer"},
]
ANNUAL_DISCOUNT = 0.2

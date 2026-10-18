"""✏️  EDIT THIS FILE to personalise the portfolio — name, bio, contact links and packages."""

PROFILE = {
    "name": "Your Name",
    "initials": "YN",
    "role": "Full-stack developer · Vue.js + FastAPI",
    "headline": "I build business software that pays for itself.",
    "intro": "SaaS platforms, AI automations, online stores, booking systems and lead-generating websites — "
             "designed, built and maintained end-to-end with Vue.js and FastAPI.",
    "location": "Remote · working worldwide",
    "email": "hello@yourdomain.com",
    "links": {"github": "https://github.com/", "linkedin": "https://www.linkedin.com/", "upwork": "https://www.upwork.com/"},
    "available": True,
    "stats": [{"value": "7", "label": "production-grade demos"}, {"value": "40+", "label": "API endpoints shipped"},
              {"value": "100%", "label": "modular MVC codebases"}, {"value": "< 24h", "label": "reply time"}],
}

SKILLS = {
    "Frontend": ["Vue 3", "Vue Router", "Tailwind CSS", "Chart.js", "Leaflet maps", "Vite"],
    "Backend": ["FastAPI", "Pydantic", "REST API design", "File uploads", "Auth & roles", "PostgreSQL / SQLAlchemy"],
    "AI & automation": ["LLM integration", "Chatbots & intent detection", "Document extraction", "Email & WhatsApp workflows"],
    "Delivery": ["Modular MVC architecture", "Docker", "CI/CD", "SEO & Core Web Vitals", "Hosting & maintenance"],
}

PACKAGES = [
    {"name": "Launch", "price": 1500, "suffix": "from", "timeline": "1–2 weeks", "for": "Corporate & lead-gen websites",
     "features": ["Up to 8 pages", "Quote & contact forms → CRM", "SEO setup, sitemap & schema", "1 month of support"]},
    {"name": "Platform", "price": 6500, "suffix": "from", "timeline": "4–8 weeks", "for": "E-commerce, booking & real-estate platforms", "popular": True,
     "features": ["Public site + admin dashboard", "Payments, bookings or listings", "Role-based back office", "3 months of support"]},
    {"name": "SaaS / AI", "price": 12000, "suffix": "from", "timeline": "8–14 weeks", "for": "B2B SaaS & AI automation",
     "features": ["Multi-module MVC architecture", "AI chatbot / extraction / reports", "Subscriptions & billing", "SLA-backed support"]},
]
RETAINERS = [
    {"name": "Hosting & care", "price": 149, "features": ["Managed hosting & backups", "Security updates", "Uptime monitoring"]},
    {"name": "Growth", "price": 690, "features": ["Everything in Care", "8 dev hours / month", "SEO & performance reports"]},
]

TESTIMONIALS = [
    {"quote": "The booking system cut our no-shows in half within the first month. Clean, fast and our staff learned it in a day.",
     "name": "Clinic owner", "company": "Dental practice, demo client"},
    {"quote": "Invoices that used to take our team hours are now extracted and posted to the ERP automatically.",
     "name": "Finance lead", "company": "Distribution company, demo client"},
    {"quote": "Our new site generates qualified RFQs every week — and they arrive already scored.",
     "name": "Sales director", "company": "Industrial manufacturer, demo client"},
]

import re

from app.core.common import Repository, rng


def unsplash(photo_id: str) -> str:
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop"


CATEGORIES = ["Data & Analytics", "Business & Leadership", "Technology", "Compliance", "Design"]

instructors = Repository([
    {"id": 1, "name": "Dr. Maya Chen", "title": "Data scientist, ex-Spotify", "photo": unsplash("1573496359142-b8d87734a5a2"), "students": 48200},
    {"id": 2, "name": "Marcus Webb", "title": "Leadership coach", "photo": unsplash("1507003211169-0a1dd7228f2d"), "students": 31500},
    {"id": 3, "name": "Priya Raman", "title": "Senior software engineer", "photo": unsplash("1494790108377-be9c29b29330"), "students": 22900},
    {"id": 4, "name": "Thomas Keller", "title": "Compliance & risk lead", "photo": unsplash("1500648767791-00dcc994a43e"), "students": 61000},
])

_LESSON_TITLES = {
    "Data & Analytics": ["Why data matters", "Cleaning messy data", "Pivot tables in depth", "Lookups & joins", "Charts that tell a story", "Building a dashboard", "Automating with macros"],
    "Business & Leadership": ["The manager mindset", "Running effective 1:1s", "Giving feedback", "Delegation frameworks", "Leading through change", "Hiring well"],
    "Technology": ["Setting up your environment", "Python syntax essentials", "Working with files", "APIs & JSON", "Testing your code", "Deploying a small app"],
    "Compliance": ["What GDPR covers", "Lawful bases for processing", "Data subject rights", "Spotting a breach", "Phishing & social engineering", "Reporting incidents"],
    "Design": ["Design thinking", "User research basics", "Wireframing", "Visual hierarchy", "Prototyping in Figma", "Usability testing"],
}

QUIZZES = {
    "Data & Analytics": [
        ("Which Excel feature summarises large tables by category?", ["VLOOKUP", "Pivot table", "Conditional formatting", "Freeze panes"], 1),
        ("XLOOKUP improves on VLOOKUP because it…", ["Is faster to type", "Can look left and returns exact match by default", "Works only on numbers", "Needs sorted data"], 1),
        ("Which chart is best for showing a trend over time?", ["Pie chart", "Line chart", "Scatter plot", "Treemap"], 1),
        ("Before analysing data you should first…", ["Add colours", "Clean and validate it", "Print it", "Delete duplicates blindly"], 1),
    ],
    "Business & Leadership": [
        ("The main purpose of a 1:1 is…", ["Status updates", "The report's growth and blockers", "Performance reviews only", "Small talk"], 1),
        ("Good feedback is…", ["Vague and kind", "Specific, timely and actionable", "Given once a year", "Always public"], 1),
        ("Delegation works best when you…", ["Keep the outcome unclear", "Agree the outcome and level of autonomy", "Micromanage each step", "Delegate only boring tasks"], 1),
        ("During change, leaders should…", ["Communicate early and often", "Wait until everything is final", "Avoid questions", "Change everything at once"], 0),
    ],
    "Technology": [
        ("Which keyword defines a function in Python?", ["func", "def", "function", "lambda only"], 1),
        ("JSON stands for…", ["Java Syntax Object Notation", "JavaScript Object Notation", "Joint Standard Object Network", "None of these"], 1),
        ("Automated tests help you…", ["Ship bugs faster", "Change code with confidence", "Avoid writing docs", "Skip code review"], 1),
        ("An HTTP 404 status means…", ["Server error", "Not found", "Unauthorised", "OK"], 1),
    ],
    "Compliance": [
        ("Under GDPR, a personal data breach must usually be reported to the regulator within…", ["24 hours", "72 hours", "7 days", "30 days"], 1),
        ("Which is a lawful basis for processing?", ["Curiosity", "Legitimate interests", "Convenience", "Marketing preference"], 1),
        ("A phishing email often…", ["Creates urgency and asks for credentials", "Comes from your manager's verified account", "Has no links", "Is always in another language"], 0),
        ("If you suspect a breach you should…", ["Ignore it", "Report it immediately via the incident process", "Fix it quietly", "Email all customers"], 1),
    ],
    "Design": [
        ("Design thinking starts with…", ["Empathy for users", "Choosing fonts", "Writing code", "Pricing"], 0),
        ("A wireframe is…", ["The final visual design", "A low-fidelity layout sketch", "A database diagram", "A marketing plan"], 1),
        ("Visual hierarchy guides users by…", ["Random placement", "Size, contrast and spacing", "Using only one colour", "Hiding navigation"], 1),
        ("Usability testing involves…", ["Watching real users attempt tasks", "Asking the CEO's opinion", "A/B testing only", "Reading analytics only"], 0),
    ],
}

_SEED = [
    ("Excel & Data Analysis Masterclass", "Data & Analytics", "Beginner", 89, "1434030216411-0b793f4b4173", 1, True),
    ("SQL for Business Analysts", "Data & Analytics", "Intermediate", 99, "1531482615713-2afd69097998", 1, False),
    ("First-Time Manager Bootcamp", "Business & Leadership", "Beginner", 129, "1552664730-d307ca884978", 2, True),
    ("Leading Remote & Hybrid Teams", "Business & Leadership", "Intermediate", 109, "1600880292203-757bb62b4baf", 2, False),
    ("Python Programming from Zero", "Technology", "Beginner", 119, "1517336714731-489689fd1ca8", 3, True),
    ("Building APIs with FastAPI", "Technology", "Advanced", 149, "1556761175-b413da4baf72", 3, False),
    ("GDPR & Data Protection Essentials", "Compliance", "Beginner", 49, "1517245386807-bb43f82c33c4", 4, False),
    ("Cyber Security Awareness 2026", "Compliance", "Beginner", 39, "1581091226825-a6a2a5aee158", 4, True),
    ("UX Design Fundamentals", "Design", "Beginner", 99, "1522202176988-66273c2fd55f", 3, False),
]


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


courses = Repository([
    {
        "id": i + 1, "slug": _slug(title), "title": title, "category": cat, "level": level, "price": price, "image": unsplash(img),
        "instructor_id": inst, "bestseller": best, "rating": round(rng.uniform(4.5, 4.9), 1), "reviews": rng.randint(300, 9000),
        "students": rng.randint(2000, 60000), "hours": len(_LESSON_TITLES[cat]) * 0.75,
        "summary": f"A practical, project-based course that takes you from the basics to confident, job-ready skills in {cat.lower()}.",
        "outcomes": ["Apply the core techniques at work immediately", "Complete a real-world capstone project", "Earn a verifiable certificate", "Lifetime access to updates"],
        "lessons": [{"id": j + 1, "title": t, "minutes": rng.choice([6, 8, 11, 14, 18]), "type": "video" if j % 3 else "reading"} for j, t in enumerate(_LESSON_TITLES[cat])],
    }
    for i, (title, cat, level, price, img, inst, best) in enumerate(_SEED)
], key="slug")

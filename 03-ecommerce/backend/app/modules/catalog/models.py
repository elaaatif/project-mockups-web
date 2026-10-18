import re

from app.core.common import Repository, rng


def unsplash(photo_id: str) -> str:
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop"


CATEGORIES = [
    {"slug": "audio-tech", "name": "Audio & Tech"},
    {"slug": "watches", "name": "Watches"},
    {"slug": "footwear", "name": "Footwear"},
    {"slug": "accessories", "name": "Accessories"},
    {"slug": "home", "name": "Home & Living"},
    {"slug": "beauty", "name": "Beauty"},
]

# Wholesale price breaks applied to every product (min quantity → discount)
WHOLESALE_TIERS = [(10, 0.15), (50, 0.25), (200, 0.35)]

_SEED = [
    ("Aura Wireless Headphones", "audio-tech", 189, "1505740420928-5e560c06d30e", "Bestseller", "40-hour battery, adaptive noise cancelling and plush memory-foam cushions."),
    ("Pulse Portable Speaker", "audio-tech", 129, "1608043152269-423dbba4e7e1", None, "Waterproof IP67 speaker with 360° sound and 20-hour playtime."),
    ("Snap Instant Camera", "audio-tech", 119, "1526170375885-4d8ecf77b99f", "New", "Retro instant camera with auto-exposure and built-in flash."),
    ("Nimbus Pro Laptop 14\"", "audio-tech", 1499, "1517336714731-489689fd1ca8", None, "Featherweight aluminium laptop with an all-day battery and a 3K display."),
    ("Minimal White Watch", "watches", 149, "1523275335684-37898b6baf30", None, "Clean Scandinavian dial, sapphire glass, silicone strap."),
    ("Heritage Chronograph", "watches", 329, "1542496658-e33a6d0d50f6", "Limited", "Swiss-movement chronograph with a leather strap and 100m water resistance."),
    ("Orbit Smartwatch S2", "watches", 279, "1546868871-7041f2a55e12", None, "Health tracking, GPS and a 2-day battery in an aluminium case."),
    ("Velocity Runner", "footwear", 139, "1542291026-7eec264c27ff", "Bestseller", "Responsive foam runner with a breathable knit upper."),
    ("Stride Trainer Grey", "footwear", 119, "1491553895911-0055eca6402d", None, "Everyday trainer with a cushioned midsole and grippy outsole."),
    ("Oxford Suede Brogue", "footwear", 169, "1560343090-f0409e92791a", None, "Hand-finished suede brogue on a durable rubber sole."),
    ("Wayfarer Sunglasses", "accessories", 89, "1572635196237-14b3f281503f", None, "Polarised lenses with UV400 protection in an acetate frame."),
    ("Commuter Backpack 22L", "accessories", 99, "1553062407-98eeb64c6a62", "New", "Water-resistant backpack with a padded 16\" laptop sleeve."),
    ("Arc Floor Lamp", "home", 159, "1507473885765-e6ed057f782c", None, "Matte steel floor lamp with an adjustable shade, E27 bulb."),
    ("Oak Bar Stool", "home", 79, "1503602642458-232111445657", None, "Solid oak stool with a whitewash finish, 65cm seat height."),
    ("Emerald Velvet Sofa", "home", 1290, "1555041469-a586c61ea9bc", "Bestseller", "Three-seat velvet sofa with walnut legs and feather cushions."),
    ("Noir Eau de Parfum", "beauty", 112, "1585386959984-a4155224a1ad", None, "Warm amber and vanilla fragrance, 100ml."),
    ("Daily Renewal Cream", "beauty", 42, "1556228578-8c89e6adf883", "New", "Lightweight moisturiser with niacinamide and hyaluronic acid."),
]


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


products = Repository([
    {
        "id": i + 1, "slug": _slug(name), "name": name, "category": cat, "price": price,
        "compare_at": round(price * 1.25) if i % 4 == 0 else None, "image": unsplash(photo), "badge": badge,
        "description": desc, "rating": round(rng.uniform(4.1, 4.9), 1), "reviews": rng.randint(18, 640),
        "stock": 0 if i == 3 else 9 if i % 7 == 2 else rng.choice([120, 260, 480, 900]), "sku": f"MC-{2000 + i}",
        "moq_wholesale": 10,
    }
    for i, (name, cat, price, photo, badge, desc) in enumerate(_SEED)
], key="slug")

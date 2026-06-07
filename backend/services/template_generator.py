"""
Generates 1000+ unique reel templates by combining categories,
color schemes, font styles, and visual variants.
"""

# ── Category definitions ───────────────────────────────────────────────────────
CATEGORIES = [
    {"key": "motivational",  "name": "Motivational",    "emoji": "🔥"},
    {"key": "gaming",        "name": "Gaming",           "emoji": "🎮"},
    {"key": "spiritual",     "name": "Spiritual",        "emoji": "✨"},
    {"key": "business",      "name": "Business",         "emoji": "💼"},
    {"key": "luxury",        "name": "Luxury",           "emoji": "👑"},
    {"key": "fitness",       "name": "Fitness",          "emoji": "💪"},
    {"key": "love",          "name": "Love & Romance",   "emoji": "❤️"},
    {"key": "travel",        "name": "Travel",           "emoji": "✈️"},
    {"key": "food",          "name": "Food & Cooking",   "emoji": "🍕"},
    {"key": "education",     "name": "Education",        "emoji": "📚"},
    {"key": "comedy",        "name": "Comedy",           "emoji": "😂"},
    {"key": "horror",        "name": "Horror",           "emoji": "💀"},
    {"key": "nature",        "name": "Nature",           "emoji": "🌿"},
    {"key": "music",         "name": "Music",            "emoji": "🎵"},
    {"key": "fashion",       "name": "Fashion",          "emoji": "👗"},
    {"key": "crypto",        "name": "Crypto / Web3",    "emoji": "₿"},
    {"key": "mindset",       "name": "Mindset",          "emoji": "🧠"},
    {"key": "sports",        "name": "Sports",           "emoji": "⚽"},
    {"key": "art",           "name": "Art & Creative",   "emoji": "🎨"},
    {"key": "tech",          "name": "Tech & AI",        "emoji": "🤖"},
    {"key": "wealth",        "name": "Wealth & Money",   "emoji": "💰"},
    {"key": "health",        "name": "Health & Wellness","emoji": "🧘"},
    {"key": "news",          "name": "News & Media",     "emoji": "📰"},
    {"key": "kids",          "name": "Kids & Fun",       "emoji": "🎉"},
    {"key": "dark",          "name": "Dark Aesthetic",   "emoji": "🖤"},
    {"key": "neon",          "name": "Neon Vibes",       "emoji": "💡"},
    {"key": "vintage",       "name": "Vintage",          "emoji": "📷"},
    {"key": "minimalist",    "name": "Minimalist",       "emoji": "◻️"},
    {"key": "aesthetic",     "name": "Aesthetic",        "emoji": "🌸"},
    {"key": "quotes",        "name": "Daily Quotes",     "emoji": "💬"},
]

# ── Color schemes: (bg_hex, text_hex, box_hex@alpha) ─────────────────────────
COLOR_SCHEMES = [
    {"name": "Black Gold",    "bg": "0a0800", "text": "FFD700", "box": "8B6914@0.8"},
    {"name": "Dark Fire",     "bg": "0f0500", "text": "FF4500", "box": "8B2500@0.8"},
    {"name": "Neon Green",    "bg": "050f05", "text": "00FF41", "box": "006400@0.8"},
    {"name": "Purple Haze",   "bg": "0d0015", "text": "BF5FFF", "box": "5B0080@0.8"},
    {"name": "Ice Blue",      "bg": "020d1a", "text": "00BFFF", "box": "00507a@0.8"},
    {"name": "Rose Gold",     "bg": "1a0a0d", "text": "FFB6C1", "box": "8B3a3a@0.8"},
    {"name": "Ocean Deep",    "bg": "00101e", "text": "00E5FF", "box": "005566@0.8"},
    {"name": "Lava",          "bg": "1a0000", "text": "FF6B35", "box": "8B2500@0.7"},
    {"name": "Matrix",        "bg": "000f00", "text": "00FF00", "box": "003300@0.9"},
    {"name": "Midnight",      "bg": "080820", "text": "E0E0FF", "box": "2a2a6e@0.8"},
    {"name": "Sunset",        "bg": "1a0520", "text": "FFB347", "box": "8B4513@0.8"},
    {"name": "Arctic",        "bg": "0a1520", "text": "FFFFFF", "box": "1a4a6e@0.8"},
    {"name": "Crimson",       "bg": "0f0005", "text": "DC143C", "box": "5a0010@0.8"},
    {"name": "Emerald",       "bg": "001a0a", "text": "50C878", "box": "006633@0.8"},
    {"name": "Bronze",        "bg": "0f0800", "text": "CD7F32", "box": "5a3500@0.8"},
    {"name": "Violet Storm",  "bg": "0a0015", "text": "9370DB", "box": "3a0066@0.8"},
    {"name": "Coral",         "bg": "1a0a08", "text": "FF6B6B", "box": "8B2a2a@0.8"},
    {"name": "Cyan Pulse",    "bg": "00101a", "text": "00FFFF", "box": "004455@0.8"},
    {"name": "Electric Blue", "bg": "000515", "text": "007FFF", "box": "00205a@0.8"},
    {"name": "Lime Pop",      "bg": "050f00", "text": "BFFF00", "box": "3a5500@0.8"},
    {"name": "Peach",         "bg": "1a0d08", "text": "FFCBA4", "box": "8B4513@0.7"},
    {"name": "Teal Glow",     "bg": "001515", "text": "20B2AA", "box": "004444@0.8"},
    {"name": "Snow White",    "bg": "0d0d0d", "text": "FFFFFF", "box": "333333@0.8"},
    {"name": "Amber Alert",   "bg": "0f0a00", "text": "FFBF00", "box": "664400@0.8"},
    {"name": "Lavender",      "bg": "0d0a1a", "text": "E6E6FA", "box": "44336e@0.8"},
    {"name": "Ruby",          "bg": "0f0005", "text": "E0115F", "box": "5a0022@0.8"},
    {"name": "Steel",         "bg": "0a0d0f", "text": "B0C4DE", "box": "2a3a4a@0.8"},
    {"name": "Copper",        "bg": "0f0800", "text": "B87333", "box": "5a3300@0.8"},
    {"name": "Magenta",       "bg": "0f0010", "text": "FF00FF", "box": "5a0055@0.8"},
    {"name": "Forest",        "bg": "050f05", "text": "228B22", "box": "0a3300@0.8"},
    {"name": "Deep Sea",      "bg": "000d1a", "text": "1E90FF", "box": "003366@0.8"},
    {"name": "Phantom",       "bg": "050505", "text": "C0C0C0", "box": "1a1a1a@0.9"},
    {"name": "Sakura",        "bg": "1a0a10", "text": "FFB7C5", "box": "7a2a44@0.8"},
    {"name": "Gold Rush",     "bg": "0a0700", "text": "FFC300", "box": "664d00@0.8"},
    {"name": "Cobalt",        "bg": "00050f", "text": "0047AB", "box": "001a44@0.8"},
]

# ── Style variants (affects font size, box border, layout feel) ───────────────
STYLE_VARIANTS = [
    {"name": "Bold",      "font_size_mod": 0,   "boxborderw": 20, "suffix": "Bold"},
    {"name": "Clean",     "font_size_mod": -8,  "boxborderw": 12, "suffix": "Clean"},
    {"name": "Massive",   "font_size_mod": 12,  "boxborderw": 28, "suffix": "Massive"},
    {"name": "Compact",   "font_size_mod": -16, "boxborderw": 8,  "suffix": "Compact"},
    {"name": "Cinematic", "font_size_mod": -4,  "boxborderw": 16, "suffix": "Cinematic"},
]

BASE_FONT_SIZE = 68


def generate_all_templates() -> list[dict]:
    """
    Generate all templates by combining categories × color_schemes × style_variants.
    Total = 30 × 35 × 5 = 5,250 templates.
    """
    templates = []
    for cat in CATEGORIES:
        for scheme in COLOR_SCHEMES:
            for style in STYLE_VARIANTS:
                tid = f"{cat['key']}__{scheme['name'].lower().replace(' ', '_')}__{style['suffix'].lower()}"
                templates.append({
                    "id": tid,
                    "name": f"{cat['name']} · {scheme['name']} · {style['name']}",
                    "category": cat["key"],
                    "category_label": cat["name"],
                    "color_scheme": scheme["name"],
                    "style": style["name"],
                    "description": f"{cat['name']} style with {scheme['name']} colors",
                    "bg_color": scheme["bg"],
                    "text_color": scheme["text"],
                    "box_color": scheme["box"],
                    "font_size": BASE_FONT_SIZE + style["font_size_mod"],
                    "boxborderw": style["boxborderw"],
                    "emoji": cat["emoji"],
                })
    return templates


# Pre-generated at import time
ALL_TEMPLATES = generate_all_templates()

# Lookup dict for fast access by id
TEMPLATE_MAP = {t["id"]: t for t in ALL_TEMPLATES}


def get_template_by_id(template_id: str) -> dict:
    """Get a template by id, fallback to first motivational template."""
    return TEMPLATE_MAP.get(template_id, ALL_TEMPLATES[0])


def get_categories() -> list[dict]:
    return CATEGORIES


def get_color_schemes() -> list[dict]:
    return [{"name": s["name"]} for s in COLOR_SCHEMES]


def get_styles() -> list[dict]:
    return [{"name": s["name"]} for s in STYLE_VARIANTS]

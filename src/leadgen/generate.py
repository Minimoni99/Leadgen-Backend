from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
QUERY_FILE = BASE_DIR / "seeds" / "queries.txt"

CATEGORIES = [
    "dentist",
    "plumber",
    "roofing contractor",
    "law firm",
    "marketing agency",
    "HVAC service",
    "electrician",
    "accountant",
    "landscaping",
    "exterminator",
]
CITIES = [
    "Austin, TX",
    "Dallas, TX",
    "Houston, TX",
    "San Antonio, TX",
    "Fort Worth, TX",
]


def generate_queries(categories=None, cities=None):
    categories = categories or CATEGORIES
    cities = cities or CITIES
    for category in categories:
        for city in cities:
            yield f"{category} in {city}"


def write_queries(path: Path, queries):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        for query in queries:
            f.write(f"{query}\n")

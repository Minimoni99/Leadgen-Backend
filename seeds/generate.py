import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
QUERY_FILE = BASE_DIR / "queries.txt"

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


def generate_queries(categories, cities):
    for category in categories:
        for city in cities:
            yield f"{category} in {city}"


def write_queries(path, queries):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for query in queries:
            writer.writerow([query])


def main():
    queries = list(generate_queries(CATEGORIES, CITIES))
    write_queries(QUERY_FILE, queries)
    print(f"Generated {len(queries)} queries to {QUERY_FILE}")


if __name__ == "__main__":
    main()

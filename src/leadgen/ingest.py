from pathlib import Path
from typing import Iterator

from .db import connect
from .scraper import read_scraper_rows


def import_leads(csv_path: Path, source: str = "scraper") -> int:
    inserted = 0
    with connect() as conn:
        with conn.cursor() as cur:
            for row in read_scraper_rows(csv_path):
                cur.execute(
                    """
                    INSERT INTO leads (source, category, city, name, address, phone, website, scraped_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        source,
                        row.get("category"),
                        row.get("city"),
                        row.get("name"),
                        row.get("address"),
                        row.get("phone"),
                        row.get("website"),
                        row.get("scraped_at"),
                    ),
                )
                lead_id = cur.fetchone()[0]
                for email in row.get("emails", []):
                    cur.execute(
                        """
                        INSERT INTO emails (lead_id, email, label, source)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (lead_id, email, row.get("email_label"), source),
                    )
                inserted += 1
        conn.commit()
    return inserted


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Import lead CSV into Postgres.")
    parser.add_argument("csv_path", type=Path, help="Path to the scraper CSV file.")
    parser.add_argument("--source", default="scraper", help="Source label for imported leads.")
    args = parser.parse_args()

    count = import_leads(args.csv_path, source=args.source)
    print(f"Imported {count} leads from {args.csv_path}")

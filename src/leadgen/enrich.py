import re
from typing import Optional

from .db import connect

PHONE_CLEAN_RE = re.compile(r"[^\d+\n]+")
URL_CLEAN_RE = re.compile(r"^(https?://)", re.IGNORECASE)


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    if not phone:
        return None
    cleaned = PHONE_CLEAN_RE.sub("", phone.strip())
    if len(cleaned) < 7:
        return None
    return cleaned


def normalize_website(website: Optional[str]) -> Optional[str]:
    if not website:
        return None
    value = website.strip()
    if not value:
        return None
    if not URL_CLEAN_RE.match(value):
        value = f"https://{value}"
    return value


def get_pending_leads(batch_size: int = 100):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, source, category, city, name, address, phone, website, scraped_at
                FROM leads
                WHERE id NOT IN (SELECT lead_id FROM lead_enrichment)
                ORDER BY id ASC
                LIMIT %s
                """,
                (batch_size,),
            )
            for row in cur.fetchall():
                yield row


def save_enrichment(lead_id: int, phone: Optional[str], website: Optional[str], notes: Optional[str] = None):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO lead_enrichment (lead_id, normalized_phone, normalized_website, notes, enrichment_source)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (lead_id) DO UPDATE SET
                    normalized_phone = EXCLUDED.normalized_phone,
                    normalized_website = EXCLUDED.normalized_website,
                    notes = EXCLUDED.notes,
                    enrichment_source = EXCLUDED.enrichment_source,
                    enriched_at = now()
                """,
                (
                    lead_id,
                    phone,
                    website,
                    notes,
                    "local-normalizer",
                ),
            )
        conn.commit()


def get_enrichment_stats() -> dict:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM leads")
            total = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM lead_enrichment")
            enriched = cur.fetchone()[0]
            pending = total - enriched
    return {"total": total, "enriched": enriched, "pending": pending}


def enrich_batch(batch_size: int = 100) -> int:
    count = 0
    for lead in get_pending_leads(batch_size=batch_size):
        normalized_phone = normalize_phone(lead[6])
        normalized_website = normalize_website(lead[7])
        notes = []
        if not normalized_phone:
            notes.append("phone_malformed")
        if not normalized_website:
            notes.append("website_missing")
        save_enrichment(
            lead[0],
            normalized_phone,
            normalized_website,
            ", ".join(notes) if notes else None,
        )
        count += 1
    return count


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Enrich pending leads.")
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    enriched = enrich_batch(batch_size=args.batch_size)
    print(f"Enriched {enriched} leads")

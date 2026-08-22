import csv
import re
from pathlib import Path
from typing import Iterator, Optional

FIELD_MAP = {
    "business_name": "name",
    "name": "name",
    "company": "name",
    "location_name": "name",
    "address": "address",
    "location": "address",
    "street": "address",
    "phone": "phone",
    "phone_number": "phone",
    "tel": "phone",
    "telephone": "phone",
    "website": "website",
    "url": "website",
    "email": "email",
    "email_address": "email",
    "emails": "email",
    "contact_email": "email",
    "email_label": "email_label",
    "email_type": "email_label",
    "category": "category",
    "industry": "category",
    "city": "city",
    "location_city": "city",
    "scraped_at": "scraped_at",
    "timestamp": "scraped_at",
    "date": "scraped_at",
    "extracted_at": "scraped_at",
}

EMAIL_SPLIT_RE = re.compile(r"[;,\n]+")


def normalize_value(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def parse_email_list(value: Optional[str]) -> list[str]:
    if not value:
        return []
    emails = [item.strip() for item in EMAIL_SPLIT_RE.split(value) if item.strip()]
    return emails


def canonical_field_name(raw_name: str) -> Optional[str]:
    if raw_name is None:
        return None
    return FIELD_MAP.get(raw_name.strip().lower())


def normalize_row(raw_row: dict) -> dict:
    normalized: dict = {}
    email_values: list[str] = []

    for raw_key, raw_value in raw_row.items():
        if raw_key is None:
            continue
        field_name = canonical_field_name(raw_key)
        if field_name is None:
            continue

        value = normalize_value(raw_value)
        if value is None:
            continue

        if field_name == "email":
            email_values.extend(parse_email_list(value))
        else:
            normalized[field_name] = value

    if email_values:
        unique_emails = []
        seen = set()
        for email in email_values:
            lower = email.lower()
            if lower not in seen:
                seen.add(lower)
                unique_emails.append(email)
        normalized["emails"] = unique_emails
        normalized.setdefault("email", unique_emails[0])

    return normalized


def read_scraper_rows(csv_path: Path) -> Iterator[dict]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield normalize_row(row)

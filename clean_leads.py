import csv
import re

INPUT_FILE = "output/results.csv"
OUTPUT_FILE = "output/clean_leads.csv"

JUNK_DOMAINS = {"domain.com", "example.com", "sentry.wixpress.com", "sentry-next.wixpress.com"}
JUNK_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def find_column(fieldnames, keyword):
    for f in fieldnames:
        if keyword.lower() in f.lower():
            return f
    return None

def is_valid_email(email):
    email = email.strip().lower()
    if not EMAIL_PATTERN.match(email):
        return False
    if any(email.endswith(ext) for ext in JUNK_EXTENSIONS):
        return False
    domain = email.split("@")[-1]
    if domain in JUNK_DOMAINS:
        return False
    return True

with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    name_col = find_column(reader.fieldnames, "title") or find_column(reader.fieldnames, "name")
    email_col = find_column(reader.fieldnames, "email")
    phone_col = find_column(reader.fieldnames, "phone")

    if not name_col or not email_col:
        print(f"Could not find expected columns. Found: {reader.fieldnames}")
        raise SystemExit(1)

    seen_emails = set()
    clean_rows = []

    for row in reader:
        raw_emails = (row.get(email_col) or "").strip()
        name = (row.get(name_col) or "").strip()
        phone = (row.get(phone_col) or "").strip() if phone_col else ""

        if not raw_emails:
            continue

        # a row may contain multiple comma-separated emails; keep the first valid one
        candidates = [e.strip() for e in raw_emails.split(",")]
        valid_email = next((e for e in candidates if is_valid_email(e)), None)

        if not valid_email:
            continue
        if valid_email.lower() in seen_emails:
            continue

        seen_emails.add(valid_email.lower())
        clean_rows.append({"name": name, "email": valid_email, "phone": phone})

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "email", "phone"])
    writer.writeheader()
    writer.writerows(clean_rows)

print(f"Done. {len(clean_rows)} unique, valid leads written to {OUTPUT_FILE}")
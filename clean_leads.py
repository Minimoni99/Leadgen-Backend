import csv

INPUT_FILE = "output/results.csv"
OUTPUT_FILE = "output/clean_leads.csv"

def find_column(fieldnames, keyword):
    for f in fieldnames:
        if keyword.lower() in f.lower():
            return f
    return None

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
        email = (row.get(email_col) or "").strip()
        name = (row.get(name_col) or "").strip()
        phone = (row.get(phone_col) or "").strip() if phone_col else ""

        if not email or "@" not in email:
            continue
        if email.lower() in seen_emails:
            continue

        seen_emails.add(email.lower())
        clean_rows.append({"name": name, "email": email, "phone": phone})

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "email", "phone"])
    writer.writeheader()
    writer.writerows(clean_rows)

print(f"Done. {len(clean_rows)} unique leads written to {OUTPUT_FILE}")
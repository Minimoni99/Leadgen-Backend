from leadgen.scraper import normalize_row, parse_email_list


def test_parse_email_list_splits_multiple_values():
    value = "a@example.com; b@example.com\nc@example.com"
    emails = parse_email_list(value)
    assert emails == ["a@example.com", "b@example.com", "c@example.com"]


def test_normalize_row_maps_fields_and_deduplicates_emails():
    raw_row = {
        "Business_Name": "Acme Plumbing",
        "address": "123 Main St",
        "Phone": "512-555-0101",
        "emails": "info@acme.com; INFO@acme.com",
        "category": "plumber",
        "city": "Austin, TX",
    }

    normalized = normalize_row(raw_row)

    assert normalized["name"] == "Acme Plumbing"
    assert normalized["address"] == "123 Main St"
    assert normalized["phone"] == "512-555-0101"
    assert normalized["category"] == "plumber"
    assert normalized["city"] == "Austin, TX"
    assert normalized["emails"] == ["info@acme.com"]
    assert normalized["email"] == "info@acme.com"

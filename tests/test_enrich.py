from leadgen.enrich import normalize_phone, normalize_website


def test_normalize_phone_strips_formatting():
    assert normalize_phone("(512) 555-0101") == "5125550101"
    assert normalize_phone("+1 512-555-0101") == "+15125550101"
    assert normalize_phone("123") is None


def test_normalize_website_adds_scheme():
    assert normalize_website("example.com") == "https://example.com"
    assert normalize_website("http://example.com") == "http://example.com"
    assert normalize_website("") is None

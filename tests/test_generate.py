from leadgen.generate import generate_queries, CATEGORIES, CITIES


def test_generate_queries_count():
    queries = list(generate_queries())
    assert len(queries) == len(CATEGORIES) * len(CITIES)


def test_generate_queries_sample():
    queries = list(generate_queries(["dentist"], ["Austin, TX"]))
    assert queries == ["dentist in Austin, TX"]

from django_filter_drf_camel_case.filters import OrderingFilter


def test_it_creates_camel_case_ordering_keys():
    filter = OrderingFilter()
    normalized_fields = filter.normalize_fields(("created_at", "updatedAt", "title"))

    expected = {
        "created_at": "createdAt",
        "updatedAt": "updatedAt",
        "title": "title",
    }

    assert normalized_fields == expected

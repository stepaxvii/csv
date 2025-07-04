import pytest

from csv_processor import filter_rows, aggregate_rows

TEST_DATA = [
    {"name": "iphone", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi", "brand": "xiaomi", "price": "199", "rating": "4.6"},
]


def test_filter_equal_text():
    result = filter_rows(TEST_DATA, "brand=apple")
    assert len(result) == 1
    assert result[0]["name"] == "iphone"


def test_filter_greater_than():
    result = filter_rows(TEST_DATA, "price>1000")
    assert len(result) == 1
    assert result[0]["name"] == "galaxy"


def test_aggregate_avg():
    result = aggregate_rows(TEST_DATA, "price=avg")
    assert result == pytest.approx((999 + 1199 + 199) / 3, 0.1)


def test_aggregate_max():
    result = aggregate_rows(TEST_DATA, "price=max")
    assert result == 1199

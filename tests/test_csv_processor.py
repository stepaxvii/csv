import pytest

from csv_processor import (
    filter_rows, 
    aggregate_rows, 
    sort_rows,
    CSVProcessingError,
    UnsupportedOperationError,
    InvalidConditionError,
    ColumnNotFoundError
)


@pytest.fixture
def test_data():
    """Фикстура с тестовыми данными."""
    return [
        {"name": "iphone", "brand": "apple", "price": "999", "rating": "4.9"},
        {"name": "galaxy", "brand": "samsung", "price": "1199", "rating": "4.8"},
        {"name": "redmi", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    ]


@pytest.mark.parametrize("condition,expected_count,expected_name", [
    ("brand=apple", 1, "iphone"),
    ("brand=xiaomi", 1, "redmi"),
    ("price>1000", 1, "galaxy"),
    ("price<500", 1, "redmi"),
    ("rating>4.7", 2, "iphone"),  # iphone и galaxy
])
def test_filter_rows(test_data, condition, expected_count, expected_name):
    """Тест фильтрации строк с различными условиями."""
    result = filter_rows(test_data, condition)
    assert len(result) == expected_count
    if expected_count == 1:
        assert result[0]["name"] == expected_name


@pytest.mark.parametrize("operation,expected", [
    ("price=avg", (999 + 1199 + 199) / 3),
    ("price=max", 1199),
    ("price=min", 199),
    ("price=median", 999.0),
    ("rating=max", 4.9),
    ("rating=min", 4.6),
])
def test_aggregate_operations(test_data, operation, expected):
    """Тест агрегатных операций."""
    result = aggregate_rows(test_data, operation)
    assert result == pytest.approx(expected, 0.1)


@pytest.mark.parametrize("column,reverse,expected_first", [
    ("rating", False, "redmi"),  # самый низкий рейтинг
    ("rating", True, "iphone"),  # самый высокий рейтинг
    ("price", False, "redmi"),   # самая низкая цена
    ("price", True, "galaxy"),   # самая высокая цена
    ("name", False, "galaxy"),   # по алфавиту
])
def test_sort_rows(test_data, column, reverse, expected_first):
    """Тест сортировки строк."""
    result = sort_rows(test_data, column, reverse)
    assert result[0]["name"] == expected_first


def test_invalid_condition():
    """Тест некорректного условия фильтрации."""
    with pytest.raises(InvalidConditionError):
        filter_rows([], "invalid_condition")


def test_unsupported_operation():
    """Тест неподдерживаемой операции."""
    with pytest.raises(UnsupportedOperationError):
        aggregate_rows([{"price": "100"}], "price=sum")


def test_empty_column():
    """Тест отсутствующего столбца."""
    with pytest.raises(ColumnNotFoundError):
        aggregate_rows([{"price": "not_number"}], "price=avg")


def test_filter_none_condition(test_data):
    """Тест фильтрации без условия."""
    result = filter_rows(test_data, None)
    assert result == test_data


def test_aggregate_none_condition():
    """Тест агрегации без условия."""
    result = aggregate_rows([], None)
    assert result is None

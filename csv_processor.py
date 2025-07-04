import csv
from typing import List, Dict, Optional


def read_csv(
    filepath: str
) -> Optional[List[Dict[str, str]]]:
    """Читаем CVS и возвращаем список строк."""
    try:
        with open(file=filepath, mode="r", encoding="utf-8") as csv_file:
            return list(csv.DictReader(csv_file))
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}.")
        return None


def filter_rows(
    rows: List[Dict[str, str]],
    condition: Optional[str]
) -> List[Dict[str, str]]:
    """Фильтруем строки по условию 'колонка=значение'."""

    if not condition:
        return rows
    if "=" in condition:
        column, value = condition.split("=")
        operator = "="
    elif ">" in condition:
        column, value = condition.split(">")
        operator = ">"
    elif "<" in condition:
        column, value = condition.split("<")
        operator = "<"
    else:
        raise ValueError(f"Неверный формат условия: {condition}.")

    filtered_products = []
    for row in rows:
        try:
            row_value = row[column.strip()]
            try:
                row_value = float(row_value)
                value_float = float(value.strip())
                if operator == "=" and row_value == value_float:
                    filtered_products.append(row)
                elif operator == ">" and row_value > value_float:
                    filtered_products.append(row)
                elif operator == "<" and row_value < value_float:
                    filtered_products.append(row)
            except ValueError:
                if operator == "=" and row_value.strip() == value.strip():
                    filtered_products.append(row)
        except KeyError:
            continue
    return filtered_products


def aggregate_rows(
    rows: List[Dict[str, str]],
    condition: Optional[str]
) -> Optional[float]:
    "Вычисляем агрегацию для столбца."
    if not condition:
        return None

    column, operation = condition.split("=")
    column = column.strip()
    operation = operation.strip().lower()

    values = []
    for row in rows:
        try:
            value = float(row[column])
            values.append(value)
        except (KeyError, ValueError):
            continue

    if not values:
        raise ValueError(f"Нет числовых значений в столбце {column}.")

    if operation == "avg":
        return round(sum(values) / len(values), 1)
    elif operation == "min":
        return min(values)
    elif operation == "max":
        return max(values)
    else:
        raise ValueError(f"Неизвестная операция: {operation}.")

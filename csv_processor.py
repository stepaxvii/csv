import csv
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class CSVProcessingError(Exception):
    """Базовое исключение для ошибок обработки CSV."""
    pass


class UnsupportedOperationError(CSVProcessingError):
    """Исключение для неподдерживаемых операций."""
    pass


class InvalidConditionError(CSVProcessingError):
    """Исключение для некорректных условий фильтрации."""
    pass


class ColumnNotFoundError(CSVProcessingError):
    """Исключение для отсутствующих столбцов."""
    pass


class Operation(ABC):
    """Абстрактный базовый класс для операций."""
    
    @abstractmethod
    def execute(self, values: List[float]) -> float:
        """Выполнить операцию над списком значений."""
        pass


class AverageOperation(Operation):
    """Операция вычисления среднего значения."""
    
    def execute(self, values: List[float]) -> float:
        return round(sum(values) / len(values), 1)


class MinOperation(Operation):
    """Операция поиска минимального значения."""
    
    def execute(self, values: List[float]) -> float:
        return min(values)


class MaxOperation(Operation):
    """Операция поиска максимального значения."""
    
    def execute(self, values: List[float]) -> float:
        return max(values)


class MedianOperation(Operation):
    """Операция вычисления медианы."""
    
    def execute(self, values: List[float]) -> float:
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 1:
            return sorted_values[n // 2]
        else:
            return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2


class OperationFactory:
    """Фабрика для создания операций."""
    
    _operations = {
        "avg": AverageOperation(),
        "min": MinOperation(),
        "max": MaxOperation(),
        "median": MedianOperation(),
    }
    
    @classmethod
    def get_operation(cls, operation_name: str) -> Operation:
        """Получить операцию по имени."""
        if operation_name not in cls._operations:
            available_ops = ", ".join(cls._operations.keys())
            raise UnsupportedOperationError(
                f"Неизвестная операция: {operation_name}. Доступные: {available_ops}."
            )
        return cls._operations[operation_name]


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
        raise InvalidConditionError(f"Неверный формат условия: {condition}.")

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
        raise ColumnNotFoundError(f"Нет числовых значений в столбце {column}.")

    # Используем фабрику операций
    operation_obj = OperationFactory.get_operation(operation)
    return operation_obj.execute(values)


def sort_rows(
    rows: List[Dict[str, str]],
    column: str,
    reverse: bool = False
) -> List[Dict[str, str]]:
    """Сортируем по определённому столбцу."""
    def get_key(row):
        value = row.get(column, "")
        try:
            return float(value)
        except ValueError:
            return str(value).lower()

    return sorted(rows, key=get_key, reverse=reverse)

# Обработчик CSV файлов

Консольная утилита для обработки CSV файлов с возможностью фильтрации и агрегации данных.

## Возможности

- Чтение CSV файлов
- Фильтрация строк по условиям
- Вычисление агрегированных значений (среднее, минимум, максимум) для столбцов

## Клонируйте репозиторий
bash
```
git clone git@github.com:stepaxvii/csv.git
```

## Создание и активация виртуального окруженоя
bash
```
python -m venv venv
source venv/Scripts/activate
```

## Установите зависимости
bash
```
pip install requirement.txt
```

## Пример использования CSV-файла `products.csv`
```
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
```

## - Чтение CSV-файла
bash
```
python main.py --file products.csv
```
### Вывод в терминал
```
name              brand      price    rating
----------------  -------  -------  --------
iphone 15 pro     apple        999       4.9
galaxy s23 ultra  samsung     1199       4.8
redmi note 12     xiaomi       199       4.6
poco x5 pro       xiaomi       299       4.4
```

## - Фильтрация по текстовому значению
bash
```
python main.py --file products.csv --where "brand=xiaomi"
```
### Вывод в терминал
```
name           brand      price    rating
-------------  -------  -------  --------
redmi note 12  xiaomi       199       4.6
poco x5 pro    xiaomi       299       4.4
```

## - Агрегация средней цены
bash
```
python main.py --file products.csv --aggregate "price=avg"
```
### Вывод в терминал
```
price=avg = 674.0
```

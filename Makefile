.PHONY: install format lint test clean help

# Установка зависимостей
install:
	pip install -r requirements.txt

# Форматирование кода
format:
	black .

# Проверка кода линтером
lint:
	flake8 .

# Запуск тестов
test:
	pytest -v

# Запуск тестов с покрытием
test-cov:
	pytest --cov=csv_processor --cov-report=html

# Очистка кэша и временных файлов
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Справка
help:
	@echo "Доступные команды:"
	@echo "  install   - установка зависимостей"
	@echo "  format    - форматирование кода"
	@echo "  lint      - проверка кода линтером"
	@echo "  test      - запуск тестов"
	@echo "  test-cov  - запуск тестов с покрытием"
	@echo "  clean     - очистка временных файлов"
	@echo "  help      - показать эту справку" 
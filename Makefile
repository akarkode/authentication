.PHONY: help install install-dev clean run migrate migrate-create db-upgrade lint format

help:
	@echo "Available commands:"
	@echo "  install           - Install production dependencies"
	@echo "  install-dev       - Install all dependencies including dev"
	@echo "  clean             - Remove test and build artifacts"
	@echo "  run               - Run the development server"
	@echo "  migrate           - Run database migrations"
	@echo "  migrate-create    - Create a new migration (use MSG='description')"
	@echo "  db-upgrade        - Upgrade database to latest migration"
	@echo "  lint              - Run linting (when configured)"
	@echo "  format            - Format code (when configured)"

install:
	poetry install --no-dev

install-dev:
	poetry install --with dev

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml .tox/ dist/ build/

run:
	poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

migrate:
	poetry run alembic upgrade head

migrate-create:
	@if [ -z "$(MSG)" ]; then \
		echo "Error: Please provide a migration message using MSG='your message'"; \
		exit 1; \
	fi
	poetry run alembic revision --autogenerate -m "$(MSG)"

db-upgrade:
	poetry run alembic upgrade head

lint:
	@echo "Run: poetry run ruff check ."
	@echo "Note: Add ruff to dev dependencies first"

format:
	@echo "Run: poetry run ruff format ."
	@echo "Note: Add ruff to dev dependencies first"

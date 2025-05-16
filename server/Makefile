.PHONY: server migrate migrate-create fmt lint test test-cov install-dev

server:
	uvicorn app.main:app --reload

migrate:
	PYTHONPATH=$$(pwd) alembic upgrade head

makemigrations:
	@read -p "Enter migration message: " message; \
	PYTHONPATH=$$(pwd) alembic revision --autogenerate -m "$$message"

fmt:
	uv run ruff check . --fix --unsafe-fixes
	uv run ruff format .
	uv run toml-sort pyproject.toml

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy .
	uv run toml-sort --check pyproject.toml

test:
	uv run pytest

install-dev-deps:
	uv sync --locked

install-deps:
	uv sync --locked --no-dev
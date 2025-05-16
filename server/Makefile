.PHONY: server migrate migrate-create fmt lint test test-cov install-dev

server:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

makemigrations:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

fmt:
	ruff check . --fix --unsafe-fixes
	ruff format .

lint:
	ruff check .
	ruff format --check .
	mypy .

test:
	pytest

install-dev-deps:
	uv sync --locked

install-deps:
	uv sync --locked --no-dev
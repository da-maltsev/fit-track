.PHONY: server migrate migrate-create

server:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

makemigrations:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message" 
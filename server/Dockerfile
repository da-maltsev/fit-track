FROM python:3.13-slim-bookworm AS deps-compile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv pip compile pyproject.toml -o requirements.txt

FROM python:3.13-slim-bookworm
WORKDIR /app

# Copy requirements from deps-compile stage
COPY --from=deps-compile /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 
# Fitness Tracker

A web application for tracking gym workouts, built with FastAPI and PWA.

## Server Setup

1. Install UV package manager if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
uv pip install -e .
```

3. Database Management:
```bash
# Generate new migrations after model changes
make makemigrations

# Apply pending migrations
make migrate
```

4. Run the server:
```bash
make server
```

The API will be available at http://localhost:8000
API documentation will be available at http://localhost:8000/docs

## Project Structure

```
server/
├── alembic/              # Database migrations
│   ├── versions/        # Migration files
│   ├── env.py          # Alembic environment
│   └── script.py.mako  # Migration template
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Core functionality
│   ├── db/              # Database configuration
│   ├── models/          # SQLAlchemy models
│   └── schemas/         # Pydantic schemas
├── alembic.ini          # Alembic configuration
└── pyproject.toml       # Project dependencies
```

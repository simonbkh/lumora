# ─── Lumora Backend Makefile ──────────────────────────────────────────────────
.PHONY: install dev migrate seed test lint format build up down logs

# Install Python deps locally
install:
	pip install -r backend/requirements.txt

# Run dev server locally (requires .env)
dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker helpers
up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f api

# Database migrations (runs inside the API container)
migrate:
	docker compose exec api alembic upgrade head

migration:
	docker compose exec api alembic revision --autogenerate -m "$(msg)"

# Seed data (runs inside the API container)
seed:
	docker compose exec api python scripts/seed.py

# Tests (run locally — requires: pip install -r backend/requirements.txt)
test:
	cd backend && pytest -v

# Linting (run locally)
lint:
	cd backend && ruff check .

format:
	cd backend && black . && ruff check --fix .

# Build Docker image only
build:
	docker compose build api

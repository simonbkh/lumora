#!/usr/bin/env bash
# ─── Lumora – one-shot startup script ────────────────────────────────────────
# Runs everything inside Docker; no local Python / Alembic install required.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# 1. Copy env file if it doesn't exist yet
if [ ! -f backend/.env ]; then
  echo "📋  Copying .env.example → backend/.env"
  cp backend/.env.example backend/.env
  echo "⚠️   Please edit backend/.env and set SECRET_KEY before continuing."
  echo "     Re-run this script when done."
  exit 0
fi

# 2. Build + start services (Postgres + API)
echo "🐳  Building and starting containers…"
docker compose up --build -d

# 3. Wait for the API container to be healthy
echo "⏳  Waiting for API container to be ready…"
sleep 5

# 4. Run Alembic migrations inside the API container
echo "🗄️   Running database migrations…"
docker compose exec api alembic upgrade head

# 5. Seed initial data
echo "🌱  Seeding initial data…"
docker compose exec api python scripts/seed.py

echo ""
echo "✅  Lumora is running!"
echo "   API docs → http://localhost:8000/docs"
echo "   ReDoc    → http://localhost:8000/redoc"

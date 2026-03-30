"""
app/db/init_db.py
─────────────────
Utility imported by Alembic env.py so that all models are registered
on the metadata before autogenerate runs.
"""
# Re-export Base so Alembic can reach the metadata
from app.db.base import Base  # noqa: F401

# Import every model module to ensure the mapper is populated
from app.models import (  # noqa: F401
    article,
    career,
    mood,
    task,
    user,
)

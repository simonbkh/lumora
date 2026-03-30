"""app/api/v1/router.py – aggregates all v1 endpoint routers."""
from fastapi import APIRouter

from app.api.v1.endpoints import articles, auth, career, mood, tasks, users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)
api_router.include_router(mood.router)
api_router.include_router(articles.router)
api_router.include_router(career.router)

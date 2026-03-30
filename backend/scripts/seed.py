"""
scripts/seed.py
───────────────
Populate the database with initial data:
  - ADMIN user
  - Article categories
  - Career paths + skills
  - Sample articles

Run with:
    cd backend && python scripts/seed.py
"""
from __future__ import annotations

import asyncio
import sys
import os

# Allow running from /backend directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import hash_password
from app.models.article import Article, ArticleCategory
from app.models.career import CareerPath, Resource, Skill
from app.models.user import RoleEnum, User

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        # ── Admin user ────────────────────────────────────────────────────────
        admin = User(
            email="admin@lumora.dev",
            hashed_password=hash_password("Admin1234!"),
            full_name="Lumora Admin",
            role=RoleEnum.ADMIN,
        )
        session.add(admin)

        # ── Article categories ────────────────────────────────────────────────
        categories = [
            ArticleCategory(name="Stress Management", slug="stress-management",
                            description="Techniques to manage daily stress"),
            ArticleCategory(name="Anxiety Relief", slug="anxiety-relief",
                            description="Methods to reduce anxiety"),
            ArticleCategory(name="Focus & Productivity", slug="focus-productivity",
                            description="Tips to improve focus and productivity"),
            ArticleCategory(name="Mindfulness", slug="mindfulness",
                            description="Mindfulness and meditation practices"),
        ]
        session.add_all(categories)
        await session.flush()

        # ── Sample articles ────────────────────────────────────────────────────
        articles = [
            Article(
                title="5 Quick Breathing Exercises to Calm Stress",
                slug="5-breathing-exercises-calm-stress",
                content="Deep breathing is one of the most effective ways...",
                summary="Simple breathing techniques you can do anywhere.",
                is_published=True,
                category_id=categories[0].id,
            ),
            Article(
                title="Understanding the Anxiety Cycle",
                slug="understanding-anxiety-cycle",
                content="Anxiety feeds itself through avoidance...",
                summary="Learn the loop that keeps anxiety going — and how to break it.",
                is_published=True,
                category_id=categories[1].id,
            ),
        ]
        session.add_all(articles)

        # ── Career paths ───────────────────────────────────────────────────────
        software = CareerPath(
            name="Software Engineering",
            slug="software-engineering",
            description="Backend, frontend, devops, and more",
        )
        marketing = CareerPath(
            name="Digital Marketing",
            slug="digital-marketing",
            description="SEO, social media, content strategy",
        )
        design = CareerPath(
            name="UI/UX Design",
            slug="ui-ux-design",
            description="User research, wireframing, prototyping",
        )
        session.add_all([software, marketing, design])
        await session.flush()

        # ── Skills ────────────────────────────────────────────────────────────
        skills = [
            Skill(name="Python", career_path_id=software.id),
            Skill(name="FastAPI", career_path_id=software.id),
            Skill(name="PostgreSQL", career_path_id=software.id),
            Skill(name="Docker", career_path_id=software.id),
            Skill(name="SEO Fundamentals", career_path_id=marketing.id),
            Skill(name="Content Strategy", career_path_id=marketing.id),
            Skill(name="Figma", career_path_id=design.id),
            Skill(name="User Research", career_path_id=design.id),
        ]
        session.add_all(skills)

        # ── Resources ─────────────────────────────────────────────────────────
        resources = [
            Resource(
                title="FastAPI Official Docs",
                url="https://fastapi.tiangolo.com",
                resource_type="link",
                career_path_id=software.id,
            ),
            Resource(
                title="The SEO Starter Guide",
                url="https://developers.google.com/search/docs/fundamentals/seo-starter-guide",
                resource_type="link",
                career_path_id=marketing.id,
            ),
        ]
        session.add_all(resources)

        await session.commit()
        print("✅  Seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed())

"""Idempotent database bootstrap: create tables and seed baseline accounts.

Runs on API startup so `docker compose up` works with no manual migration step.
Alembic remains available for versioned schema history (see migrations/).
"""

from sqlalchemy import select

from app.shared.config import get_settings
from app.shared.db import Base, async_session_factory, engine
from app.shared.models import User
from app.shared.security import hash_password

settings = get_settings()


async def _seed_user(session, *, email: str, nombre: str, password: str, rol: str) -> None:
    exists = await session.scalar(select(User).where(User.email == email))
    if exists is None:
        session.add(
            User(
                email=email,
                nombre=nombre,
                password_hash=hash_password(password),
                rol=rol,
                activo=True,
            )
        )


async def init_db() -> None:
    """Create all tables and seed the demo admin + storefront customer."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        await _seed_user(
            session,
            email=settings.demo_admin_username,  # "admin" acts as the login handle
            nombre="Admin Principal",
            password=settings.demo_admin_password,
            rol="Admin",
        )
        await _seed_user(
            session,
            email=settings.storefront_customer_email,
            nombre="Storefront Customer",
            password="customer123",
            rol="Lector",
        )
        await session.commit()

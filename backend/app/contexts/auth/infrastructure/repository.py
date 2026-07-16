"""SQLAlchemy async adapter for the UserRepository port."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.models import User


class SqlAlchemyUserRepository:
    """Async user repository backed by the shared SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.scalar(select(User).where(User.id == user_id))

    async def get_by_email(self, email: str) -> User | None:
        return await self._session.scalar(select(User).where(User.email == email))

    async def list_all(self) -> list[User]:
        result = await self._session.scalars(select(User).order_by(User.id))
        return list(result.all())

    async def add(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def save(self, user: User) -> User:
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.commit()

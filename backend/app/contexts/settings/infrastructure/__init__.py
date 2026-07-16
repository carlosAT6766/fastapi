"""SQLAlchemy async adapter implementing the settings repository port."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.contexts.settings.domain import Settings
from app.shared.models import UserSettings


class SqlAlchemySettingsRepository:
    """Maps the `user_settings` table to and from the domain `Settings` entity."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: int) -> Settings | None:
        row = await self._session.get(UserSettings, user_id)
        if row is None:
            return None
        return Settings(default_source=row.default_source, default_style=row.default_style)

    async def upsert(self, user_id: int, settings: Settings) -> Settings:
        row = await self._session.get(UserSettings, user_id)
        if row is None:
            row = UserSettings(user_id=user_id)
            self._session.add(row)
        row.default_source = settings.default_source
        row.default_style = settings.default_style
        await self._session.commit()
        return Settings(default_source=row.default_source, default_style=row.default_style)

"""Use cases orchestrating settings retrieval and persistence."""

from app.contexts.settings.application.ports import SettingsRepositoryPort
from app.contexts.settings.domain import Settings


class SettingsService:
    """Application service for reading and updating a user's default settings."""

    def __init__(self, repository: SettingsRepositoryPort) -> None:
        self._repository = repository

    async def get_settings(self, user_id: int) -> Settings:
        """Return stored settings, or domain defaults when none exist yet."""
        return await self._repository.get(user_id) or Settings()

    async def update_settings(self, user_id: int, settings: Settings) -> Settings:
        """Upsert the user's default source and style."""
        return await self._repository.upsert(user_id, settings)

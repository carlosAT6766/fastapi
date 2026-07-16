"""Repository port for the settings context (driven side of the hexagon)."""

from typing import Protocol

from app.contexts.settings.domain import Settings


class SettingsRepositoryPort(Protocol):
    """Persistence contract for per-user default settings."""

    async def get(self, user_id: int) -> Settings | None:
        """Return the stored settings for a user, or None if absent."""
        ...

    async def upsert(self, user_id: int, settings: Settings) -> Settings:
        """Create or update the user's settings and return the stored value."""
        ...

"""Shared Redis settings and pub/sub channel helpers (queue + fan-out)."""

from arq.connections import RedisSettings

from app.shared.config import get_settings

settings = get_settings()

REDIS_SETTINGS = RedisSettings(
    host=settings.redis_host,
    port=settings.redis_port,
    database=settings.redis_db,
)


def user_channel(user_id: int) -> str:
    """Pub/sub channel a WebSocket connection subscribes to for its own events."""
    return f"tx:user:{user_id}"

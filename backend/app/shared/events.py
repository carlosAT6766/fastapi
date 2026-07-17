"""Redis pub/sub event publisher used by use cases and the worker.

Publishing a status change to a user's channel is what lets the WebSocket
fan-out work behind the load balancer (any replica can serve any socket).
"""

import json
from typing import Any

from redis.asyncio import Redis

from app.shared.config import get_settings
from app.shared.redis import STOREFRONT_CHANNEL, user_channel

settings = get_settings()


def _client() -> Redis:
    return Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)


async def publish_transaction_event(user_id: int, event: dict[str, Any]) -> None:
    """Publish a transaction status change to the owner's channel."""
    client = _client()
    try:
        await client.publish(user_channel(user_id), json.dumps(event, default=str))
    finally:
        await client.aclose()


async def publish_storefront_event(event: dict[str, Any]) -> None:
    """Broadcast a catalog change to the public storefront channel."""
    client = _client()
    try:
        await client.publish(STOREFRONT_CHANNEL, json.dumps(event, default=str))
    finally:
        await client.aclose()

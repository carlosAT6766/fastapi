"""Redis adapter for the EventPublisher port.

Thin wrapper over the shared publisher so use cases depend on the port, not on
the concrete Redis helper.
"""

from typing import Any

from app.shared.events import publish_storefront_event, publish_transaction_event


class RedisEventPublisher:
    """Publishes transaction events to the owner's pub/sub channel."""

    async def publish(self, user_id: int, event: dict[str, Any]) -> None:
        await publish_transaction_event(user_id, event)

    async def publish_storefront(self, event: dict[str, Any]) -> None:
        await publish_storefront_event(event)

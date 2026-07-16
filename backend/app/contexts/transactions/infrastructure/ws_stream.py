"""WebSocket fan-out backed by Redis pub/sub.

Each connection subscribes to its owner's channel on the local replica and
forwards messages to the socket. Because every replica subscribes to Redis, the
fan-out works behind the load balancer with no sticky sessions (T4).
"""

import asyncio

from redis.asyncio import Redis
from starlette.websockets import WebSocket, WebSocketState

from app.shared.config import get_settings
from app.shared.redis import user_channel

settings = get_settings()

_SUBPROTOCOL_SEPARATOR = ","


def extract_token(websocket: WebSocket) -> str | None:
    """Read the JWT from the Sec-WebSocket-Protocol header (subprotocol auth).

    The client offers ["bearer", <jwt>]; skip the "bearer" marker and return the
    actual token.
    """
    header = websocket.headers.get("sec-websocket-protocol")
    if not header:
        return None
    parts = [p.strip() for p in header.split(_SUBPROTOCOL_SEPARATOR) if p.strip()]
    if not parts:
        return None
    if len(parts) >= 2 and parts[0].lower() == "bearer":
        return parts[1]
    return parts[0]


async def forward_events(websocket: WebSocket, user_id: int) -> None:
    """Subscribe to the user's channel and forward each message to the socket."""
    client = Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
    pubsub = client.pubsub()
    await pubsub.subscribe(user_channel(user_id))
    try:
        while websocket.application_state == WebSocketState.CONNECTED:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message is not None:
                data = message["data"]
                await websocket.send_text(data.decode() if isinstance(data, bytes) else data)
            else:
                await asyncio.sleep(0)
    finally:
        await pubsub.unsubscribe(user_channel(user_id))
        await pubsub.aclose()
        await client.aclose()

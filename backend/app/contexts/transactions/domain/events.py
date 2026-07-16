"""Serialization of a transaction into the WebSocket event contract.

Single source of truth for the JSON pushed to clients (T4), reused by the API
on synchronous transitions and by the worker on book pipeline transitions.
"""

from datetime import UTC, datetime
from typing import Any

from app.shared.models import Transaction

EVENT_CREATED = "created"
EVENT_STATUS_CHANGED = "status_changed"


def _to_float(value: Any) -> float | None:
    return float(value) if value is not None else None


def transaction_event(transaction: Transaction, event: str) -> dict[str, Any]:
    """Build the JSON event for a transaction status change."""
    return {
        "event": event,
        "id": transaction.id,
        "user_id": transaction.user_id,
        "tipo": transaction.tipo,
        "estado": transaction.estado,
        "sub_estado": transaction.sub_estado,
        "titulo": transaction.titulo,
        "estilo": transaction.estilo,
        "precio": _to_float(transaction.precio),
        "monto": _to_float(transaction.monto),
        "libro_id": transaction.libro_id,
        "resumen": transaction.resumen,
        "ts": datetime.now(UTC).isoformat(),
    }

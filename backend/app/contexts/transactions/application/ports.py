"""Hexagonal ports (Protocols) for the transactions context.

Use cases depend on these abstractions; concrete adapters live in
`infrastructure/`. Keeps application logic free of SQLAlchemy and Redis.
"""

from typing import Any, Protocol

from app.shared.models import Transaction


class TransactionRepository(Protocol):
    """Persistence port for the unified transactional core."""

    async def find_by_idempotency_key(self, key: str) -> Transaction | None: ...

    async def get_book(self, book_id: int) -> Transaction | None: ...

    async def create_sale(
        self,
        *,
        user_id: int,
        monto: float,
        libro_id: int,
        idempotency_key: str,
    ) -> tuple[Transaction, bool]:
        """Atomically create a sale. Returns (transaction, created)."""
        ...

    async def create_book(
        self,
        *,
        user_id: int,
        titulo: str,
        precio: float,
        estilo: str,
    ) -> Transaction: ...

    async def list_books(self, estado: str | None) -> list[Transaction]: ...

    async def list_sales(self, user_id: int) -> list[Transaction]: ...

    async def snapshot(self, user_id: int) -> list[Transaction]: ...


class EventPublisher(Protocol):
    """Fan-out port: publishes events to a user's channel for the WebSocket."""

    async def publish(self, user_id: int, event: dict[str, Any]) -> None: ...

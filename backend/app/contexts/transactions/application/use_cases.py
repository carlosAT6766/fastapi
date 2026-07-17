"""Application use cases for the transactions context.

Idempotency and sellability rules live here (not in the HTTP adapter), so they
are reused identically by any entrypoint.
"""

from app.shared.models import STATUS_PENDING, STATUS_PROCESSED, Transaction

from ..domain.errors import BookNotFoundError, BookNotSellableError
from ..domain.events import EVENT_CREATED, EVENT_STATUS_CHANGED, transaction_event
from .ports import EventPublisher, TransactionRepository

SUB_STATE_SEARCHING = "buscando"


class RegisterSale:
    """Idempotently register a sale of a published book (POST /transactions/create)."""

    def __init__(self, repository: TransactionRepository, publisher: EventPublisher) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(
        self, *, user_id: int, monto: float, libro_id: int, idempotency_key: str
    ) -> tuple[Transaction, bool]:
        existing = await self._repository.find_by_idempotency_key(idempotency_key)
        if existing is not None:
            return existing, False

        book = await self._repository.get_book(libro_id)
        if book is None:
            raise BookNotFoundError(f"Book {libro_id} does not exist")
        if book.estado != STATUS_PROCESSED or not book.precio or book.precio <= 0:
            raise BookNotSellableError(f"Book {libro_id} is not available for sale")

        sale, created = await self._repository.create_sale(
            user_id=user_id,
            monto=monto,
            libro_id=libro_id,
            idempotency_key=idempotency_key,
        )
        if created:
            # Notify the seller (book owner), not the buyer, so the admin's
            # Ventas view updates live over the WebSocket. Enrich with the book
            # title so the UI can show it (the sale row itself has no title).
            event = transaction_event(sale, EVENT_CREATED)
            event["libro_titulo"] = book.titulo
            await self._publisher.publish(book.user_id, event)
        return sale, created


class RequestBookGeneration:
    """Create a pending book and enqueue its async generation (POST /transactions/async-process)."""

    def __init__(self, repository: TransactionRepository, publisher: EventPublisher) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(
        self, *, user_id: int, titulo: str, precio: float, estilo: str
    ) -> Transaction:
        book = await self._repository.create_book(
            user_id=user_id, titulo=titulo, precio=precio, estilo=estilo
        )
        await self._publisher.publish(user_id, transaction_event(book, EVENT_CREATED))
        return book


class UpdateBook:
    """Edit an existing book's title/price/style/summary (PATCH /books/{id})."""

    def __init__(self, repository: TransactionRepository, publisher: EventPublisher) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(
        self,
        *,
        book_id: int,
        titulo: str,
        precio: float,
        estilo: str,
        resumen: str | None,
    ) -> Transaction:
        book = await self._repository.update_book(
            book_id=book_id, titulo=titulo, precio=precio, estilo=estilo, resumen=resumen
        )
        if book is None:
            raise BookNotFoundError(f"Book {book_id} does not exist")
        await self._publisher.publish(book.user_id, transaction_event(book, EVENT_STATUS_CHANGED))
        return book


class PublishBook:
    """Make a ready book visible in the storefront (POST /books/{id}/publish)."""

    def __init__(self, repository: TransactionRepository, publisher: EventPublisher) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(self, *, book_id: int) -> Transaction:
        book = await self._repository.get_book(book_id)
        if book is None:
            raise BookNotFoundError(f"Book {book_id} does not exist")
        if book.estado != STATUS_PROCESSED:
            raise BookNotSellableError(f"Book {book_id} must be ready before publishing")
        published = await self._repository.publish_book(book_id)
        # Broadcast to the public storefront channel so every open storefront
        # refreshes its catalog live. The acting admin still updates optimistically.
        await self._publisher.publish_storefront(
            transaction_event(published, EVENT_STATUS_CHANGED)
        )
        return published


class ListPublishedBooks:
    """Public storefront listing (GET /books)."""

    def __init__(self, repository: TransactionRepository) -> None:
        self._repository = repository

    async def execute(self, *, estado: str | None = None) -> list[Transaction]:
        return await self._repository.list_books(estado)


class ListUserSales:
    """User sales list plus aggregate metrics (GET /sales)."""

    def __init__(self, repository: TransactionRepository) -> None:
        self._repository = repository

    async def execute(self, *, user_id: int) -> tuple[list[Transaction], dict[str, float]]:
        sales = await self._repository.list_sales(user_id)
        recaudado = sum(float(sale.monto) for sale in sales if sale.monto)
        metrics = {"total": len(sales), "recaudado": round(recaudado, 2)}
        return sales, metrics


class GetTransactionsSnapshot:
    """Current state of a user's transactions, sent on WebSocket connect."""

    def __init__(self, repository: TransactionRepository) -> None:
        self._repository = repository

    async def execute(self, *, user_id: int) -> list[Transaction]:
        return await self._repository.snapshot(user_id)


__all__ = [
    "STATUS_PENDING",
    "SUB_STATE_SEARCHING",
    "GetTransactionsSnapshot",
    "ListPublishedBooks",
    "ListUserSales",
    "PublishBook",
    "RegisterSale",
    "RequestBookGeneration",
    "UpdateBook",
]

"""SQLAlchemy adapter for the TransactionRepository port."""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.shared.models import (
    KIND_BOOK,
    KIND_SALE,
    STATUS_PENDING,
    STATUS_PROCESSED,
    Transaction,
)

SUB_STATE_SEARCHING = "buscando"


class SqlAlchemyTransactionRepository:
    """Concrete repository backed by an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_idempotency_key(self, key: str) -> Transaction | None:
        return await self._session.scalar(
            select(Transaction).where(Transaction.idempotency_key == key)
        )

    async def get_book(self, book_id: int) -> Transaction | None:
        return await self._session.scalar(
            select(Transaction).where(Transaction.id == book_id, Transaction.tipo == KIND_BOOK)
        )

    async def create_sale(
        self, *, user_id: int, monto: float, libro_id: int, idempotency_key: str
    ) -> tuple[Transaction, bool]:
        """Insert a sale atomically; a duplicate key returns the original row."""
        stmt = (
            pg_insert(Transaction)
            .values(
                user_id=user_id,
                tipo=KIND_SALE,
                estado=STATUS_PROCESSED,
                monto=monto,
                libro_id=libro_id,
                idempotency_key=idempotency_key,
            )
            .on_conflict_do_nothing(index_elements=["idempotency_key"])
            .returning(Transaction.id)
        )
        result = await self._session.execute(stmt)
        new_id = result.scalar_one_or_none()
        await self._session.commit()

        if new_id is not None:
            sale = await self._session.get(Transaction, new_id)
            return sale, True

        existing = await self.find_by_idempotency_key(idempotency_key)
        return existing, False

    async def create_book(
        self, *, user_id: int, titulo: str, precio: float, estilo: str
    ) -> Transaction:
        book = Transaction(
            user_id=user_id,
            tipo=KIND_BOOK,
            estado=STATUS_PENDING,
            sub_estado=SUB_STATE_SEARCHING,
            titulo=titulo,
            precio=precio,
            estilo=estilo,
            log=[],
        )
        self._session.add(book)
        await self._session.commit()
        await self._session.refresh(book)
        return book

    async def list_books(self, estado: str | None) -> list[Transaction]:
        query = select(Transaction).where(
            Transaction.tipo == KIND_BOOK,
            Transaction.precio.is_not(None),
            Transaction.precio > 0,
            Transaction.estado == (estado or STATUS_PROCESSED),
        )
        result = await self._session.scalars(query.order_by(Transaction.created_at.desc()))
        return list(result)

    def _owned_book_ids(self, user_id: int):
        """Subquery: ids of the books owned (created) by this user."""
        return select(Transaction.id).where(
            Transaction.tipo == KIND_BOOK, Transaction.user_id == user_id
        )

    async def list_sales(self, user_id: int) -> list[Transaction]:
        """Sales of the user's own books (seller view), each enriched with the book title."""
        book = aliased(Transaction)
        query = (
            select(Transaction, book.titulo)
            .join(book, Transaction.libro_id == book.id)
            .where(
                Transaction.tipo == KIND_SALE,
                Transaction.libro_id.in_(self._owned_book_ids(user_id)),
            )
            .order_by(Transaction.created_at.desc())
        )
        rows = await self._session.execute(query)
        sales: list[Transaction] = []
        for sale, book_title in rows:
            sale.libro_titulo = book_title  # transient attribute for serialization
            sales.append(sale)
        return sales

    async def snapshot(self, user_id: int) -> list[Transaction]:
        """The user's own books plus the sales of those books (for the WS connect snapshot)."""
        query = select(Transaction).where(
            (Transaction.user_id == user_id)
            | (
                (Transaction.tipo == KIND_SALE)
                & Transaction.libro_id.in_(self._owned_book_ids(user_id))
            )
        )
        result = await self._session.scalars(query.order_by(Transaction.created_at.desc()))
        return list(result)

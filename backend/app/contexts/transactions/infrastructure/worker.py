"""arq worker for asynchronous BOOK generation.

Pipeline for `generate_book(ctx, transaction_id)`:
  1. sub_estado="buscando"        -> publish
  2. fetch the Wikipedia paragraph (Teammate C's RPA adapter)
  3. sub_estado="resumiendo"      -> publish
  4. summarize the paragraph      (Teammate C's summarizer)
  5. estado="procesado" + resumen -> publish
On error: estado="fallido" -> publish -> re-raise so arq records the failure.

The worker owns its DB session (no FastAPI Depends) and publishes via the shared
pub/sub helper for the WebSocket fan-out.
"""

from app.contexts.assistant.application.summarizer import summarize_text
from app.contexts.assistant.infrastructure.wikipedia import fetch_first_paragraph
from app.shared.db import async_session_factory
from app.shared.events import publish_transaction_event
from app.shared.models import (
    STATUS_FAILED,
    STATUS_PROCESSED,
    Transaction,
)
from app.shared.redis import REDIS_SETTINGS

from ..domain.events import EVENT_STATUS_CHANGED, transaction_event

SUB_STATE_SEARCHING = "buscando"
SUB_STATE_SUMMARIZING = "resumiendo"
DEFAULT_SOURCE = "Wikipedia + DBpedia (ES)"
DEFAULT_STYLE = "Formal"


async def _publish(transaction: Transaction) -> None:
    await publish_transaction_event(
        transaction.user_id, transaction_event(transaction, EVENT_STATUS_CHANGED)
    )


async def generate_book(ctx: dict, transaction_id: int) -> None:
    """Run the book generation pipeline for a single transaction."""
    async with async_session_factory() as session:
        book = await session.get(Transaction, transaction_id)
        if book is None:
            return

        try:
            book.sub_estado = SUB_STATE_SEARCHING
            await session.commit()
            await _publish(book)

            paragraph = await fetch_first_paragraph(book.titulo, DEFAULT_SOURCE)

            book.sub_estado = SUB_STATE_SUMMARIZING
            await session.commit()
            await _publish(book)

            resumen = await summarize_text(paragraph, book.estilo or DEFAULT_STYLE, book.user_id)

            book.resumen = resumen
            book.estado = STATUS_PROCESSED
            book.sub_estado = None
            await session.commit()
            await _publish(book)
        except Exception:
            book.estado = STATUS_FAILED
            book.sub_estado = None
            await session.commit()
            await _publish(book)
            raise


class WorkerSettings:
    functions = [generate_book]
    redis_settings = REDIS_SETTINGS
    max_tries = 3
    job_timeout = 60

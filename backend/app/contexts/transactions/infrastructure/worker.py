"""arq worker for asynchronous BOOK generation.

STUB — Teammate B implements `generate_book`:
  1. mark transaction sub_estado="buscando"; publish event
  2. run RPA (call Teammate C's RPA or trigger the rpa-bot) to fetch the Wikipedia
     paragraph for `titulo`
  3. sub_estado="resumiendo"; publish
  4. call /assistant/summarize (or the summarizer use case) -> resumen
  5. estado="procesado" (listo) + resumen; publish. On error estado="fallido"; publish.

Uses app.shared.events.publish_transaction_event for the WS fan-out.
"""

import asyncio

from app.shared.redis import REDIS_SETTINGS


async def generate_book(ctx: dict, transaction_id: int) -> None:
    # Teammate B: replace the sleep with the real book-generation pipeline.
    await asyncio.sleep(1)


class WorkerSettings:
    functions = [generate_book]
    redis_settings = REDIS_SETTINGS
    max_tries = 3
    job_timeout = 60

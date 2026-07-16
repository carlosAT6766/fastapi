"""Summarize use case: pick the adapter, run it, persist the log.

Exposes `summarize_text`, imported by the async worker (Teammate B).
"""

import logging

from app.contexts.assistant.application.ports import SummarizerPort
from app.contexts.assistant.infrastructure.fake_adapter import FakeSummarizerAdapter
from app.contexts.assistant.infrastructure.openai_adapter import OpenAIAdapter
from app.shared.config import get_settings
from app.shared.db import async_session_factory
from app.shared.models import AssistantLog

logger = logging.getLogger(__name__)

DEFAULT_STYLE = "Formal"

STATUS_OK = "ok"
STATUS_ERROR = "error"


def get_summarizer() -> SummarizerPort:
    """Real OpenAI adapter when a key is configured, deterministic fake otherwise."""
    if get_settings().openai_api_key:
        return OpenAIAdapter()
    return FakeSummarizerAdapter()


async def _run_summarizer(text: str, style: str) -> tuple[str, str, str]:
    """Return (summary, model, status), degrading to the fake adapter on API errors."""
    summarizer = get_summarizer()
    try:
        summary = await summarizer.summarize(text, style)
        return summary, summarizer.name, STATUS_OK
    except Exception:  # noqa: BLE001 - third-party API must never break the demo
        logger.exception("Summarizer '%s' failed; falling back to fake", summarizer.name)
        fake = FakeSummarizerAdapter()
        summary = await fake.summarize(text, style)
        return summary, fake.name, STATUS_ERROR


async def _persist_log(
    text: str, summary: str, model: str, status: str, user_id: int | None
) -> None:
    async with async_session_factory() as session:
        session.add(
            AssistantLog(
                user_id=user_id,
                input_text=text,
                output_text=summary,
                model=model,
                status=status,
            )
        )
        await session.commit()


async def summarize_and_log(text: str, style: str, user_id: int | None = None) -> tuple[str, str]:
    """Summarize `text`, persist an AssistantLog, return (summary, model)."""
    summary, model, status = await _run_summarizer(text, style)
    await _persist_log(text, summary, model, status, user_id)
    return summary, model


async def summarize_text(text: str, style: str, user_id: int | None = None) -> str:
    """Summarize `text` in `style`, persist an AssistantLog, return the summary."""
    summary, _model = await summarize_and_log(text, style, user_id)
    return summary

"""Assistant entrypoints.

Contract:
  POST /assistant/summarize -> {summary, model}. Real OpenAI when OPENAI_API_KEY is
  set, deterministic fake otherwise. Persists request/response to assistant_logs.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.contexts.assistant.application.summarizer import DEFAULT_STYLE, summarize_and_log
from app.contexts.assistant.infrastructure.wikipedia import fetch_first_paragraph
from app.shared.models import User
from app.shared.security import get_current_user

router = APIRouter(tags=["assistant"])


class SummarizeRequest(BaseModel):
    text: str | None = Field(default=None, description="Text to summarize.")
    style: str = Field(default=DEFAULT_STYLE, description="Summary style/tone.")
    term: str | None = Field(default=None, description="Wikipedia term to fetch instead of text.")


class SummarizeResponse(BaseModel):
    summary: str
    model: str


async def _resolve_text(payload: SummarizeRequest) -> str:
    if payload.text and payload.text.strip():
        return payload.text
    if payload.term and payload.term.strip():
        return await fetch_first_paragraph(payload.term)
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Provide 'text' or 'term'")


@router.post("/assistant/summarize", response_model=SummarizeResponse)
async def summarize(
    payload: SummarizeRequest,
    user: User = Depends(get_current_user),
) -> SummarizeResponse:
    text = await _resolve_text(payload)
    summary, model = await summarize_and_log(text, payload.style, user.id)
    return SummarizeResponse(summary=summary, model=model)


@router.get("/assistant/health")
async def assistant_health() -> dict[str, str]:
    return {"context": "assistant", "status": "ok"}

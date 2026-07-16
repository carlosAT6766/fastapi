"""Assistant entrypoints. Teammate C implements the route below.

Contract:
  POST /assistant/summarize -> {summary}. Real OpenAI when OPENAI_API_KEY is set,
  fake deterministic summarizer otherwise. Persists request/response to assistant_logs.
"""

from fastapi import APIRouter

router = APIRouter(tags=["assistant"])


@router.get("/assistant/health")
async def assistant_health() -> dict[str, str]:
    return {"context": "assistant", "status": "stub"}

"""OpenAI-backed summarizer adapter."""

from openai import AsyncOpenAI

from app.shared.config import get_settings

REQUEST_TIMEOUT_SECONDS = 30.0
TEMPERATURE = 0.3
SYSTEM_PROMPT = (
    "Eres un asistente que resume textos en 2-3 frases claras en espanol. "
    "Respeta el estilo solicitado y no inventes datos."
)


class OpenAIAdapter:
    """Calls the OpenAI Chat Completions API to produce the summary."""

    name: str

    def __init__(self) -> None:
        settings = get_settings()
        self.name = settings.openai_model
        self._model = settings.openai_model
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

    async def summarize(self, text: str, style: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Estilo: {style}.\n\nTexto:\n{text}"},
            ],
        )
        return (response.choices[0].message.content or "").strip()

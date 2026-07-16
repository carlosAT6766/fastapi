"""Deterministic summarizer used when no OpenAI key is configured (or as fallback)."""

SUMMARY_WORD_LIMIT = 28
SIMULATED_SUFFIX = "(resumen simulado)"

# Style-driven opening so the demo shows the `style` argument taking effect.
STYLE_PREFIXES = {
    "formal": "En resumen: ",
    "informal": "Resumiendo rapidito: ",
    "tecnico": "Resumen tecnico: ",
    "técnico": "Resumen tecnico: ",
    "narrativo": "La historia en breve: ",
}
DEFAULT_PREFIX = "Resumen: "


class FakeSummarizerAdapter:
    """Style prefix + the first words of the text + a simulated marker."""

    name = "fake"

    async def summarize(self, text: str, style: str) -> str:
        prefix = STYLE_PREFIXES.get(style.strip().lower(), DEFAULT_PREFIX)
        words = text.split()
        head = " ".join(words[:SUMMARY_WORD_LIMIT])
        return f"{prefix}{head} {SIMULATED_SUFFIX}".strip()

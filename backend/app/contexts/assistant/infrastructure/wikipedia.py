"""Fetch the first paragraph of a Wikipedia article via its REST summary API."""

import httpx

REQUEST_TIMEOUT_SECONDS = 30.0

# Wikimedia rejects requests without a descriptive User-Agent (HTTP 403).
USER_AGENT = "ResumeAI/0.1 (technical-test; contact: admin@resumeai.com)"

# Maps a human-facing source label to the Wikipedia language subdomain.
SOURCE_TO_LANG = {
    "Wikipedia (ES)": "es",
    "Wikipedia (EN)": "en",
    "Wikipedia (PT)": "pt",
}
DEFAULT_LANG = "es"


def _lang_for(source: str) -> str:
    return SOURCE_TO_LANG.get(source, DEFAULT_LANG)


async def fetch_first_paragraph(term: str, source: str = "Wikipedia (ES)") -> str:
    """Return the article's lead extract (first real paragraph) for `term`."""
    lang = _lang_for(source)
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{term}"
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.get(
            url, headers={"accept": "application/json", "user-agent": USER_AGENT}
        )
        response.raise_for_status()
        return response.json().get("extract", "").strip()

"""Fetch the lead paragraph of an article.

Two providers, so a single source can fall back when the first has no article:
  * Wikipedia REST summary API (primary).
  * DBpedia (a different site built from Wikipedia data) as the fallback.

The default source "Wikipedia + DBpedia (ES)" tries Wikipedia first and, only if
it returns nothing, DBpedia — so book generation still succeeds when a term is
missing or empty on Wikipedia.
"""

import httpx

REQUEST_TIMEOUT_SECONDS = 30.0

# Wikimedia rejects requests without a descriptive User-Agent (HTTP 403).
USER_AGENT = "ResumeAI/0.1 (technical-test; contact: admin@resumeai.com)"

# Combined source: Wikipedia first, DBpedia as fallback.
COMBINED_SOURCE = "Wikipedia + DBpedia (ES)"

# Maps a human-facing source label to the Wikipedia language subdomain.
SOURCE_TO_LANG = {
    COMBINED_SOURCE: "es",
    "Wikipedia (ES)": "es",
    "Wikipedia (EN)": "en",
    "Wikipedia (PT)": "pt",
}
DEFAULT_LANG = "es"

DBPEDIA_ABSTRACT_KEY = "http://dbpedia.org/ontology/abstract"


def _lang_for(source: str) -> str:
    return SOURCE_TO_LANG.get(source, DEFAULT_LANG)


async def _fetch_wikipedia(term: str, lang: str) -> str:
    """Return the Wikipedia article's lead extract, or '' if unavailable."""
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{term}"
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.get(
            url, headers={"accept": "application/json", "user-agent": USER_AGENT}
        )
        if response.status_code == 404:
            return ""
        response.raise_for_status()
        return response.json().get("extract", "").strip()


async def _fetch_dbpedia(term: str, lang: str) -> str:
    """Return the DBpedia abstract for `term`, or '' if unavailable.

    DBpedia is a distinct site that publishes structured, encyclopedic data
    derived from Wikipedia, so it makes a natural second source.
    """
    resource = term.replace(" ", "_")
    url = f"https://{lang}.dbpedia.org/data/{resource}.json"
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.get(url, headers={"user-agent": USER_AGENT})
        if response.status_code == 404:
            return ""
        response.raise_for_status()
        data = response.json()

    resource_uri = f"http://{lang}.dbpedia.org/resource/{resource}"
    abstracts = data.get(resource_uri, {}).get(DBPEDIA_ABSTRACT_KEY, [])
    # Prefer the requested language, otherwise take the first available abstract.
    for entry in abstracts:
        if entry.get("lang") == lang and entry.get("value"):
            return entry["value"].strip()
    for entry in abstracts:
        if entry.get("value"):
            return entry["value"].strip()
    return ""


async def fetch_first_paragraph(term: str, source: str = COMBINED_SOURCE) -> str:
    """Return the lead paragraph for `term` from the configured source.

    For the combined source, Wikipedia is tried first and DBpedia is used as a
    fallback; single-provider sources hit only Wikipedia.
    """
    lang = _lang_for(source)
    paragraph = await _fetch_wikipedia(term, lang)
    if not paragraph and source == COMBINED_SOURCE:
        paragraph = await _fetch_dbpedia(term, lang)
    return paragraph

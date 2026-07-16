"""RPA bot: open Wikipedia, extract the first paragraph, POST it to /assistant/summarize.

Runs headless with sync Playwright + httpx (matching sync flows). Configuration
comes from environment variables so it works both in Docker and locally.
"""

import os
import sys

import httpx
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://nginx:80")
ADMIN_USERNAME = os.getenv("RPA_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("RPA_PASSWORD", "admin123")
DEFAULT_TERM = "Inteligencia artificial"
WIKI_LANG = os.getenv("WIKI_LANG", "es")

MIN_PARAGRAPH_LENGTH = 40
HTTP_TIMEOUT_SECONDS = 30.0
PARAGRAPH_SELECTOR = ".mw-parser-output > p"

BROWSER_ARGS = ["--no-sandbox", "--disable-dev-shm-usage"]


def login() -> str:
    """Authenticate against the API and return the JWT access token."""
    response = httpx.post(
        f"{BASE_URL}/auth/login",
        data={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
        timeout=HTTP_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def extract_first_paragraph(term: str) -> str:
    """Navigate directly to the article URL and return its first real paragraph."""
    url = f"https://{WIKI_LANG}.wikipedia.org/wiki/{term.replace(' ', '_')}"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=BROWSER_ARGS)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        for paragraph in page.query_selector_all(PARAGRAPH_SELECTOR):
            text = (paragraph.inner_text() or "").strip()
            if len(text) > MIN_PARAGRAPH_LENGTH:
                browser.close()
                return text
        browser.close()
    raise RuntimeError(f"No paragraph longer than {MIN_PARAGRAPH_LENGTH} chars for '{term}'")


def summarize(token: str, text: str, term: str) -> dict:
    """POST the extracted paragraph to the assistant summarize endpoint."""
    response = httpx.post(
        f"{BASE_URL}/assistant/summarize",
        json={"text": text, "style": "Formal", "term": term},
        headers={"Authorization": f"Bearer {token}"},
        timeout=HTTP_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    term = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TERM
    print(f"[rpa] term={term!r} base={BASE_URL}")
    token = login()
    paragraph = extract_first_paragraph(term)
    print(f"[rpa] extracted {len(paragraph)} chars")
    result = summarize(token, paragraph, term)
    print(f"[rpa] model={result.get('model')} summary={result.get('summary')}")


if __name__ == "__main__":
    main()

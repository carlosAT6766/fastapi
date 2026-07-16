"""Hexagonal ports for the assistant context."""

from typing import Protocol


class SummarizerPort(Protocol):
    """Turns a block of text into a short summary in the requested style."""

    name: str

    async def summarize(self, text: str, style: str) -> str: ...

"""Settings domain: entity and valid option sets, independent of framework/ORM."""

from dataclasses import dataclass

DEFAULT_SOURCE = "Wikipedia (ES)"
DEFAULT_STYLE = "Formal"

VALID_SOURCES: frozenset[str] = frozenset(
    {"Wikipedia (ES)", "Wikipedia (EN)", "Wikipedia (PT)"}
)
VALID_STYLES: frozenset[str] = frozenset(
    {"Formal", "Casual", "Técnico", "Ejecutivo", "Divertido"}
)


@dataclass(frozen=True)
class Settings:
    """A user's default source and style for creating a book summary."""

    default_source: str = DEFAULT_SOURCE
    default_style: str = DEFAULT_STYLE

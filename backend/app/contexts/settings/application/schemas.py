"""Pydantic v2 schemas for the settings API."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.contexts.settings.domain import DEFAULT_SOURCE, DEFAULT_STYLE

SourceLiteral = Literal["Wikipedia (ES)", "Wikipedia (EN)", "Wikipedia (PT)"]
StyleLiteral = Literal["Formal", "Casual", "Técnico", "Ejecutivo", "Divertido"]


class SettingsRead(BaseModel):
    """Response body for GET/PUT /settings."""

    default_source: str = DEFAULT_SOURCE
    default_style: str = DEFAULT_STYLE


class SettingsUpdate(BaseModel):
    """Request body for PUT /settings; invalid options are rejected by FastAPI."""

    default_source: Annotated[SourceLiteral, Field()]
    default_style: Annotated[StyleLiteral, Field()]

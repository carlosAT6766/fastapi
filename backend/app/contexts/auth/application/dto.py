"""Pydantic v2 schemas (DTOs) for the auth + users entrypoints."""

from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.contexts.auth.domain import ROLE_READER

# Basic RFC-ish email pattern (kept local to avoid an email-validator dependency).
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class RegisterRequest(BaseModel):
    """Public self-registration payload."""

    email: str = Field(pattern=EMAIL_PATTERN)
    nombre: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=6, max_length=128)
    rol: str = ROLE_READER


class LoginRequest(BaseModel):
    """Login payload accepting an email or the demo admin username.

    Accepts both the English (`username`/`password`) and Spanish
    (`usuario`/`clave`) field names so either frontend contract works.
    """

    usuario: str = Field(
        min_length=1, validation_alias=AliasChoices("username", "usuario")
    )
    clave: str = Field(min_length=1, validation_alias=AliasChoices("password", "clave"))


class TokenResponse(BaseModel):
    """Bearer token returned on successful login."""

    access_token: str
    token_type: str = "bearer"


class CreateUserRequest(BaseModel):
    """Admin-driven user creation (password defaults to changeme123)."""

    email: str = Field(pattern=EMAIL_PATTERN)
    nombre: str = Field(min_length=1, max_length=255)
    rol: str = ROLE_READER


class UpdateUserRequest(BaseModel):
    """Partial update of a user's role and/or active flag."""

    rol: str | None = None
    activo: bool | None = None


class UserResponse(BaseModel):
    """User projection that never exposes the password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    nombre: str
    rol: str
    activo: bool
    created_at: datetime

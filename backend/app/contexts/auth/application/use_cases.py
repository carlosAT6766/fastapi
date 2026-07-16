"""Application use cases for authentication and user administration."""

from fastapi import HTTPException, status

from app.contexts.auth.application.dto import (
    CreateUserRequest,
    LoginRequest,
    RegisterRequest,
    UpdateUserRequest,
)
from app.contexts.auth.application.ports import UserRepository
from app.contexts.auth.domain import (
    DEFAULT_USER_PASSWORD,
    ROLE_ADMIN,
    is_valid_role,
)
from app.shared.config import get_settings
from app.shared.models import User
from app.shared.security import create_access_token, hash_password, verify_password

settings = get_settings()


def _ensure_valid_role(role: str) -> None:
    """Reject unknown roles with a 422-style validation error."""
    if not is_valid_role(role):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Invalid role: {role}")


class RegisterUser:
    """Create a self-registered user."""

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def __call__(self, payload: RegisterRequest) -> User:
        _ensure_valid_role(payload.rol)
        if await self._users.get_by_email(payload.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
        user = User(
            email=payload.email,
            nombre=payload.nombre,
            password_hash=hash_password(payload.password),
            rol=payload.rol,
            activo=True,
        )
        return await self._users.add(user)


class LoginUser:
    """Validate credentials and return a signed access token.

    Accepts an email or the demo admin username. The demo admin is provisioned
    lazily so the contract works even before the database seed has run.
    """

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def __call__(self, payload: LoginRequest) -> str:
        user = await self._users.get_by_email(payload.usuario)
        if user is None and payload.usuario == settings.demo_admin_username:
            user = await self._ensure_demo_admin(payload.clave)
        if user is None or not verify_password(payload.clave, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        if not user.activo:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Inactive user")
        return create_access_token(user.id, user.email)

    async def _ensure_demo_admin(self, provided_password: str) -> User | None:
        """Create the seeded demo admin on first login if it does not exist."""
        if provided_password != settings.demo_admin_password:
            return None
        admin = await self._users.get_by_email(settings.demo_admin_username)
        if admin is not None:
            return admin
        admin = User(
            email=settings.demo_admin_username,
            nombre="Administrator",
            password_hash=hash_password(settings.demo_admin_password),
            rol=ROLE_ADMIN,
            activo=True,
        )
        return await self._users.add(admin)


class ListUsers:
    """Return every user (admin only)."""

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def __call__(self) -> list[User]:
        return await self._users.list_all()


class CreateUser:
    """Create a user with a default password (admin only)."""

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def __call__(self, payload: CreateUserRequest) -> User:
        _ensure_valid_role(payload.rol)
        if await self._users.get_by_email(payload.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
        user = User(
            email=payload.email,
            nombre=payload.nombre,
            password_hash=hash_password(DEFAULT_USER_PASSWORD),
            rol=payload.rol,
            activo=True,
        )
        return await self._users.add(user)


class UpdateUser:
    """Update a user's role and/or active flag (admin only)."""

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def __call__(self, user_id: int, payload: UpdateUserRequest) -> User:
        user = await self._get_or_404(user_id)
        if payload.rol is not None:
            _ensure_valid_role(payload.rol)
            user.rol = payload.rol
        if payload.activo is not None:
            user.activo = payload.activo
        return await self._users.save(user)

    async def _get_or_404(self, user_id: int) -> User:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user


class DeleteUser:
    """Delete a user (admin only)."""

    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def __call__(self, user_id: int) -> None:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        await self._users.delete(user)

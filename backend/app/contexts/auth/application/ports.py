"""Ports (hexagonal boundaries) for the auth context."""

from typing import Protocol

from app.shared.models import User


class UserRepository(Protocol):
    """Persistence port for users. Adapters live in `infrastructure`."""

    async def get_by_id(self, user_id: int) -> User | None:
        """Return the user with the given id, or None."""
        ...

    async def get_by_email(self, email: str) -> User | None:
        """Return the user with the given email, or None."""
        ...

    async def list_all(self) -> list[User]:
        """Return every user ordered by id."""
        ...

    async def add(self, user: User) -> User:
        """Persist a new user and return it with its generated id."""
        ...

    async def save(self, user: User) -> User:
        """Flush pending changes on a tracked user and return it."""
        ...

    async def delete(self, user: User) -> None:
        """Remove the given user."""
        ...

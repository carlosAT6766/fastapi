"""Auth + Users HTTP entrypoints (hexagonal adapter over the use cases).

Contract (do not rename paths):
  POST  /auth/register  -> create user, return user
  POST  /auth/login     -> {access_token, token_type}
  GET   /auth/me        -> current user
  GET   /users          -> list users            (Admin)
  POST  /users          -> create user           (Admin)
  PATCH /users/{id}     -> update rol/activo      (Admin)
  DELETE /users/{id}    -> delete user            (Admin)
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.contexts.auth.application.dto import (
    CreateUserRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateUserRequest,
    UserResponse,
)
from app.contexts.auth.application.use_cases import (
    CreateUser,
    DeleteUser,
    ListUsers,
    LoginUser,
    RegisterUser,
    UpdateUser,
)
from app.contexts.auth.domain import ROLE_ADMIN
from app.contexts.auth.infrastructure.repository import SqlAlchemyUserRepository
from app.shared.db import get_session
from app.shared.models import User
from app.shared.security import get_current_user, require_role

router = APIRouter(tags=["auth"])


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlAlchemyUserRepository:
    """Provide the SQLAlchemy user repository bound to the request session."""
    return SqlAlchemyUserRepository(session)


@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    users: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> User:
    """Register a new user and return it without the password hash."""
    return await RegisterUser(users)(payload)


@router.post("/auth/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    users: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> TokenResponse:
    """Validate credentials and issue a bearer access token."""
    token = await LoginUser(users)(payload)
    return TokenResponse(access_token=token)


@router.get("/auth/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> User:
    """Return the currently authenticated user."""
    return current_user


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    _: User = Depends(require_role(ROLE_ADMIN)),
    users: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> list[User]:
    """List every user (Admin only)."""
    return await ListUsers(users)()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: CreateUserRequest,
    _: User = Depends(require_role(ROLE_ADMIN)),
    users: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> User:
    """Create a user with the default password (Admin only)."""
    return await CreateUser(users)(payload)


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    payload: UpdateUserRequest,
    _: User = Depends(require_role(ROLE_ADMIN)),
    users: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> User:
    """Change a user's role and/or active flag (Admin only)."""
    return await UpdateUser(users)(user_id, payload)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    _: User = Depends(require_role(ROLE_ADMIN)),
    users: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> None:
    """Delete a user (Admin only)."""
    await DeleteUser(users)(user_id)

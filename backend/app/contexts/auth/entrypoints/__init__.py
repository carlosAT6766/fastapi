"""Auth + Users entrypoints. Teammate A implements the routes below.

Contract (do not rename paths):
  POST /auth/register   -> create user, return user
  POST /auth/login      -> {access_token, token_type}
  GET  /auth/me         -> current user
  GET  /users           -> list users            (Admin)
  POST /users           -> create user           (Admin)
  PATCH /users/{id}     -> update rol/activo      (Admin)
  DELETE /users/{id}    -> delete user            (Admin)
"""

from fastapi import APIRouter

router = APIRouter(tags=["auth"])


@router.get("/auth/health")
async def auth_health() -> dict[str, str]:
    return {"context": "auth", "status": "stub"}

"""Settings entrypoints. Teammate D implements the routes below.

Contract:
  GET /settings -> current user's {default_source, default_style} (defaults if none)
  PUT /settings -> upsert {default_source, default_style}
"""

from fastapi import APIRouter

router = APIRouter(tags=["settings"])


@router.get("/settings/health")
async def settings_health() -> dict[str, str]:
    return {"context": "settings", "status": "stub"}

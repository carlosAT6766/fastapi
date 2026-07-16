"""Settings entrypoints (driving side).

Contract:
  GET /settings -> current user's {default_source, default_style} (defaults if none)
  PUT /settings -> upsert {default_source, default_style}
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.contexts.settings.application.schemas import SettingsRead, SettingsUpdate
from app.contexts.settings.application.use_cases import SettingsService
from app.contexts.settings.domain import Settings
from app.contexts.settings.infrastructure import SqlAlchemySettingsRepository
from app.shared.db import get_session
from app.shared.models import User
from app.shared.security import get_current_user

router = APIRouter(tags=["settings"])


def get_service(session: AsyncSession = Depends(get_session)) -> SettingsService:
    return SettingsService(SqlAlchemySettingsRepository(session))


@router.get("/settings", response_model=SettingsRead)
async def read_settings(
    user: User = Depends(get_current_user),
    service: SettingsService = Depends(get_service),
) -> SettingsRead:
    settings = await service.get_settings(user.id)
    return SettingsRead(**vars(settings))


@router.put("/settings", response_model=SettingsRead)
async def update_settings(
    payload: SettingsUpdate,
    user: User = Depends(get_current_user),
    service: SettingsService = Depends(get_service),
) -> SettingsRead:
    settings = await service.update_settings(
        user.id,
        Settings(default_source=payload.default_source, default_style=payload.default_style),
    )
    return SettingsRead(**vars(settings))

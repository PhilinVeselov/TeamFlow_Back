from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.services.profile_service import get_user_profile, update_user_profile
from src.dependencies.auth import get_current_user
from src.schemas.profile import ProfileOut, ProfileUpdate
from src.models.user import User

router = APIRouter()

@router.get("/profile", response_model=ProfileOut)
async def read_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_user_profile(db, current_user)

@router.patch("/profile", response_model=ProfileOut)
async def edit_profile(
    data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_user_profile(db, current_user, data)

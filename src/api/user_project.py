from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.services.user_project_service import assign_user_to_project
from src.schemas.UserProject import UserProjectCreate, UserProjectRead
from src.dependencies.auth import get_current_user
from src.models import User

router = APIRouter()

@router.post("/", response_model=UserProjectRead)
async def assign(
    data: UserProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ⬅️ токен обязателен
):
    return await assign_user_to_project(db, data)

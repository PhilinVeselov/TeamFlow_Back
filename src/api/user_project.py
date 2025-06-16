from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.services.user_project_service import assign_user_to_project, get_users_in_project, remove_user_from_project
from src.schemas.UserProject import UserProjectCreate, UserProjectRead
from src.dependencies.auth import get_current_user
from src.models import User

router = APIRouter()

@router.post("/", response_model=UserProjectRead)
async def assign_user_to_project_api(
    data: UserProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await assign_user_to_project(db, data, current_user)


@router.get("/project/{id_project}", response_model=list[UserProjectRead])
async def get_users_in_project_api(
    id_project: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_users_in_project(db, id_project)

@router.delete("/{id_user_project}")
async def delete_user_from_project(id_user_project: int, db: AsyncSession = Depends(get_db)):
    await remove_user_from_project(db, id_user_project)
    return {"detail": "Пользователь удалён из проекта"}
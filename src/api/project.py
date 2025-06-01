from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.project_service import create_project, get_all_projects
from src.schemas.project import ProjectCreate, ProjectRead
from src.db.session import get_db
from src.dependencies.auth import get_current_user
from src.models import User

router = APIRouter()

@router.post("/", response_model=ProjectRead)
async def create(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ⬅️ только с токеном
):
    return await create_project(db, data)


@router.get("/", response_model=list[ProjectRead])
async def read_all(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ⬅️ только с токеном
):
    return await get_all_projects(db)

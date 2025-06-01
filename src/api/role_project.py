from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.role_project_service import create_role_project, get_roles
from src.db.session import get_db
from src.schemas.RoleProject import RoleProjectCreate, RoleProjectRead

router = APIRouter()

@router.post("/", response_model=RoleProjectRead)
async def create_role(data: RoleProjectCreate, db: AsyncSession = Depends(get_db)):
    return await create_role_project(db, data.name)

@router.get("/", response_model=list[RoleProjectRead])
async def get_all_roles(db: AsyncSession = Depends(get_db)):
    return await get_roles(db)

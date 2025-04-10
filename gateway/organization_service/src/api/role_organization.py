from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db.session import get_db
from src.schemas.RoleOrganization import RoleOrganizationCreate, RoleOrganizationRead
from src.services.role_organization_service import create_role, get_all_roles

router = APIRouter(prefix="/roles", tags=["Role Organization"])

@router.post("/", response_model=RoleOrganizationRead)
async def add_role(role_data: RoleOrganizationCreate, db: AsyncSession = Depends(get_db)):
    return await create_role(db, role_data)

@router.get("/", response_model=list[RoleOrganizationRead])
async def list_roles(db: AsyncSession = Depends(get_db)):
    return await get_all_roles(db)

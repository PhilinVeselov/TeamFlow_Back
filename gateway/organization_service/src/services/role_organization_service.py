from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from shared.models.RoleOrganization import RoleOrganization
from src.schemas.RoleOrganization import RoleOrganizationCreate

async def create_role(db: AsyncSession, role_data: RoleOrganizationCreate):
    role = RoleOrganization(**role_data.dict())
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role

async def get_all_roles(db: AsyncSession):
    result = await db.execute(select(RoleOrganization))
    return result.scalars().all()

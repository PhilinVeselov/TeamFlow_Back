from sqlalchemy.ext.asyncio import AsyncSession
from src.models.RoleProject import RoleProject
from sqlalchemy.future import select

async def create_role_project(db: AsyncSession, name: str) -> RoleProject:
    role = RoleProject(name=name)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role

async def get_roles(db: AsyncSession):
    result = await db.execute(select(RoleProject))
    return result.scalars().all()

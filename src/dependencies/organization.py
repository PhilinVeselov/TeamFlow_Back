# src/dependencies/organization.py
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.session import get_db
from src.models import User, UserOrganization, RoleOrganization, Organization
from src.dependencies.auth import get_current_user
from fastapi import Body
from src.schemas.project import ProjectCreate

async def get_organization_if_admin_by_id(
    id_organizations: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Organization:
    result = await db.execute(
        select(Organization).where(Organization.id_organizations == id_organizations)
    )
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    result = await db.execute(
        select(UserOrganization)
        .join(RoleOrganization)
        .where(
            UserOrganization.id_user == current_user.id_user,
            UserOrganization.id_organizations == id_organizations,
            UserOrganization.id_role_organization == RoleOrganization.id_role_organization,
            RoleOrganization.name == "Admin"
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Вы не админ в организации")

    return org


async def get_org_by_project_create(
    data: ProjectCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Organization:
    return await get_organization_if_admin_by_id(
        id_organizations=data.id_organizations,
        db=db,
        current_user=current_user
    )
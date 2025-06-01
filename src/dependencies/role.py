from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dependencies.auth import get_current_user
from src.db.session import get_db
from src.models import UserOrganization, RoleOrganization, Organization, User

async def require_admin(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    # Получаем домен без порта
    host = request.headers.get("host")
    if not host:
        raise HTTPException(status_code=400, detail="Не удалось определить домен")
    domein = host.split(":")[0]

    result = await db.execute(
        select(UserOrganization)
        .options(
            joinedload(UserOrganization.role_organization),
            joinedload(UserOrganization.organization)
        )
        .join(RoleOrganization, UserOrganization.id_role_organization == RoleOrganization.id_role_organization)
        .join(Organization, UserOrganization.id_organizations == Organization.id_organizations)
        .where(
            UserOrganization.id_user == current_user.id_user,
            RoleOrganization.name == "Admin",
            Organization.domein == domein
        )
    )

    user_org = result.scalars().first()

    if not user_org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав администратора в текущем домене."
        )

    # Присваиваем организацию и роль текущему пользователю
    object.__setattr__(current_user, "organization", user_org.organization)
    object.__setattr__(current_user, "organization_id", user_org.id_organizations)
    object.__setattr__(current_user, "role_organization", user_org.role_organization)

    return current_user

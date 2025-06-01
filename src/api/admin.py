from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from uuid import uuid4
from sqlalchemy import delete

from src.dependencies.auth import get_current_user
from src.dependencies.role import require_admin
from src.db.session import get_db
from src.models import (
    User,
    InviteOrganization,
    RoleOrganization,
    UserOrganization,
    Organization,
    Project,
    UserProjectHistory,
)
from src.models.user_project import UserProject
from sqlalchemy.future import select

from src.schemas.organization import OrganizationBase, OrganizationRead, OrganizationUp
from src.schemas.UserOrganization import UserOrganizationRead

from src.schemas.UserOrganization import AddUserByEmail
from src.services.email_service import send_invite_email
router = APIRouter()


async def get_organization_by_domain_if_admin(
    domain: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Organization:
    result = await db.execute(
        select(Organization).where(Organization.domein == domain)
    )
    organization = result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    result = await db.execute(
        select(UserOrganization)
        .join(RoleOrganization)
        .where(
            UserOrganization.id_user == current_user.id_user,
            UserOrganization.id_organizations == organization.id_organizations,
            UserOrganization.id_role_organization == RoleOrganization.id_role_organization,
            RoleOrganization.name == "Admin"
        )
    )
    user_org = result.scalar_one_or_none()
    if not user_org:
        raise HTTPException(status_code=403, detail="Вы не админ в этой организации")

    return organization



def check_user_belongs_to_organization(user: User, org: Organization):
    if user.organization_id != org.id_organizations:
        raise HTTPException(status_code=403, detail="Нет доступа к данной организации")


@router.get("/organization/{domain}", response_model=OrganizationRead)
async def get_organization_by_domain(
    domain: str,
    organization: Organization = Depends(get_organization_by_domain_if_admin)
):
    return organization



@router.patch("/organization/{domain}", response_model=OrganizationRead)
async def update_organization(
    domain: str,
    org_update: OrganizationUp,
    db: AsyncSession = Depends(get_db),
    organization: Organization = Depends(get_organization_by_domain_if_admin)
):
    organization.name = org_update.name
    organization.email = org_update.email

    await db.commit()
    await db.refresh(organization)
    return organization

@router.post("/organization/{domain}/add_user")
async def add_or_invite_user(
    domain: str,
    payload: AddUserByEmail,
    db: AsyncSession = Depends(get_db),
    organization: Organization = Depends(get_organization_by_domain_if_admin)
):
    # Поиск пользователя
    result = await db.execute(
        select(User).options(selectinload(User.user_organizations)).where(User.email == payload.email)
    )
    user = result.scalar_one_or_none()

    if user:
        result = await db.execute(
            select(UserOrganization).where(
                UserOrganization.id_user == user.id_user,
                UserOrganization.id_organizations == organization.id_organizations
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Пользователь уже в организации")

        user_email = user.email  # сохранить до commit, чтобы не отвалился lazy-load

        db.add(UserOrganization(
            id_user=user.id_user,
            id_organizations=organization.id_organizations,
            id_role_organization=payload.id_role_organization
        ))
        await db.commit()

        return {"message": f"Пользователь {user_email} добавлен в организацию."}

    # Создание инвайта
    token = str(uuid4())
    invite = InviteOrganization(
        email=payload.email,
        token=token,
        id_organizations=organization.id_organizations,
        id_role_organization=payload.id_role_organization
    )
    db.add(invite)
    await db.commit()

    await send_invite_email(email=payload.email, token=token, domein=domain)
    return {"message": "Пользователь не найден. Отправлено приглашение на почту."}

@router.get("/organization/{domain}/users", response_model=list[UserOrganizationRead])
async def get_users_in_organization(
    domain: str,
    db: AsyncSession = Depends(get_db),
    organization: Organization = Depends(get_organization_by_domain_if_admin)
):
    result = await db.execute(
        select(UserOrganization)
        .where(UserOrganization.id_organizations == organization.id_organizations)
        .options(
            selectinload(UserOrganization.role_organization),
            selectinload(UserOrganization.organization),
        )
    )
    return result.scalars().all()
@router.delete("/organization/{domain}/users/{user_id}", status_code=204)
async def delete_user_from_organization(
    domain: str,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    organization: Organization = Depends(get_organization_by_domain_if_admin),
    current_user: User = Depends(get_current_user),
):
    if user_id == current_user.id_user:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")

    result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.id_user == user_id,
            UserOrganization.id_organizations == organization.id_organizations
        )
    )
    user_org = result.scalar_one_or_none()
    if not user_org:
        raise HTTPException(status_code=404, detail="Пользователь не найден в организации")

    result = await db.execute(
        select(UserProject).join(Project).where(
            UserProject.id_user == user_id,
            Project.id_organizations == organization.id_organizations
        )
    )
    user_projects = result.scalars().all()
    for up in user_projects:
        await db.delete(up)

    await db.execute(
        delete(UserOrganization).where(
            UserOrganization.id_user == user_id,
            UserOrganization.id_organizations == organization.id_organizations
        )
    )


    await db.commit()
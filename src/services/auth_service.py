from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.user_service import get_user_by_email, create_user
from src.schemas.auth import TokenData, RegisterOrganization, RegisterParticipant
from src.core.security import verify_password, create_access_token, get_password_hash
from src.models.user import User
from src.models.organization import Organization
from src.models.UserOrganization import UserOrganization
from src.models.user_technology_stack import UserTechnologyStack
from sqlalchemy import select
from src.models.RoleOrganization import RoleOrganization
from jose import jwt, JWTError
from sqlalchemy.orm import joinedload

from src.core.config import settings
from src.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token, 
    get_password_hash
)


async def get_current_user_from_token(db: AsyncSession, token: str) -> User | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        return None

    result = await db.execute(
        select(User)
        .options(
            joinedload(User.user_organizations).joinedload(UserOrganization.organization),
            joinedload(User.user_organizations).joinedload(UserOrganization.role_organization)
        )
        .where(User.id_user == user_id)
    )
    user = result.unique().scalar_one_or_none()

    if not user:
        return None

    if user.user_organizations:
        first_org_link = user.user_organizations[0]
        user.organization = first_org_link.organization
        user.role_organization = first_org_link.role_organization
        user.organization_id = first_org_link.id_organizations
    else:
        user.organization = None
        user.role_organization = None
        user.organization_id = None

    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def login_for_access_token(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": str(user.id_user)})
    refresh_token = create_refresh_token(data={"sub": str(user.id_user)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

async def get_admin_role_id(db):
    query = select(RoleOrganization).where(RoleOrganization.name == "Admin")
    result = await db.execute(query)
    role = result.scalar_one_or_none()
    if not role:
        raise Exception("Роль Admin не найдена")
    return role.id_role_organization

async def register_participant_user(db: AsyncSession, user_in: RegisterParticipant) -> User:
    existing_user = await get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
        description=user_in.description,
        img=user_in.img,
        is_looking_for_project=True
    )
    db.add(new_user)
    await db.flush()  # чтобы получить id_user

    # Привязка стеков к пользователю
    for tech_id in user_in.technology_stack_ids:
        db.add(UserTechnologyStack(id_user=new_user.id_user, id_technology_stack=tech_id))

    await db.commit()
    await db.refresh(new_user)
    return new_user

async def register_organization_user(db: AsyncSession, data: RegisterOrganization):
    # Проверка: существует ли уже пользователь с таким email
    existing_user = await get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    # 1. Создаём организацию
    organization = Organization(
        name=data.organization_name,
        domein=data.organization_domain,
        email=data.organization_email
    )
    db.add(organization)
    await db.flush()  # чтобы получить ID организации

    # 2. Создаём пользователя, указывая organization_id
    user = User(
        name=data.name,
        email=data.email,
        password=get_password_hash(data.password)
    )
    db.add(user)
    await db.flush()

    # 3. Получаем ID роли Admin
    admin_role = await db.execute(
        select(RoleOrganization).where(RoleOrganization.name == "Admin")
    )
    admin_role_id = admin_role.scalar_one().id_role_organization

    # 4. Связываем пользователя с организацией через UserOrganization
    user_org = UserOrganization(
        id_user=user.id_user,
        id_organizations=organization.id_organizations,
        id_role_organization=admin_role_id
    )
    db.add(user_org)

    # 5. Финализируем
    await db.commit()
    await db.refresh(user)

    return user

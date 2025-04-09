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

from src.core.config import settings
from src.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token, 
    get_password_hash
)


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


async def register_organization_user(db: AsyncSession, data: RegisterOrganization) -> User:
    existing_user = await get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    org = Organization(
        name=data.organization_name,
        domein=data.organization_domain,
        email=data.organization_email
    )
    db.add(org)
    await db.flush()  # получить id_organizations

    hashed_password = get_password_hash(data.password)
    user = User(
        name=data.name,
        email=data.email,
        password=hashed_password
    )
    db.add(user)
    await db.flush()  # получить id_user

    link = UserOrganization(
        id_user=user.id_user,
        id_organizations=org.id_organizations,
        id_role_organization=1  # по умолчанию admin
    )
    db.add(link)
    await db.commit()
    await db.refresh(user)
    return user

from fastapi import APIRouter, Depends, HTTPException, status, Request, File, Form, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select  # ✅
from sqlalchemy.exc import IntegrityError  # ✅
from jose import JWTError, jwt
from uuid import uuid4

from src.schemas.auth import RegisterParticipant, RegisterOrganization, TokenData, LoginSchema
from src.db.session import get_db
from src.services.auth_service import (
    register_organization_user,
    register_participant_user,
    login_for_access_token
)
from src.models import Organization  # ✅
from src.core.security import create_access_token
from src.core.config import settings


router = APIRouter()


@router.post("/register/participant", response_model=TokenData)
async def register_participant(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    description: str = Form(None),
    is_looking_for_project: bool = Form(False),
    technology_stack_ids: list[int] = Form(...),
    img: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    # Сохраняем файл
    img_path = None
    if img:
        ext = img.filename.split('.')[-1]
        file_name = f"{uuid4()}.{ext}"
        file_path = f"src/static/profile_images/{file_name}"
        with open(file_path, "wb") as f:
            f.write(await img.read())
        img_path = f"/static/profile_images/{file_name}"

    # Собираем схему вручную
    user_in = RegisterParticipant(
        name=name,
        email=email,
        password=password,
        description=description,
        img=img_path,
        is_looking_for_project=is_looking_for_project,
        technology_stack_ids=technology_stack_ids
    )

    user = await register_participant_user(db, user_in)
    return await login_for_access_token(db, user.email, password)
@router.post("/register/organization", response_model=TokenData)
async def register_organization(
    data: RegisterOrganization, db: AsyncSession = Depends(get_db)
):
    # 🔍 Проверка на уникальность домена
    result = await db.execute(
        select(Organization).where(Organization.domein == data.organization_domain)
    )

    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Организация с таким доменом уже существует")

    try:
        user = await register_organization_user(db, data)
        return await login_for_access_token(db, user.email, data.password)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка при регистрации организации (возможно, дублируются данные)")

@router.post("/login", response_model=TokenData)
async def login(
    data: LoginSchema,
    db: AsyncSession = Depends(get_db),
):
    return await login_for_access_token(db, data.username, data.password)

    
@router.post("/refresh", response_model=TokenData)
async def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

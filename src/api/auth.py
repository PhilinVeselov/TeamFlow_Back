from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.schemas.auth import RegisterParticipant, RegisterOrganization, TokenData
from src.db.session import get_db
from src.services.auth_service import (
    register_organization_user,
    register_participant_user,
    login_for_access_token
)
from src.core.security import create_access_token
from src.core.config import settings

router = APIRouter()


@router.post("/register/participant", response_model=TokenData)
async def register_participant(
    user_in: RegisterParticipant, db: AsyncSession = Depends(get_db)
):
    user = await register_participant_user(db, user_in)
    return await login_for_access_token(db, user.email, user_in.password)


@router.post("/register/organization", response_model=TokenData)
async def register_organization(
    data: RegisterOrganization, db: AsyncSession = Depends(get_db)
):
    user = await register_organization_user(db, data)
    return await login_for_access_token(db, user.email, data.password)


@router.post("/login", response_model=TokenData)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await login_for_access_token(db, form_data.username, form_data.password)


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

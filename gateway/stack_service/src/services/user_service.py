from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from shared.models.user import User
from src.schemas.user import UserCreate
from shared.core.security import get_password_hash


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(select(User).where(User.id_user == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
        description=user_in.description,
        img=user_in.img,
        id_technology_stack=user_in.id_technology_stack,
        is_looking_for_project=user_in.is_looking_for_project
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

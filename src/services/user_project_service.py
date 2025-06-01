from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user_project import UserProject
from src.schemas.UserProject import UserProjectCreate

async def assign_user_to_project(db: AsyncSession, data: UserProjectCreate) -> UserProject:
    user_project = UserProject(
        id_user=data.id_user,
        id_project=data.id_project,
        id_role_project=data.id_role_project
    )
    db.add(user_project)
    await db.commit()
    await db.refresh(user_project)
    return user_project

async def get_users_in_project(db: AsyncSession, id_project: int):
    result = await db.execute(select(UserProject).where(UserProject.id_project == id_project))
    return result.scalars().all()

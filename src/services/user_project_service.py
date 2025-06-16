from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user_project import UserProject
from src.schemas.UserProject import UserProjectCreate
from sqlalchemy.orm import selectinload
from sqlalchemy import delete
from src.models import User

async def assign_user_to_project(db: AsyncSession, data: UserProjectCreate, current_user: User) -> UserProject:
    # Получение проекта и его организации
    project = await db.execute(
        select(Project).where(Project.id_project == data.id_project)
    )
    project = project.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Проверка, что текущий пользователь админ в этой организации
    result = await db.execute(
        select(UserOrganization)
        .join(RoleOrganization)
        .where(
            UserOrganization.id_user == current_user.id_user,
            UserOrganization.id_organizations == project.id_organizations,
            RoleOrganization.name == "Admin",
            UserOrganization.id_role_organization == RoleOrganization.id_role_organization,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Нет прав добавлять пользователей в этот проект")

    # Проверка, что добавляемый пользователь принадлежит организации
    result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.id_user == data.id_user,
            UserOrganization.id_organizations == project.id_organizations
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь не в организации проекта")

    user_project = UserProject(
        id_user=data.id_user,
        id_project=data.id_project,
        id_role_project=data.id_role_project
    )
    db.add(user_project)
    await db.commit()
    await db.refresh(user_project)
    return user_project

async def remove_user_from_project(db: AsyncSession, id_user_project: int) -> None:
    await db.execute(
        delete(UserProject).where(UserProject.id_user_project == id_user_project)
    )
    await db.commit()

async def get_users_in_project(db: AsyncSession, id_project: int):
    result = await db.execute(
        select(UserProject)
        .where(UserProject.id_project == id_project)
        .options(
            selectinload(UserProject.user),
            selectinload(UserProject.role),
        )
    )
    return result.scalars().all()
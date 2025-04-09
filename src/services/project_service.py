from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from src.models.project import Project
from src.models.UserProject import UserProject
from src.models.UserOrganization import UserOrganization
from src.schemas.project import ProjectBase


async def create_project(db: AsyncSession, project_in: ProjectBase) -> Project:
    new_project = Project(**project_in.dict())
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


async def add_user_to_project(db: AsyncSession, id_user: int, id_project: int, id_role_project: int) -> UserProject:
    # Проверяем, что организация пользователя совпадает с организацией проекта
    project = await db.get(Project, id_project)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    user_org = await db.execute(
        select(UserOrganization).where(UserOrganization.id_user == id_user)
    )
    user_org = user_org.scalar_one_or_none()

    if not user_org or user_org.id_organizations != project.id_organizations:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to the same organization as the project"
        )

    user_project = UserProject(
        id_user=id_user,
        id_project=id_project,
        id_role_project=id_role_project
    )
    db.add(user_project)
    await db.commit()
    await db.refresh(user_project)
    return user_project
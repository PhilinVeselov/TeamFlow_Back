from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.project import Project
from src.schemas.project import ProjectCreate

async def create_project(db: AsyncSession, data: ProjectCreate) -> Project:
    project = Project(**data.dict())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

async def get_all_projects(db: AsyncSession):
    result = await db.execute(select(Project))
    return result.scalars().all()

async def get_project_by_id(db: AsyncSession, id_project: int) -> Project:
    result = await db.execute(select(Project).where(Project.id_project == id_project))
    return result.scalar_one_or_none()

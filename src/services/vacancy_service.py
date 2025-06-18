from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.vacancy import Vacancy
from src.schemas.vacancy import VacancyCreate

async def create_vacancy(db: AsyncSession, data: VacancyCreate):
    vacancy = Vacancy(**data.dict())
    db.add(vacancy)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy

async def deactivate_vacancy(db: AsyncSession, id_vacancy: int):
    result = await db.execute(select(Vacancy).where(Vacancy.id_vacancy == id_vacancy))
    vacancy = result.scalar_one_or_none()
    if vacancy:
        vacancy.is_active = False
        await db.commit()
        await db.refresh(vacancy)
    return vacancy

async def get_active_vacancy_projects(db: AsyncSession):
    from src.models.project import Project
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(Project)
        .join(Project.vacancies)
        .filter(Vacancy.is_active == True)
        .options(selectinload(Project.organization), selectinload(Project.technology_stacks))
        .distinct()
    )
    return result.scalars().all()

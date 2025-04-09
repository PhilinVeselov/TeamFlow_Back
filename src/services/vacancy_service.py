from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from src.models.vacancy import Vacancy
from src.models.VacancyResponse import VacancyResponse
from src.schemas.vacancy import VacancyBase


async def create_vacancy(db: AsyncSession, vacancy_in: VacancyBase) -> Vacancy:
    vacancy = Vacancy(**vacancy_in.dict())
    db.add(vacancy)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy


async def respond_to_vacancy(db: AsyncSession, id_vacancy: int, id_user: int, status: str = "pending") -> VacancyResponse:
    # Проверить, что вакансия существует
    vacancy = await db.get(Vacancy, id_vacancy)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    response = VacancyResponse(
        id_vacancy=id_vacancy,
        id_user=id_user,
        status=status
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.vacancy import VacancyCreate, VacancyOut
from src.services.vacancy_service import create_vacancy, deactivate_vacancy
from src.db.session import get_db

router = APIRouter()

@router.post("/", response_model=VacancyOut)
async def publish_vacancy(data: VacancyCreate, db: AsyncSession = Depends(get_db)):
    return await create_vacancy(db, data)

@router.patch("/{id_vacancy}/deactivate", response_model=VacancyOut)
async def close_vacancy(id_vacancy: int, db: AsyncSession = Depends(get_db)):
    vacancy = await deactivate_vacancy(db, id_vacancy)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
    return vacancy

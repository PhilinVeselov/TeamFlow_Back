from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # ← добавь, если забыл
from shared.db.session import get_db
from shared.models.TechnologyStack import TechnologyStack
from src.schemas.TechnologyStack import TechnologyStackCreate, TechnologyStackOut
from typing import List

router = APIRouter()

@router.post("/", response_model=TechnologyStackOut)
async def create_stack(
    stack_data: TechnologyStackCreate, db: AsyncSession = Depends(get_db)
):
    new_stack = TechnologyStack(name=stack_data.name)
    db.add(new_stack)
    await db.commit()
    await db.refresh(new_stack)
    return new_stack

@router.get("/", response_model=List[TechnologyStackOut])
async def get_all_stacks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TechnologyStack))
    return result.scalars().all()

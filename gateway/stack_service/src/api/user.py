from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db.session import get_db
from src.services.user_service import get_user_by_id
from src.schemas.user import UserRead
from pydantic import BaseModel
from typing import List

router = APIRouter()

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
class AddStacksToUser(BaseModel):
    user_id: int
    technology_stack_ids: List[int]

@router.post("/add-stacks")
async def add_tech_stacks(data: AddStacksToUser, db: AsyncSession = Depends(get_db)):
    for tech_id in data.technology_stack_ids:
        link = UserTechnologyStack(id_user=data.user_id, id_technology_stack=tech_id)
        db.add(link)
    await db.commit()
    return {"status": "success", "message": f"Добавлены стеки для пользователя {data.user_id}"}
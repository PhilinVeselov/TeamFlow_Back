from fastapi import FastAPI
from src.api.router import router
from src.services.role_organization_service import create_default_roles
from src.db.session import get_async_session

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    async with get_async_session() as session:
        await create_default_roles(session)

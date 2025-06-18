from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- добавь это
from fastapi.staticfiles import StaticFiles

from src.api.router import router
from src.services.role_organization_service import create_default_roles
from src.db.session import get_async_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ТВОЙ фронт
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    async with get_async_session() as session:
        await create_default_roles(session)

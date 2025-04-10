from fastapi import FastAPI
from src.api.role_organization import router as role_router

app = FastAPI(title="Organization Service")

app.include_router(role_router, prefix="/roles")



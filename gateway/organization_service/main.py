from fastapi import FastAPI
from src.api.organization import router as organization_router
from src.api.role_organization import router as role_router

app = FastAPI(title="Organization Service")

app.include_router(organization_router, prefix="/organization")
app.include_router(role_router, prefix="/roles")

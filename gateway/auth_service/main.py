from fastapi import FastAPI
from src.api.auth import router as auth_router  

app = FastAPI(title="Auth Service")
app.include_router(auth_router, prefix="/auth")


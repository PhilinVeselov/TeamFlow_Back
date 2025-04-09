from fastapi import FastAPI
from src.api.auth import router as auth_router  
from src.api.user import router as user_router
from src.api.technology_stack import router as tech_router

app = FastAPI(title="Auth Service")
app.include_router(auth_router, prefix="/auth")



app = FastAPI(title="User Service")
app.include_router(user_router, prefix="/users")
app.include_router(tech_router, prefix="/technology-stack")

from fastapi import APIRouter
from src.api import auth, user, technology_stack, role_organization

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(technology_stack.router, prefix="/technology-stack", tags=["Technology Stack"])
router.include_router(role_organization.router)

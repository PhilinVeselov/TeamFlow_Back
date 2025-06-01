from fastapi import APIRouter
from src.api import auth, user, technology_stack, role_organization, profile, admin,  project, role_project, user_project

router = APIRouter()


router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(technology_stack.router, prefix="/technology-stack", tags=["Technology Stack"])
router.include_router(role_organization.router)
router.include_router(profile.router, tags=["Profile"])
router.include_router(admin.router, prefix="/admin", tags=["Admin"])
router.include_router(project.router, prefix="/projects", tags=["Project"])
router.include_router(role_project.router, prefix="/roles-project", tags=["RoleProject"])
router.include_router(user_project.router, prefix="/user-project", tags=["UserProject"])

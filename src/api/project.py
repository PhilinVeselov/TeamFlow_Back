from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.project_service import create_project, get_user_projects, update_project
from src.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from src.db.session import get_db
from src.dependencies.auth import get_current_user
from src.models import User
from src.models import Organization
from fastapi import Body
from src.dependencies.organization import get_org_by_project_create
from fastapi import HTTPException
from sqlalchemy.future import select
from src.models.project import Project
from sqlalchemy.orm import selectinload
from src.services.email_service import send_project_apply_email
from src.models import UserOrganization, RoleOrganization

router = APIRouter()

@router.post("/", response_model=ProjectRead)
async def create(
    data: ProjectCreate = Body(...),
    organization: Organization = Depends(get_org_by_project_create),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_project(db, data, current_user.id_user)

@router.get("/", response_model=list[ProjectRead])
async def read_user_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_user_projects(db, current_user.id_user)

@router.get("/public", response_model=list[ProjectRead])
async def get_all_projects(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).options(selectinload(Project.organization))
    )
    projects = result.scalars().all()
    return [ProjectRead.model_validate(p) for p in projects]

@router.post("/{id_project}/apply")
async def apply_to_project(
    id_project: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id_project == id_project))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    admins_result = await db.execute(
        select(User)
        .join(UserOrganization)
        .join(RoleOrganization)
        .where(
            UserOrganization.id_organizations == project.id_organizations,
            UserOrganization.id_user == User.id_user,
            UserOrganization.id_role_organization == RoleOrganization.id_role_organization,
            RoleOrganization.name == "Admin"
        )
    )
    admins = admins_result.scalars().all()

    for admin in admins:
        await send_project_apply_email(
            to_user_email=current_user.email,
            to_admin_email=admin.email,
            user_name=current_user.name,
            project_name=project.name
        )

    return {"message": f"Вы откликнулись на проект {project.name}"}

@router.patch("/{id_project}", response_model=ProjectRead)
async def patch_project(
    id_project: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = await get_project_by_id(db, id_project)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    org = await get_organization_if_admin_by_id(project.id_organizations, db, current_user)
    return await update_project(db, id_project, data)

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
from fastapi import Query

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



@router.get("/filter", response_model=list[ProjectRead])
async def filter_projects(
    tech_stack_ids: list[int] = Query(None),
    role_ids: list[int] = Query(None),
    is_paid: bool | None = None,
    is_remote: bool | None = None,
    organization_ids: list[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    from src.models.vacancy import Vacancy  # ⬅️ важно

    query = (
        select(Project)
        .join(Vacancy)
        .options(
            selectinload(Project.organization),
            selectinload(Project.technology_stacks),
            selectinload(Project.vacancies).selectinload(Vacancy.role)  # 👈 добавляем, если выводишь vacancy.role.name
        )
        .where(Vacancy.is_active == True)
    )

    if tech_stack_ids:
        query = query.join(Project.technology_stacks).where(TechnologyStack.id_technology_stack.in_(tech_stack_ids))

    if role_ids:
        query = query.where(Vacancy.id_role_project.in_(role_ids))

    if is_paid is not None:
        query = query.where(Project.is_paid == is_paid)

    if is_remote is not None:
        query = query.where(Project.is_remote == is_remote)

    if organization_ids:
        query = query.where(Project.id_organizations.in_(organization_ids))

    result = await db.execute(query)
    projects = result.scalars().unique().all()
    return [ProjectRead.from_orm(p) for p in projects]


@router.post("/{id_project}/apply")
async def apply_to_project(
    id_project: int,
    id_vacancy: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Получаем проект
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.vacancies))
        .where(Project.id_project == id_project)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Если указан id_vacancy — ищем вакансию
    vacancy_name = None
    if id_vacancy:
        vacancy = next((v for v in project.vacancies if v.id_vacancy == id_vacancy), None)
        if not vacancy or not vacancy.is_active:
            raise HTTPException(status_code=404, detail="Вакансия не найдена или неактивна")
        vacancy_name = vacancy.name

    # Получаем админов организации
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

    # Формируем сообщение
    subject = f"Вы откликнулись на проект: {project.name}"
    if vacancy_name:
        subject = f"Вы откликнулись на вакансию: {vacancy_name} в проекте: {project.name}"

    for admin in admins:
        await send_project_apply_email(
            to_user_email=current_user.email,
            to_admin_email=admin.email,
            user_name=current_user.name,
            project_name=subject
        )

    return {"message": subject}

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

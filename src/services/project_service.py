from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate
from src.models.user import User
from src.models.user_project import UserProject
from src.models.RoleProject import RoleProject
from sqlalchemy.orm import selectinload
from src.schemas.project import ProjectRead
from src.models import UserOrganization, RoleOrganization

async def create_project(db: AsyncSession, data: ProjectCreate, id_user: int) -> Project:
    project = Project(**data.dict())
    db.add(project)
    await db.commit()
    await db.refresh(project)

    # Получаем роль "Admin"
    result = await db.execute(select(RoleProject).where(RoleProject.name == "Admin"))
    admin_role = result.scalar_one_or_none()
    if not admin_role:
        raise ValueError("Role 'Admin' not found")

    # Привязка пользователя к проекту
    user_project = UserProject(
        id_user=id_user,
        id_project=project.id_project,
        id_role_project=admin_role.id_role_project
    )
    db.add(user_project)
    await db.commit()

    # 🔥 ВАЖНО: подгружаем организацию
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.organization))  # <---
        .where(Project.id_project == project.id_project)
    )
    project_with_organization = result.scalar_one()
    return ProjectRead.model_validate(project_with_organization)

async def get_user_projects(db: AsyncSession, id_user: int) -> list[ProjectRead]:
    # 1. Получаем список ID организаций, где пользователь — админ
    result = await db.execute(
        select(UserOrganization.id_organizations)
        .join(RoleOrganization)
        .where(
            UserOrganization.id_user == id_user,
            UserOrganization.id_role_organization == RoleOrganization.id_role_organization,
            RoleOrganization.name == "Admin"
        )
    )
    admin_org_ids = [row[0] for row in result.fetchall()]

    if admin_org_ids:
        # 2. Если пользователь админ хотя бы в одной организации — получаем все проекты из этих организаций
        result = await db.execute(
            select(Project)
            .options(selectinload(Project.organization))
            .where(Project.id_organizations.in_(admin_org_ids))
        )
    else:
        # 3. Иначе — только те, в которых он участвует
        result = await db.execute(
            select(Project)
            .join(UserProject)
            .options(selectinload(Project.organization))
            .where(UserProject.id_user == id_user)
        )

    projects = result.scalars().all()
    return [ProjectRead.model_validate(p) for p in projects]

async def get_project_by_id(db: AsyncSession, id_project: int):
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.organization))  # 🔥 Важно!
        .where(Project.id_project == id_project)
    )
    return result.scalar_one_or_none()
async def update_project(db: AsyncSession, id_project: int, data: ProjectUpdate) -> Project:
    result = await db.execute(select(Project).where(Project.id_project == id_project))
    project = result.scalar_one_or_none()
    if not project:
        raise ValueError("Project not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    await db.commit()

    # 🔥 Подгружаем организацию перед возвратом
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.organization))
        .where(Project.id_project == id_project)
    )
    return result.scalar_one()

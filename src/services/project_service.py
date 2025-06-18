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
from src.models.TechnologyStack import TechnologyStack

async def create_project(db: AsyncSession, data: ProjectCreate, id_user: int) -> ProjectRead:
    # Убираем лишнее поле (оно есть только в pydantic-схеме)
    project_data = data.dict(exclude={"technology_stack_ids"})

    project = Project(**project_data)
    db.add(project)
    await db.commit()
    await db.refresh(project)

    # Привязка технологий к проекту
    if data.technology_stack_ids:
        result = await db.execute(
            select(TechnologyStack).where(TechnologyStack.id_technology_stack.in_(data.technology_stack_ids))
        )
        technologies = result.scalars().all()
        project.technology_stacks.extend(technologies)
        await db.commit()

    # Назначение роли
    result = await db.execute(select(RoleProject).where(RoleProject.name == "Admin"))
    admin_role = result.scalar_one_or_none()
    if not admin_role:
        raise ValueError("Role 'Admin' not found")

    user_project = UserProject(
        id_user=id_user,
        id_project=project.id_project,
        id_role_project=admin_role.id_role_project
    )
    db.add(user_project)
    await db.commit()

    # Возврат с подгрузкой
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.organization), selectinload(Project.technology_stacks))
        .where(Project.id_project == project.id_project)
    )
    return ProjectRead.model_validate(result.scalar_one())

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
            .options(selectinload(Project.organization),  selectinload(Project.technology_stacks))
            .where(Project.id_organizations.in_(admin_org_ids))
        )
    else:
        # 3. Иначе — только те, в которых он участвует
        result = await db.execute(
            select(Project)
            .join(UserProject)
            .options(selectinload(Project.organization),  selectinload(Project.technology_stacks))
            .where(UserProject.id_user == id_user)
        )

    projects = result.scalars().all()
    return [ProjectRead.model_validate(p) for p in projects]

async def get_project_by_id(db: AsyncSession, id_project: int):
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.organization),  selectinload(Project.technology_stacks))
        .where(Project.id_project == id_project)
    )
    return result.scalar_one_or_none()

async def update_project(db: AsyncSession, id_project: int, data: ProjectUpdate) -> ProjectRead:
    result = await db.execute(select(Project).where(Project.id_project == id_project))
    project = result.scalar_one_or_none()
    if not project:
        raise ValueError("Project not found")

    update_data = data.dict(exclude_unset=True, exclude={"technology_stack_ids"})
    for key, value in update_data.items():
        setattr(project, key, value)

    # Обновляем стеки технологий, если переданы
    if "technology_stack_ids" in data.model_fields_set:
        result = await db.execute(
            select(TechnologyStack).where(TechnologyStack.id_technology_stack.in_(data.technology_stack_ids))
        )
        technologies = result.scalars().all()
        project.technology_stacks = technologies  # полная замена
    await db.commit()

    result = await db.execute(
        select(Project)
        .options(selectinload(Project.organization), selectinload(Project.technology_stacks))
        .where(Project.id_project == id_project)
    )
    return ProjectRead.model_validate(result.scalar_one())

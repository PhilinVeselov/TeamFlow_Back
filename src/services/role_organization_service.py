from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.RoleOrganization import RoleOrganization
from src.schemas.RoleOrganization import RoleOrganizationCreate

async def create_role(db: AsyncSession, role_data: RoleOrganizationCreate) -> RoleOrganization:
    role = RoleOrganization(
        id_role_organization=role_data.id_role_organization,
        name=role_data.name
    )
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role

async def get_all_roles(db: AsyncSession):
    result = await db.execute(select(RoleOrganization))
    return result.scalars().all()
async def create_default_roles(db):
    default_roles = ["Admin", "User"]

    # Получаем уже существующие роли из базы
    result = await db.execute(select(RoleOrganization).where(RoleOrganization.name.in_(default_roles)))
    existing_roles = result.scalars().all()
    existing_role_names = {role.name for role in existing_roles}

    # Создаём только те роли, которых ещё нет
    for role_name in default_roles:
        if role_name not in existing_role_names:
            db.add(RoleOrganization(name=role_name))
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
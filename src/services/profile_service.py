from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user import User
from src.models.user_technology_stack import UserTechnologyStack
from src.schemas.profile import ProfileOut, ProfileUpdate
from src.schemas.organization import OrganizationRead
from src.schemas.RoleOrganization import RoleOrganizationRead
from src.schemas.UserOrganization import UserOrganizationRead
async def get_user_profile(db: AsyncSession, current_user: User) -> ProfileOut:
    await db.refresh(current_user, attribute_names=["technology_stacks", "user_organizations"])

    technology_stack = [
        {"id_technology_stack": tech.id_technology_stack, "name": tech.name}
        for tech in current_user.technology_stacks
    ]

    user_organizations = []
    for uo in current_user.user_organizations:
        user_organizations.append(
            UserOrganizationRead(
                id_user_organization=uo.id_user_organization,
                id_user=uo.id_user,
                id_organizations=uo.id_organizations,
                id_role_organization=uo.id_role_organization,
                organization=OrganizationRead(
                    id_organizations=uo.organization.id_organizations,
                    name=uo.organization.name,
                    domein=uo.organization.domein,
                    email=uo.organization.email,
                ),
                role_organization=RoleOrganizationRead(
                    id_role_organization=uo.role_organization.id_role_organization,
                    name=uo.role_organization.name,
                )
            )

        )

    return ProfileOut(
        id_user=current_user.id_user,
        name=current_user.name,
        email=current_user.email,
        description=current_user.description,
        img=current_user.img,
        technology_stack=technology_stack,
        user_organizations=user_organizations  # ✅ преобразованные вручную
    )

async def update_user_profile(db: AsyncSession, current_user: User, data: ProfileUpdate) -> ProfileOut:
    if data.name is not None:
        current_user.name = data.name
    if data.description is not None:
        current_user.description = data.description
    if data.img is not None:
        current_user.img = data.img

    if data.technology_stack_ids is not None:
        await db.execute(
            UserTechnologyStack.__table__.delete().where(
                UserTechnologyStack.id_user == current_user.id_user
            )
        )
        for tech_id in data.technology_stack_ids:
            db.add(UserTechnologyStack(id_user=current_user.id_user, id_technology_stack=tech_id))

    user_id = current_user.id_user

    await db.commit()

    refreshed_user = await db.get(User, user_id)

    return await get_user_profile(db, refreshed_user)

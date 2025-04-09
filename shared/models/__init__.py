from shared.db.base import Base

from shared.models.user import User
from shared.models.organization import Organization
from shared.models.project import Project
from shared.models.vacancy import Vacancy
from shared.models.TechnologyStack import TechnologyStack
from shared.models.RoleProject import RoleProject
from shared.models.RoleOrganization import RoleOrganization
from shared.models.UserOrganization import UserOrganization
from shared.models.UserProject import UserProject
from shared.models.UserProjectHistory import UserProjectHistory
from shared.models.VacancyResponse import VacancyResponse

__all__ = [
    "Base",
    "User",
    "Organization",
    "Project",
    "Vacancy",
    "TechnologyStack",
    "RoleProject",
    "RoleOrganization",
    "UserOrganization",
    "UserProject",
    "UserProjectHistory",
    "VacancyResponse"
]

target_metadata = Base.metadata

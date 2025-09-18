from api.base import BaseCRUDRouter
from services.role_service import role_service
from models.models import Role
from schemas.schemas import RoleCreate, RoleUpdate, RoleResponse


class RoleRouter(BaseCRUDRouter[Role, RoleCreate, RoleUpdate, RoleResponse]):
    """Router for role endpoints"""

    def __init__(self):
        super().__init__(
            prefix="/roles",
            resource="roles",
            service=role_service,
            create_schema=RoleCreate,
            update_schema=RoleUpdate,
            response_schema=RoleResponse,
        )


# Create role router instance
role_router = RoleRouter().router

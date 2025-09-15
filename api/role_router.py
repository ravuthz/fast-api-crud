from api.base import BaseCRUDRouter
from services.role_service import role_service
from models.models import Role
from schemas.schemas import RoleCreate, RoleUpdate, RoleResponse

class RoleRouter(BaseCRUDRouter[Role, RoleCreate, RoleUpdate, RoleResponse]):
    """Router for role endpoints"""
    
    def __init__(self):
        super().__init__(
            service=role_service,
            response_schema=RoleResponse,
            prefix="/roles",
            tags=["roles"]
        )
    
    def get_resource_name(self) -> str:
        return "roles"

# Create role router instance
role_router = RoleRouter().router
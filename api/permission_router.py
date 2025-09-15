from api.base import BaseCRUDRouter
from services.permission_service import permission_service
from models.models import Permission
from schemas.schemas import PermissionCreate, PermissionUpdate, PermissionResponse

class PermissionRouter(BaseCRUDRouter[Permission, PermissionCreate, PermissionUpdate, PermissionResponse]):
    """Router for permission endpoints"""
    
    def __init__(self):
        super().__init__(
            service=permission_service,
            response_schema=PermissionResponse,
            prefix="/permissions",
            tags=["permissions"]
        )
    
    def get_resource_name(self) -> str:
        return "permissions"

# Create permission router instance
permission_router = PermissionRouter().router
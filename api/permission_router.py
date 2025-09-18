from api.base import BaseCRUDRouter
from services.permission_service import permission_service
from models.models import Permission
from schemas.schemas import PermissionCreate, PermissionUpdate, PermissionResponse


class PermissionRouter(
    BaseCRUDRouter[Permission, PermissionCreate, PermissionUpdate, PermissionResponse]
):
    """Router for permission endpoints"""

    def __init__(self):
        super().__init__(
            prefix="/permissions",
            resource="permissions",
            service=permission_service,
            create_schema=PermissionCreate,
            update_schema=PermissionUpdate,
            response_schema=PermissionResponse,
        )


# Create permission router instance
permission_router = PermissionRouter().router

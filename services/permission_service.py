from sqlalchemy.orm import Session
from models.models import Permission
from schemas.schemas import PermissionCreate, PermissionUpdate
from services.base import BaseService

class PermissionService(BaseService[Permission, PermissionCreate, PermissionUpdate]):
    """Service for permission operations"""
    
    def __init__(self):
        super().__init__(Permission)
    
    def get_by_name(self, db: Session, name: str) -> Permission:
        """Get permission by name"""
        return self.get_by_field(db, "name", name)

# Global permission service instance
permission_service = PermissionService()
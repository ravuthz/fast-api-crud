from sqlalchemy.orm import Session
from models.models import Role, Permission
from schemas.schemas import RoleCreate, RoleUpdate
from services.base import BaseService

class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    """Service for role operations"""
    
    def __init__(self):
        super().__init__(Role)
    
    def get_by_name(self, db: Session, name: str) -> Role:
        """Get role by name"""
        return self.get_by_field(db, "name", name)
    
    def _prepare_create_data(self, data: dict) -> dict:
        """Remove permission_ids from data"""
        data.pop("permission_ids", None)  # Handle separately in post_create
        return data
    
    def _prepare_update_data(self, data: dict) -> dict:
        """Remove permission_ids from data"""
        data.pop("permission_ids", None)  # Handle separately in post_update
        return data
    
    def _post_create(self, db: Session, db_obj: Role, obj_in: RoleCreate) -> None:
        """Assign permissions after role creation"""
        if obj_in.permission_ids:
            permissions = db.query(Permission).filter(Permission.id.in_(obj_in.permission_ids)).all()
            db_obj.permissions = permissions
            db.commit()
    
    def _post_update(self, db: Session, db_obj: Role, obj_in: RoleUpdate) -> None:
        """Update permissions after role update"""
        if obj_in.permission_ids is not None:
            permissions = db.query(Permission).filter(Permission.id.in_(obj_in.permission_ids)).all()
            db_obj.permissions = permissions
            db.commit()

# Global role service instance
role_service = RoleService()
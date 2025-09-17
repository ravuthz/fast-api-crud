from sqlalchemy.orm import Session
from models.models import User, Role
from schemas.schemas import UserCreate, UserUpdate
from services.base import BaseService
from services.auth_service import auth_service

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for user operations"""
    
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User:
        """Get user by email"""
        return self.get_by_field(db, "email", email)

    def get_by_username(self, db: Session, username: str) -> User:
        """Get user by username"""
        return self.get_by_field(db, "username", username)

    def authenticate(self, db: Session, username: str, password: str) -> User | None:
        """Authenticate user with username and password"""
        user = self.get_by_username(db, username)
        if not user or not auth_service.verify_password(password, user.hashed_password):
            return None
        return user
    
    def _prepare_create_data(self, data: dict) -> dict:
        """Hash password before creating user"""
        if "password" in data:
            data["hashed_password"] = auth_service.get_password_hash(data.pop("password"))
        data.pop("role_ids", None)  # Handle separately in post_create
        return data
    
    def _prepare_update_data(self, data: dict) -> dict:
        """Hash password before updating user"""
        if "password" in data:
            data["hashed_password"] = auth_service.get_password_hash(data.pop("password"))
        data.pop("role_ids", None)  # Handle separately in post_update
        return data
    
    def _post_create(self, db: Session, db_obj: User, obj_in: UserCreate) -> None:
        """Assign roles after user creation"""
        if obj_in.role_ids:
            roles = db.query(Role).filter(Role.id.in_(obj_in.role_ids)).all()
            db_obj.roles = roles
            db.commit()
    
    def _post_update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> None:
        """Update roles after user update"""
        if obj_in.role_ids is not None:
            roles = db.query(Role).filter(Role.id.in_(obj_in.role_ids)).all()
            db_obj.roles = roles
            db.commit()

# Global user service instance
user_service = UserService()
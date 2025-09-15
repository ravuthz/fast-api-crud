from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.connection import db_manager
from services.auth_service import auth_service
from services.user_service import user_service
from models.models import User
from typing import List

security = HTTPBearer()

def get_db() -> Session:
    """Dependency to get database session"""
    return next(db_manager.get_db())

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    username = auth_service.verify_token(token)
    user = user_service.get_by_username(db, username=username)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

class PermissionChecker:
    """Class-based permission checker for cleaner dependency injection"""
    
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_permissions = current_user.get_permissions()
        
        for required_permission in self.required_permissions:
            if required_permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required: {required_permission}"
                )
        
        return current_user

def require_permissions(permissions: List[str]):
    """Factory function to create permission checker"""
    return PermissionChecker(permissions)
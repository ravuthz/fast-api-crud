from sqlalchemy import Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import BaseModel

# Association tables for many-to-many relationships
user_roles = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('role_id', ForeignKey('roles.id'))
)

role_permissions = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('role_id', ForeignKey('roles.id')),
    Column('permission_id', ForeignKey('permissions.id'))
)

class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    def has_permission(self, resource: str, action: str) -> bool:
        """Check if user has specific permission"""
        for role in self.roles:
            for permission in role.permissions:
                if permission.resource == resource and permission.action == action:
                    return True
        return False
    
    def get_permissions(self) -> list[str]:
        """Get all user permissions as resource:action format"""
        permissions = []
        for role in self.roles:
            for permission in role.permissions:
                perm_string = f"{permission.resource}:{permission.action}"
                if perm_string not in permissions:
                    permissions.append(perm_string)
        return permissions

class Role(BaseModel):
    __tablename__ = "roles"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(BaseModel):
    __tablename__ = "permissions"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    resource = Column(String, nullable=False)
    action = Column(String, nullable=False)
    
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
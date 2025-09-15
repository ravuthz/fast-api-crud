from pydantic import EmailStr
from typing import List, Optional
from schemas.base import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema

# Permission schemas
class PermissionBase(BaseCreateSchema):
    name: str
    description: Optional[str] = None
    resource: str
    action: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseUpdateSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None

class PermissionResponse(PermissionBase, BaseResponseSchema):
    pass

# Role schemas
class RoleBase(BaseCreateSchema):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []

class RoleUpdate(BaseUpdateSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None

class RoleResponse(RoleBase, BaseResponseSchema):
    permissions: List[PermissionResponse] = []

# User schemas
class UserBase(BaseCreateSchema):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role_ids: Optional[List[int]] = []

class UserUpdate(BaseUpdateSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[int]] = None

class UserResponse(UserBase, BaseResponseSchema):
    is_active: bool
    roles: List[RoleResponse] = []

# Authentication schemas
class Token(BaseCreateSchema):
    access_token: str
    token_type: str

class TokenData(BaseCreateSchema):
    username: Optional[str] = None

class UserLogin(BaseCreateSchema):
    username: str
    password: str
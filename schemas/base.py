from pydantic import BaseModel, ConfigDict
from typing import Optional, Generic, TypeVar, List
from datetime import datetime
from abc import ABC, abstractmethod

# Generic type for model
ModelType = TypeVar('ModelType')

class BaseSchema(BaseModel, ABC):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True)

class BaseCreateSchema(BaseSchema, ABC):
    """Base schema for create operations"""
    pass

class BaseUpdateSchema(BaseSchema, ABC):
    """Base schema for update operations"""
    pass

class BaseResponseSchema(BaseSchema, ABC):
    """Base schema for response operations"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class PaginationSchema(BaseSchema):
    """Schema for pagination parameters"""
    skip: int = 0
    limit: int = 100

class ResponseListSchema(BaseSchema, Generic[ModelType]):
    """Generic schema for list responses"""
    items: List[ModelType]
    total: int
    skip: int
    limit: int
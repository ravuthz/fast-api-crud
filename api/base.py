from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Type
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from api.dependencies import get_db, require_permissions
from services.base import BaseService
from schemas.base import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema, ResponseListSchema
from models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseResponseSchema)

class BaseCRUDRouter(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    """Base CRUD router with common endpoints"""
    
    def __init__(
        self,
        service: BaseService[ModelType, CreateSchemaType, UpdateSchemaType],
        response_schema: Type[ResponseSchemaType],
        prefix: str,
        tags: List[str]
    ):
        self.service = service
        self.response_schema = response_schema
        self.router = APIRouter(prefix=prefix, tags=tags)
        self._setup_routes()
    
    @abstractmethod
    def get_resource_name(self) -> str:
        """Get resource name for permissions"""
        pass
    
    def _setup_routes(self):
        """Setup common CRUD routes"""
        resource = self.get_resource_name()
        
        @self.router.post("/", response_model=self.response_schema)
        async def create_item(
            item = Body(),
            db: Session = Depends(get_db),
            current_user = Depends(require_permissions([f"{resource}:create"]))
        ):
            print("create user: ")
            print(item)
            return self.service.create(db, item)
        
        @self.router.get("/", response_model=List[self.response_schema])
        async def read_items(
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db),
            current_user = Depends(require_permissions([f"{resource}:read"]))
        ):
            return self.service.get_multi(db, skip=skip, limit=limit)
        
        @self.router.get("/{item_id}", response_model=self.response_schema)
        async def read_item(
            item_id: int,
            db: Session = Depends(get_db),
            current_user = Depends(require_permissions([f"{resource}:read"]))
        ):
            db_item = self.service.get(db, item_id)
            if db_item is None:
                raise HTTPException(status_code=404, detail=f"{resource.title()} not found")
            return db_item
        
        @self.router.put("/{item_id}", response_model=self.response_schema)
        async def update_item(
            item_id: int,
            item: UpdateSchemaType,
            db: Session = Depends(get_db),
            current_user = Depends(require_permissions([f"{resource}:update"]))
        ):
            db_item = self.service.get(db, item_id)
            if db_item is None:
                raise HTTPException(status_code=404, detail=f"{resource.title()} not found")
            return self.service.update(db, db_item, item)
        
        @self.router.delete("/{item_id}")
        async def delete_item(
            item_id: int,
            db: Session = Depends(get_db),
            current_user = Depends(require_permissions([f"{resource}:delete"]))
        ):
            success = self.service.delete(db, item_id)
            if not success:
                raise HTTPException(status_code=404, detail=f"{resource.title()} not found")
            return {"message": f"{resource.title()} deleted successfully"}

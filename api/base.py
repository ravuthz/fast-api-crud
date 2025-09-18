import json

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Type
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from api.dependencies import get_db, require_permissions
from services.base import BaseService
from schemas.base import (
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    ResponseListSchema,
)
from models.base import BaseModel
from starlette import status


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseResponseSchema)


class BaseCRUDRouter(
    ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]
):
    """Base CRUD router with common endpoints"""

    def __init__(
        self,
        service: BaseService[ModelType, CreateSchemaType, UpdateSchemaType],
        prefix: str,
        resource: str,
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
        response_schema: Type[ResponseSchemaType],
    ):
        self.service = service
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self.resource = resource
        self.router = APIRouter(prefix=prefix, tags=[resource])
        self._setup_routes()

    def _setup_routes(self):
        """Setup common CRUD routes"""
        # resource = self.get_resource_name()

        @self.router.post(
            "/",
            response_model=self.response_schema,
            status_code=status.HTTP_201_CREATED,
        )
        async def create_item(
            item: self.create_schema,
            db: Session = Depends(get_db),
            current_user=Depends(require_permissions([f"{self.resource}:create"])),
        ):
            print(f"The {self.resource} create payload")
            print(json.dumps(item.model_dump(), indent=2, ensure_ascii=False))
            return self.service.create(db, item)

        @self.router.get("/", response_model=List[self.response_schema])
        async def read_items(
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db),
            current_user=Depends(require_permissions([f"{self.resource}:read"])),
        ):
            return self.service.get_multi(db, skip=skip, limit=limit)

        @self.router.get("/{item_id}", response_model=self.response_schema)
        async def read_item(
            item_id: int,
            db: Session = Depends(get_db),
            current_user=Depends(require_permissions([f"{self.resource}:read"])),
        ):
            db_item = self.service.get(db, item_id)
            if db_item is None:
                raise HTTPException(
                    status_code=404, detail=f"{self.resource.title()} not found"
                )
            return db_item

        @self.router.put("/{item_id}", response_model=self.response_schema)
        async def update_item(
            item_id: int,
            item: self.update_schema,
            db: Session = Depends(get_db),
            current_user=Depends(require_permissions([f"{self.resource}:update"])),
        ):
            print(f"The {self.resource} update payload")
            print(json.dumps(item.model_dump(), indent=2, ensure_ascii=False))
            db_item = self.service.get(db, item_id)
            if db_item is None:
                raise HTTPException(
                    status_code=404, detail=f"{self.resource.title()} not found"
                )
            return self.service.update(db, db_item, item)

        @self.router.delete("/{item_id}")
        async def delete_item(
            item_id: int,
            db: Session = Depends(get_db),
            current_user=Depends(require_permissions([f"{self.resource}:delete"])),
        ):
            success = self.service.delete(db, item_id)
            if not success:
                raise HTTPException(
                    status_code=404, detail=f"{self.resource.title()} not found"
                )
            return {"message": f"{self.resource.title()} deleted successfully"}

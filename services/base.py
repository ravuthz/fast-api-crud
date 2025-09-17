from abc import ABC
from typing import TypeVar, Generic, Optional, List, Type, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.base import BaseModel
from schemas.base import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema
from fastapi import HTTPException, status

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)

class BaseService(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base service class with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get single record by id"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get multiple records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def count(self, db: Session) -> int:
        """Get total count of records"""
        return db.query(self.model).count()
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create new record"""
        try:
            obj_data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in.dict()
            db_obj = self.model(**self._prepare_create_data(obj_data))
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            self._post_create(db, db_obj, obj_in)
            # return {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Creation failed: {str(e.orig)}"
            )
    
    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """Update existing record"""
        try:
            update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, 'model_dump') else obj_in.dict(exclude_unset=True)
            update_data = self._prepare_update_data(update_data)
            
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            db.commit()
            db.refresh(db_obj)
            self._post_update(db, db_obj, obj_in)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Update failed: {str(e.orig)}"
            )
    
    def delete(self, db: Session, id: int) -> bool:
        """Delete record by id"""
        db_obj = self.get(db, id)
        if not db_obj:
            return False
        
        self._pre_delete(db, db_obj)
        db.delete(db_obj)
        db.commit()
        return True
    
    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        """Get record by specific field"""
        return db.query(self.model).filter(getattr(self.model, field) == value).first()
    
    # Hook methods for customization
    def _prepare_create_data(self, data: dict) -> dict:
        """Prepare data before create operation"""
        return data
    
    def _prepare_update_data(self, data: dict) -> dict:
        """Prepare data before update operation"""
        return data
    
    def _post_create(self, db: Session, db_obj: ModelType, obj_in: CreateSchemaType) -> None:
        """Hook called after successful create"""
        pass
    
    def _post_update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> None:
        """Hook called after successful update"""
        pass
    
    def _pre_delete(self, db: Session, db_obj: ModelType) -> None:
        """Hook called before delete"""
        pass
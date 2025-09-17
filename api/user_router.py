from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status

from api.base import BaseCRUDRouter
from api.dependencies import get_db
from services.user_service import user_service, UserService
from models.models import User
from schemas.schemas import UserCreate, UserUpdate, UserResponse

user_router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return user_service.create(db, user_in)


@user_router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_multi(db, skip, limit)


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.get(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update(db, db_user, user_in)


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete(db, user_id)
    return {"message": "User deleted successfully"}
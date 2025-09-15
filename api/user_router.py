from api.base import BaseCRUDRouter
from services.user_service import user_service
from models.models import User
from schemas.schemas import UserCreate, UserUpdate, UserResponse

class UserRouter(BaseCRUDRouter[User, UserCreate, UserUpdate, UserResponse]):
    """Router for user endpoints"""
    
    def __init__(self):
        super().__init__(
            service=user_service,
            response_schema=UserResponse,
            prefix="/users",
            tags=["users"]
        )
    
    def get_resource_name(self) -> str:
        return "users"

# Create user router instance
user_router = UserRouter().router
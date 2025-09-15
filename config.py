import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str = "your-secret-key-change-in-production"
    database_url: str = "postgresql://username:password@localhost/fastapi_crud"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
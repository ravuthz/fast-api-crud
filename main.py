from fastapi import FastAPI
from database.connection import db_manager
from api.auth_router import router as auth_router
from api.user_router import user_router
from api.role_router import role_router
from api.permission_router import permission_router

# Create database tables
db_manager.create_tables()

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI CRUD with OOP Base Implementation",
    description="A comprehensive CRUD API with user, role, and permission management using OOP principles",
    version="1.0.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)

@app.get("/")
async def root():
    return {"message": "FastAPI CRUD with OOP Base Implementation"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
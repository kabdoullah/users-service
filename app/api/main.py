from fastapi import APIRouter

from app.api.routers import user, login

api_router = APIRouter()

api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])

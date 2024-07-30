from fastapi import APIRouter

from app.api import login, user 

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, tags=["users"])
from fastapi import APIRouter

from app.api.routers import user, login, profile, right, category, subcategory

api_router = APIRouter()

api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    profile.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(right.router, prefix="/rights", tags=["Rights"])
api_router.include_router(
    category.router, prefix="/categories", tags=["Categories"])
api_router.include_router(subcategory.router,
                          prefix="/subcategories", tags=["SubCategories"])

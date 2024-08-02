from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.exceptions.custom_exception import CategoryNotFoundException
from app.models.data.category import Category
from app.models.requests.category import CategoryCreate, CategoryInDB
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("/", response_model=List[CategoryInDB])
def get_all_categories(service: CategoryService = Depends(CategoryService)):
    return service.get_all_categories()


@router.get("/{category_id}", response_model=CategoryInDB)
def get_category_by_id(category_id: UUID, service: CategoryService = Depends(CategoryService)):
    try:
        return service.get_category_by_id(category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/{category_id}", response_model=CategoryInDB)
def get_category_by_id(category_id: UUID, service: CategoryService = Depends(CategoryService)):
    try:
        return service.get_category_by_id(category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/", response_model=CategoryInDB)
def create_category(category: CategoryCreate, service: CategoryService = Depends(CategoryService)):
    return service.create_category(category)


@router.put("/{category_id}", response_model=CategoryInDB)
def update_category(category_id: UUID, category: CategoryCreate, service: CategoryService = Depends(CategoryService)):
    try:
        return service.update_category(category_id, category)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{category_id}")
def delete_category(category_id: UUID, service: CategoryService = Depends(CategoryService)):
    try:
        service.delete_category(category_id)
        return {"message": "Catégorie supprimée"}
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

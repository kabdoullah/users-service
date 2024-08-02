from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.exceptions.custom_exception import SubCategoryNotFoundException
from app.models.data.category import SubCategory
from app.models.requests.category import SubCategoryCreate, SubCategoryInDB
from app.repository.subcategory_repository import SubCategoryRepository


router = APIRouter()


@router.get("/", response_model=List[SubCategoryInDB])
def get_all_subcategories(service: SubCategoryRepository = Depends()):
    return service.get_all_subcategories()


@router.get("/{subcategory_id}", response_model=SubCategoryInDB)
def get_subcategory_by_id(subcategory_id: UUID, service: SubCategoryRepository = Depends()):
    try:
        return service.get_subcategory_by_id(subcategory_id)
    except SubCategoryNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/", response_model=SubCategoryInDB)
def create_subcategory(subcategory: SubCategoryCreate, service: SubCategoryRepository = Depends(SubCategoryRepository)):
    return service.create_subcategory(subcategory)


@router.put("/{subcategory_id}", response_model=SubCategoryInDB)
def update_subcategory(subcategory_id: UUID, subcategory: SubCategoryCreate, service: SubCategoryRepository = Depends(SubCategoryRepository)):
    try:
        return service.update_subcategory(subcategory_id, subcategory)
    except SubCategoryNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{subcategory_id}")
def delete_subcategory(subcategory_id: UUID, service: SubCategoryRepository = Depends(SubCategoryRepository)):
    try:
        service.delete_subcategory(subcategory_id)
        return {"detail": "SubCategory deleted"}
    except SubCategoryNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

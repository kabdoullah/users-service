from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.exceptions.custom_exception import RightNotFoundException
from app.models.requests.right import RightCreate, RightInDB
from app.services.right_service import RightService


router = APIRouter()


@router.get("/", response_model=List[RightInDB])
def get_all_rights(service: RightService = Depends()):
    return service.get_all_rights()


@router.get("/{right_id}", response_model=RightInDB)
def get_right_by_id(right_id: UUID, service: RightService = Depends()):
    try:
        return service.get_right_by_id(right_id)
    except RightNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/", response_model=RightInDB)
def create_right(right: RightCreate, service: RightService = Depends(RightService)):
    return service.create_right(right)


@router.put("/{right_id}", response_model=RightInDB)
def update_right(right_id: UUID, right: RightCreate, service: RightService = Depends(RightService)):
    try:
        return service.update_right(right_id, right)
    except RightNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{right_id}")
def delete_right(right_id: UUID, service: RightService = Depends(RightService)):
    try:
        service.delete_right(right_id)
        return {"message": "Droit supprimé"}
    except RightNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

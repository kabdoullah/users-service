from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.exceptions.custom_exception import ProfileNotFoundException
from app.models.requests.profile import ProfileCreate, ProfileInDB, ProfileUpdate
from app.services.profile_service import ProfileService

router = APIRouter()


@router.get("/", response_model=List[ProfileInDB])
def get_all_profiles(service: ProfileService = Depends(ProfileService)):
    return service.get_all_profiles()


@router.get("/{profile_id}", response_model=ProfileInDB)
def get_profile_by_id(profile_id: UUID, service: ProfileService = Depends(ProfileService)):
    try:
        return service.get_profile_by_id(profile_id)
    except ProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/", response_model=ProfileInDB)
def create_profile(profile: ProfileCreate, service: ProfileService = Depends(ProfileService)):
    return service.create_profile(profile)


@router.put("/{profile_id}", response_model=ProfileInDB)
def update_profile(profile_id: UUID, profile: ProfileUpdate, service: ProfileService = Depends(ProfileService)):
    try:
        return service.update_profile(profile_id, profile)
    except ProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{profile_id}")
def delete_profile(profile_id: UUID, service: ProfileService = Depends(ProfileService)):
    try:
        service.delete_profile(profile_id)
        return {"message": "Profil supprimé"}
    except ProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

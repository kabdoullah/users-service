from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProfileBase(BaseModel):
    name: str

class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass

class ProfileInDB(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True


class ProfileRightBase(BaseModel):
    profile_id: UUID
    right_id: UUID

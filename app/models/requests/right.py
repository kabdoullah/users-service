from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class RightBase(BaseModel):
    name: str


class RightCreate(RightBase):
    pass


class RightUpdate(RightBase):
    pass

class RightInDB(RightBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True

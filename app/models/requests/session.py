from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class SessionCreate(BaseModel):
    user_id: UUID4
    token: str
    expired_at: Optional[datetime] = None

class SessionResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    expired_at: Optional[datetime]
    token: str

    class Config:
        from_attributes = True

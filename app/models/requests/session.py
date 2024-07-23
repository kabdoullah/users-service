from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class SessionCreate(BaseModel):
    user_id: UUID4
    token: str
    expired_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

class SessionResponse(BaseModel):
    acces_token: str
    refresh_token: str
    token_type: str = "bearer"
    

    class Config:
        from_attributes = True
        
class SessionData(BaseModel):
    user_id: UUID4

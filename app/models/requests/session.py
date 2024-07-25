from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class SessionCreate(BaseModel):
    user_id: UUID4
    token: str
    expired_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

class LoginSuccessResponse(BaseModel):
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    attempts_left: int
    
    class ConfigDict:
        from_attributes = True

class LoginErrorResponse(BaseModel):
    message: str
    attempts_left: int
    

        
class SessionData(BaseModel):
    user_id: UUID4
    
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

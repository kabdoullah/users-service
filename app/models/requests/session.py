from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class SessionCreate(BaseModel):
    user_id: UUID4
    access_token: str
    refresh_token: str
    expired_at: Optional[datetime] = None
    


class SessionData(BaseModel):
    user_id: UUID4
    
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

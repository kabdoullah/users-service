from datetime import date
from typing import Union
from uuid import UUID
from pydantic import BaseModel

class Session(BaseModel):
    id: UUID
    user_id : UUID
    created_at : Union[date, None] = None 
    expired_at : Union[date, None] = None 



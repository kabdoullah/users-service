from datetime import date
from typing import Union
from uuid import UUID
from .user import UserBase

class ParticularUser(UserBase):
    
    id: UUID
    birth_day: Union[date, None] = None 

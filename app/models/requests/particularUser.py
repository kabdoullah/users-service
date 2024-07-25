from datetime import date
from typing import Union
from pydantic import UUID4
from .user import UserBase

class ParticularUser(UserBase):
    id: UUID4
    birth_day: Union[date, None] = None 

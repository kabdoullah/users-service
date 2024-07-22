import re
from datetime import datetime, date
from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator

class Session(Base):
    id: UUID
    user_id : UUID
    created_at : Union[date, None] = None 
    expired_at : Union[date, None] = None 



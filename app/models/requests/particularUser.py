import re
from datetime import datetime, date
from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator

class ParticularUser(UsersBase):
    
    id: UUID
    birth_day: Union[date, None] = None 
    
    @field_validator('password')
    def password_password(cls, value: str) -> str:
        if not validate_password_complexity(value):
            raise ValueError(
                'Password must be at least 8 characters long, include an uppercase letter, '
                'a lowercase letter, a digit, and a special character.'
            )
        return value
import re
from datetime import datetime, date
from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator


class ProfessionalUser(UsersBase):
    phone_2: Union[str, None] = Field(None, min_length=10, max_length=15)
    company: Union[str, None] = None
    country: Union[str, None] = None
    company_type: Union[str, None] = None
    professional_category: Union[str, None] = None
    sub_category: Union[str, None] = None
    website: Union[str, None] = None

    
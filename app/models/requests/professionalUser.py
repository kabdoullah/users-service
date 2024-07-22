from typing import Union
from pydantic import Field
from .user import UserBase


class ProfessionalUser(UserBase):
    phone_2: Union[str, None] = Field(None, min_length=10, max_length=15)
    company: Union[str, None] = None
    country: Union[str, None] = None
    company_type: Union[str, None] = None
    professional_category: Union[str, None] = None
    sub_category: Union[str, None] = None
    website: Union[str, None] = None

    
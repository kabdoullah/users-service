from typing import Union
from pydantic import UUID4, Field
from .user import UserBase


class ProfessionalUser(UserBase):
    id: UUID4
    number_fix : str = Field(..., min_length=10, max_length=50)
    company: Union[str, None] = None
    country: Union[str, None] = None
    company_type: Union[str, None] = None
    professional_category: Union[str, None] = None
    sub_category: Union[str, None] = None
    website: Union[str, None] = None

    
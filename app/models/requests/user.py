

from datetime import date
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator
from app.utils.password import validate_password_complexity



class UserBase(BaseModel):
    id: UUID4
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    type: str = Field(..., min_length=3, max_length=50)
    

    @field_validator('password')
    def password_password(cls, value: str) -> str:
        if not validate_password_complexity(value):
            raise ValueError(
                'Password must be at least 8 characters long, include an uppercase letter, '
                'a lowercase letter, a digit, and a special character.'
            )
        return value

    class Config:
        from_attributes = True

class UserParticular(UserBase):
    id: UUID4
    birth_day : date
    phone: str = Field(..., min_length=10, max_length=15)

class UserProfessional(UserBase):
    id: UUID4
    number_fix : str = Field(..., min_length=2, max_length=50)
    company : str = Field(...,min_length=3,max_length=50)
    country : str = Field(...,min_length=3,max_length=50)
    company_type : str = Field(...,min_length=3,max_length=50)
    professional_category : str = Field(...,min_length=3,max_length=50)
    sub_category : str = Field(...,min_length=3,max_length=50)
    website : str = Field(...,min_length=3,max_length=50)

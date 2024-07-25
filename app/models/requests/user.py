from datetime import date
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator
from app.utils.password import validate_password_complexity

        
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    new_password: str
    otp: str

    # @field_validator('new_password')
    # def password_new_password(cls, value: str) -> str:
    #     if not validate_password_complexity(value):
    #         raise ValueError(
    #             'Password must be at least 8 characters long, include an uppercase letter, '
    #             'a lowercase letter, a digit, and a special character.'
    #         )
    #     return value

class UserParticular(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    birth_day : date
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
    
    
    # @field_validator('password')
    # def password_password(cls, value: str) -> str:
    #     if not validate_password_complexity(value):
    #         raise ValueError(
    #             'Password must be at least 8 characters long, include an uppercase letter, '
    #             'a lowercase letter, a digit, and a special character.'
    #         )
    #     return value

class UserProfessional(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    number_fix : str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    company : str = Field(...,min_length=3,max_length=50)
    country : str = Field(...,min_length=3,max_length=50)
    professional_category : str = Field(...,min_length=3,max_length=50)
    sub_category : str = Field(...,min_length=3,max_length=50)
    website : str = Field(...,min_length=3,max_length=50)
    
    
    # @field_validator('password')
    # def password_password(cls, value: str) -> str:
    #     if not validate_password_complexity(value):
    #         raise ValueError(
    #             'Password must be at least 8 characters long, include an uppercase letter, '
    #             'a lowercase letter, a digit, and a special character.'
    #         )
    #     return value

class UserResponse(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    type: str
    is_active: bool
    number_fix: str | None = None
    company: str | None = None
    country: str | None = None
    professional_category: str | None = None
    sub_category: str | None = None
    website: str | None = None
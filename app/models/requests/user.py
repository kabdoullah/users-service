from pydantic import BaseModel, EmailStr, Field, field_validator
from app.utils.password import validate_password_complexity



class UserBase(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8, max_length=50)
    type: str = Field(..., min_length=8, max_length=50)

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
        
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    new_password: str
    otp: str

    @field_validator('new_password')
    def password_new_password(cls, value: str) -> str:
        if not validate_password_complexity(value):
            raise ValueError(
                'Password must be at least 8 characters long, include an uppercase letter, '
                'a lowercase letter, a digit, and a special character.'
            )
        return value
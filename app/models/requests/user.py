from datetime import date
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator
import pycountry


# Générer la liste des pays
COUNTRIES = [country.name for country in pycountry.countries]


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    new_password: str = Field(..., min_length=6, max_length=50)


class UserParticular(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    birth_day: date
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)


class UserEnterprise(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    number_fix: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=4, max_length=50)
    company: str = Field(..., min_length=3, max_length=50)
    company_type: str = Field(..., min_length=3, max_length=50)
    country: str = Field(..., min_length=3, max_length=50)
    category_id: str = Field(..., min_length=3, max_length=50)
    sub_category_id: str = Field(..., min_length=3, max_length=50)
    website: str = Field(..., min_length=3, max_length=50)

    @field_validator('country')
    def validate_country(cls, value: str) -> str:
        if value not in COUNTRIES:
            raise ValueError('Invalid country')
        return value


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
    company_type: str | None = None
    country: str | None = None
    category_id: str | None = None
    sub_category: str | None = None
    website: str | None = None


# class UserBase(BaseModel):
#     first_name: str
#     last_name: str
#     email: EmailStr
#     phone: str | None
#     profile_photo: str | None
#     birth_day: date | None
#     number_fix: str | None
#     company: str | None
#     country: str | None
#     website: str | None
#     gender: str
#     is_active: bool

#     @field_validator('country')
#     def validate_country(cls, value: str) -> str:
#         if value not in COUNTRIES:
#             raise ValueError('Invalid country')
#         return value


# class UserCreate(UserBase):
#     password: str


# class UserUpdate(UserBase):
#     password: str | None


# class UserInDB(UserBase):
#     id: UUID
#     reference: str
#     created_at: datetime
#     updated_at: datetime

#     class ConfigDict:
#         from_attributes = True

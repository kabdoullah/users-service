from datetime import date, datetime
from uuid import UUID
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator
import pycountry

from app.models.data.user import GenderEnum


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
    id: UUID
    reference: str
    first_name: str
    last_name: str
    email: str
    phone: str
    profile_id: UUID
    profile_photo: str | None = None
    birth_day: date | None = None
    birth_place: str | None = None
    number_fix: str | None = None
    company: str | None = None
    country: str | None = None
    category_id: UUID | None = None
    sub_category_id: UUID | None = None
    website: str | None = None
    gender: GenderEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    profile_photo: str | None
    birth_day: date | None
    birth_place: str | None
    type: str
    gender: GenderEnum


class UserCreate(UserBase):
    reference: str | None = None
    password: str


class UserUpdate(UserBase):
    password: str | None


class UserInDB(UserBase):
    id: UUID
    reference: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True

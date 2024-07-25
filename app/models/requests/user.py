from datetime import date
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator
import pycountry


# Générer la liste des pays
COUNTRIES = [country.name for country in pycountry.countries]
        
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    new_password: str
    otp: str


class UserParticular(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    birth_day : date
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=50)
    


class UserProfessional(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    number_fix : str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4, max_length=50)
    company : str = Field(...,min_length=3,max_length=50)
    country : str = Field(...,min_length=3,max_length=50)
    professional_category : str = Field(...,min_length=3,max_length=50)
    sub_category : str = Field(...,min_length=3,max_length=50)
    website : str = Field(...,min_length=3,max_length=50)

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
    country: str | None = None
    professional_category: str | None = None
    sub_category: str | None = None
    website: str | None = None
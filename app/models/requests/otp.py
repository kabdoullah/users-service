import re
from datetime import datetime, date
from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator

class OTP(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., min_length=6, max_length=6)


    class Config:
        from_attributes = True
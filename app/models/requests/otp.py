from pydantic import BaseModel, EmailStr, Field

class OTP(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., min_length=6, max_length=6)


    class Config:
        from_attributes = True
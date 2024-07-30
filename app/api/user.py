from typing import Annotated, List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.dependencies.auth import get_current_active_user
from app.exceptions.custom_exception import EmailAlreadyUsedException, UserNotFoundException
from app.models.data.user import User
from app.models.requests.otp import OTPVerify
from app.models.requests.user import UserParticular, UserProfessional, UserResponse
from app.security.security import generate_otp
from app.services.otp_service import OTPService
from app.services.user_service import UserService
from app.utils.email import send_otp_email
import pycountry

router = APIRouter()

# Générer la liste des pays
COUNTRIES = [country.name for country in pycountry.countries]

@router.get("/countries", response_model=List[str])
def get_countries():
    return COUNTRIES

@router.post("/register/particular", response_model=UserResponse)
async def register_user(user_data: UserParticular, background_tasks: BackgroundTasks, userservice: UserService = Depends(UserService), otpservice: OTPService = Depends(OTPService)):
    db_user = userservice.get_user_by_email(user_data.email)
    if db_user:
        raise EmailAlreadyUsedException()
    new_user = userservice.create_particular(user_data)
    
    return new_user


@router.post("/register/professionnal", response_model=UserResponse)
async def register_professionel(user_data: UserProfessional,  background_tasks: BackgroundTasks, userservice: UserService = Depends(UserService), otpservice: OTPService = Depends(OTPService)):
    db_user = userservice.get_user_by_email(user_data.email)
    if db_user:
        raise EmailAlreadyUsedException()
     
    new_user = userservice.create_professional(user_data)
    
    return new_user

@router.post("/send-otp")
async def send_otp_route(email: str, background_tasks: BackgroundTasks, otpservice: OTPService = Depends(OTPService), userservice: UserService = Depends(UserService)):
    db_user = userservice.get_user_by_email(email)
    if db_user:
        raise EmailAlreadyUsedException()
    otp, expiry_time = generate_otp()
    otpservice.store_register_otp(otp=otp, expiry_time=expiry_time, email=email)
    await send_otp_email(email, otp, background_tasks)  
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp_route(data: OTPVerify, otpservice: OTPService = Depends(OTPService), userservice: UserService = Depends(UserService)):
    db_user = userservice.get_user_by_email(data.email)
    if not db_user:
        raise UserNotFoundException()
    if not otpservice.validate_otp(user_id=db_user.id,otp=data.otp_code):
        raise HTTPException(status_code=400, detail="Invalid OTP or OTP expired")
    return {"message": "OTP verified"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

# @router.get("/users/", response_model=List[User])
# def get_all_users(service: UserService = Depends()):
#     return service.get_all_users()

# @router.get("/users/{user_id}", response_model=User)
# def get_user_by_id(user_id: int, service: UserService = Depends()):
#     user = service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, user: UserBase, service: UserService = Depends()):
#     updated_user = service.update_user(user)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user

# @router.delete("/users/{user_id}", response_model=bool)
# def delete_user(user_id: int, service: UserService = Depends()):
#     success = service.delete_user(user_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found")
#     return success

# @router.post("/users/reset_password/", response_model=User)
# def reset_password(email: str, new_password: str, service: UserService = Depends()):
#     user = service.reset_password(email, new_password)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found or invalid OTP")
#     return user

# @router.post("/users/update_password/", response_model=User)
# def update_password(user_id: int, new_password: str, service: UserService = Depends()):
#     user = service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     updated_user = service.update_password(user, new_password)
#     return updated_user

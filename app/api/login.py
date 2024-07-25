from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from app.exceptions.custom_exception import InvalidTokenException, UserNotFoundException
from app.models.requests.user import PasswordResetConfirm, PasswordResetRequest
from app.security.security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, decode_access_token, generate_otp, hash_password
from app.services.otp_service import OTPService
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.models.requests.session import LoginErrorResponse, LoginSuccessResponse, SessionCreate, Token
from app.utils.email import send_otp_email



router = APIRouter()

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  user_service: UserService = Depends(UserService), session_service: SessionService = Depends(SessionService)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    try:
        result = user_service.authenticate_user(email=form_data.username, password=form_data.password)
        if "user" not in result:
            return LoginErrorResponse(message=result["message"], attempts_left=result["attempts_left"]) 
        
        user = result["user"]
        
        access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": user.id}, expires_delta=refresh_token_expires)
        
        session_service.create_session(session_data=SessionCreate(user_id=user.id, token=access_token, expires_at=access_token_expires))
        
        return LoginSuccessResponse(
            message="Login successful",
            access_token=access_token,
            refresh_token=refresh_token, 
            attempts_left=result["attempts_left"]
        )
    except HTTPException as e:
        raise e
    
    
   
@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, userservice: UserService = Depends(UserService), session_service: SessionService = Depends(SessionService)):

    try:
        token_data = decode_access_token(refresh_token)
    except InvalidTokenError:
        raise InvalidTokenException()

    user = userservice.get_user_by_id(token_data.user_id)
    if not user:
        raise UserNotFoundException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    session_service.create_session(session_data=SessionCreate(user_id=user.id, token=access_token, expires_at=access_token_expires))

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    

@router.post("/password-reset-request")
async def password_reset_request(data: PasswordResetRequest, background_tasks: BackgroundTasks, userservice: UserService = Depends(UserService), otpservice: OTPService = Depends(OTPService)):
    user = userservice.get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")
    
    otp, expiry_time = generate_otp()
    otpservice.store_otp(otp=otp, expiry_time=expiry_time, user_id=user.id)
    await send_otp_email(user.email, otp, background_tasks)
    return {"message": "OTP sent to email"}

@router.post("/password-reset-confirm")
def password_reset_confirm(data: PasswordResetConfirm, otpservice: OTPService = Depends(OTPService), userservice: UserService = Depends(UserService)):
    if not otpservice.verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP or OTP expired")
    
    data.new_password = hash_password(data.new_password)
    user = userservice.reset_password(data.email, data.new_password)
    if not user:
        raise HTTPException(status_code=400, detail="Password reset failed")
    
    return {"message": "Password reset successfully"}
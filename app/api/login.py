from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.exceptions.custom_exception import InvalidCredentialsException
from app.security.security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, verify_password
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.models.requests.session import SessionResponse, SessionCreate



router = APIRouter()

@router.post("/login", response_model=SessionResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  userservice: UserService = Depends(UserService), token_service: SessionService = Depends(SessionService)):
    user = userservice.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    token_service.store_token(token=SessionResponse(token=access_token, user_id=user.id, expires_at=access_token_expires))
    refresh_token = create_refresh_token(data={"sub": user.id}, expires_delta=refresh_token_expires)

    return SessionResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
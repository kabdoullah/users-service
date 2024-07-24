from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.exceptions.custom_exception import InvalidCredentialsException, InactiveUserException
from app.security.security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.models.requests.session import SessionResponse, SessionCreate



router = APIRouter()

@router.post("/login", response_model=SessionResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  user_service: UserService = Depends(UserService), session_service: SessionService = Depends(SessionService)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    try:
        result = user_service.authenticate_user(email=form_data.username, password=form_data.password)
        if "user" not in result:
            return result
        
        user = result["user"]
        
        access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": user.id}, expires_delta=refresh_token_expires)
        
        session_service.create_session(session_data=SessionCreate(user_id=user.id, token=access_token,created_at=datetime.now(timezone.utc), expires_at=access_token_expires))
        
        return {"message": "Login successful", "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    


    
   

    
    
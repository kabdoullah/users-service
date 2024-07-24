from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.exceptions.custom_exception import InvalidCredentialsException, InactiveUserException
from app.security.security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.models.requests.session import LoginResponse, SessionCreate



router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    user_service: UserService = Depends(UserService), 
    session_service: SessionService = Depends(SessionService)
):
    """
    Route de connexion qui authentifie l'utilisateur et génère des tokens d'accès et de rafraîchissement.

    Args:
        form_data (OAuth2PasswordRequestForm): Formulaire de connexion contenant l'email et le mot de passe.
        user_service (UserService): Service utilisateur pour les opérations d'authentification.
        session_service (SessionService): Service de session pour gérer les sessions utilisateur.

    Returns:
        SessionResponse: Réponse contenant les tokens d'accès et de rafraîchissement.
    """
    # Authentification de l'utilisateur
    user = user_service.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise InvalidCredentialsException()
    elif not user.is_active:
        raise InactiveUserException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.id}, expires_delta=refresh_token_expires)
    
    session_data = SessionCreate(
        user_id=user.id,
        token=access_token,
        expires_at=datetime.now(timezone.utc) + access_token_expires
    )
    
    session_service.create_session(session_data=session_data)
    
    return LoginResponse(acces_token=access_token, refresh_token=refresh_token)

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
import logfire
from app.configuration.config import AuthSettings
from app.exceptions.custom_exception import EmailNotRegisterException, InactiveUserException, InvalidOTPException, InvalidTokenException, PasswordResetFailedException, UserNotFoundException
from app.models.requests.otp import OTPVerify
from app.models.requests.user import PasswordResetConfirm, PasswordResetRequest
from app.security.security import create_access_token, create_refresh_token, decode_access_token, generate_otp
from app.services.otp_service import OTPService
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.models.requests.session import SessionCreate, Token
from app.utils.email import send_otp_email

auth_settings = AuthSettings()

router = APIRouter()


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  user_service: UserService = Depends(UserService), session_service: SessionService = Depends(SessionService)):
    """
    Route de connexion pour authentifier un utilisateur et générer des tokens d'accès.

    :param form_data: Formulaire de requête contenant les données d'authentification de l'utilisateur
    :param user_service: Service d'utilisateur pour gérer l'authentification
    :param session_service: Service de session pour créer et gérer les sessions utilisateur
    :return: Réponse de succès de connexion contenant les tokens d'accès et de rafraîchissement
    :raises HTTPException: Si l'authentification échoue
    """

    access_token_expires = timedelta(
        minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(
        minutes=auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    try:
        user = user_service.authenticate_user(
            email=form_data.username, password=form_data.password)

        if not user.is_active:
            logfire.warn(
                f"Utilisateur inactif avec email {form_data.username}.")
            raise InactiveUserException()

        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}, expires_delta=refresh_token_expires)

        session_service.create_session(session_data=SessionCreate(
            user_id=user.id, token=access_token, expires_at=access_token_expires))

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    except HTTPException as e:
        logfire.error(
            f"Échec de la connexion pour l'utilisateur avec email {form_data.username}: {e.detail}")
        raise e


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, userservice: UserService = Depends(UserService), session_service: SessionService = Depends(SessionService)):
    """
    Route pour rafraîchir le token d'accès en utilisant le token de rafraîchissement.

    :param refresh_token: Token de rafraîchissement
    :param userservice: Service d'utilisateur pour gérer les opérations utilisateur
    :param session_service: Service de session pour gérer les sessions utilisateur
    :return: Nouveaux tokens d'accès et de rafraîchissement
    :raises HTTPException: Si le token est invalide ou si l'utilisateur n'est pas trouvé
    """
    try:
        token_data = decode_access_token(refresh_token)
    except InvalidTokenError:
        logfire.warn("Token de rafraîchissement invalide.")
        raise InvalidTokenException()

    user = userservice.get_user_by_id(token_data.user_id)
    if not user:
        logfire.warn(f"Utilisateur non trouvé pour l'ID {token_data.user_id}.")
        raise UserNotFoundException()

    access_token_expires = timedelta(
        minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires)
    session_service.create_session(session_data=SessionCreate(
        user_id=user.id, token=access_token, expires_at=access_token_expires))

    logfire.info(f"Token rafraîchi pour l'utilisateur avec ID {user.id}.")
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/verify-otp")
def verify_otp_route(data: OTPVerify, otpservice: OTPService = Depends(OTPService), userservice: UserService = Depends(UserService)):
    db_user = userservice.get_user_by_email(data.email)
    if not db_user:
        raise UserNotFoundException()
    if not otpservice.validate_otp(user_id=db_user.id, otp=data.otp_code):
        raise HTTPException(
            status_code=400, detail="Invalid OTP or OTP expired")
    return {"message": "OTP verified"}


@router.post("/password-reset-request")
async def password_reset_request(data: PasswordResetRequest, background_tasks: BackgroundTasks, userservice: UserService = Depends(UserService), otpservice: OTPService = Depends(OTPService)):
    """
    Route pour demander une réinitialisation de mot de passe.

    :param data: Données de la requête de réinitialisation de mot de passe
    :param background_tasks: Tâches en arrière-plan pour l'envoi d'email
    :param userservice: Service d'utilisateur pour gérer les opérations utilisateur
    :param otpservice: Service OTP pour gérer les OTP
    :return: Message de succès
    :raises HTTPException: Si l'email n'est pas enregistré
    """
    user = userservice.get_user_by_email(data.email)
    if not user:
        logfire.warn(
            f"Réinitialisation de mot de passe demandée pour un email non enregistré : {data.email}.")
        raise EmailNotRegisterException()

    otp, expiry_time = generate_otp()
    otpservice.store_otp(otp=otp, expiry_time=expiry_time, user_id=user.id)
    await send_otp_email(user.email, otp, background_tasks)

    logfire.info(f"OTP envoyé à l'email {user.email}.")
    return {"message": "OTP sent to email"}


@router.post("/password-reset")
def password_reset_confirm(data: PasswordResetConfirm, userservice: UserService = Depends(UserService)):
    """
    Route pour confirmer la réinitialisation de mot de passe avec l'OTP.

    :param data: Données de la requête de confirmation de réinitialisation de mot de passe
    :param otpservice: Service OTP pour gérer les OTP
    :param userservice: Service d'utilisateur pour gérer les opérations utilisateur
    :return: Message de succès
    :raises HTTPException: Si l'OTP est invalide ou expiré, ou si la réinitialisation échoue
    :raises UserNotFoundException: Si l'utilisateur n'est pas trouvé
    """
    db_user = userservice.get_user_by_email(data.email)
    if not db_user:
        logfire.warn(f"Utilisateur non trouvé pour l'email {data.email}.")
        raise UserNotFoundException()

    user = userservice.reset_password(data.email, data.new_password)
    if not user:
        logfire.error(
            f"Échec de la réinitialisation du mot de passe pour l'utilisateur avec email {data.email}.")
        raise PasswordResetFailedException()

    logfire.info(
        f"Réinitialisation de mot de passe réussie pour l'utilisateur avec email {data.email}.")
    return {"message": "Password reset successfully"}

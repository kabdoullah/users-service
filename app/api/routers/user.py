from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from app.dependencies.auth import get_current_active_user
from app.exceptions.custom_exception import EmailAlreadyUsedException, UserAlreadyExistsException, UserNotFoundException
from app.models.data.user import User
from app.models.requests.otp import OTPVerify
from app.models.requests.user import UserInDB, UserParticular, UserEnterprise, UserResponse, UserUpdate, UserCreate
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
async def register_professionel(user_data: UserEnterprise,  background_tasks: BackgroundTasks, userservice: UserService = Depends(UserService), otpservice: OTPService = Depends(OTPService)):
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
    otpservice.store_register_otp(
        otp=otp, expiry_time=expiry_time, email=email)
    await send_otp_email(email, otp, background_tasks)
    return {"message": "OTP sent successfully"}


@router.post("/verify-otp")
def verify_otp_route(data: OTPVerify, otpservice: OTPService = Depends(OTPService), userservice: UserService = Depends(UserService)):
    db_user = userservice.get_user_by_email(data.email)
    if not db_user:
        raise UserNotFoundException()
    if not otpservice.validate_otp(user_id=db_user.id, otp=data.otp_code):
        raise HTTPException(
            status_code=400, detail="Invalid OTP or OTP expired")
    return {"message": "OTP verified"}

# api pour verification d'otp utilisateur non connecté


@router.post("/verify-register-otp")
def verify_register_otp_route(data: OTPVerify, otpservice: OTPService = Depends(OTPService)):
    if not otpservice.validate_register_otp(email=data.email, otp=data.otp_code):
        raise HTTPException(
            status_code=400, detail="Invalid OTP or OTP expired")
    return {"message": "OTP verified"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

# Gestion des utilisateurs by Ablo


@router.get("/", response_model=List[UserInDB], status_code=status.HTTP_200_OK)
def get_all_users(service: UserService = Depends(UserService)):
    """
    Récupère tous les utilisateurs.

    **Réponse**:
    - **200 OK**: Liste des utilisateurs.
    """
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserInDB, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Récupère un utilisateur par son identifiant.

    **Paramètres**:
    - `user_id` (UUID): Identifiant de l'utilisateur.

    **Réponse**:
    - **200 OK**: Détails de l'utilisateur.
    - **404 Not Found**: Utilisateur non trouvé.
    """
    return service.get_user_by_id(user_id)


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(UserService)):
    """
    Crée un nouvel utilisateur.

    **Réponse**:
    - **201 Created**: Utilisateur créé avec succès.
    - **400 Bad Request**: Email déjà utilisé.
    """
    return service.create_user(user)


@router.put("/{user_id}", response_model=UserInDB, status_code=status.HTTP_200_OK)
def update_user(user_id: UUID, user: UserUpdate, service: UserService = Depends(UserService)):
    """
    Met à jour un utilisateur existant.

    **Paramètres**:
    - `user_id` (UUID): Identifiant de l'utilisateur.

    **Réponse**:
    - **200 OK**: Utilisateur mis à jour avec succès.
    - **404 Not Found**: Utilisateur non trouvé.
    """
    return service.update_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Supprime un utilisateur par son identifiant.

    **Paramètres**:
    - `user_id` (UUID): Identifiant de l'utilisateur.

    **Réponse**:
    - **200 OK**: Utilisateur supprimé avec succès.
    - **404 Not Found**: Utilisateur non trouvé.
    """
    is_deleted = service.delete_user(user_id)
    if is_deleted:
        return {"message": "Utilisateur supprimé avec succès"}


@router.put("/{user_id}/activate", response_model=UserInDB, status_code=status.HTTP_200_OK)
def activate_user(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Active un utilisateur par son identifiant.

    **Paramètres**:
    - `user_id` (UUID): Identifiant de l'utilisateur.

    **Réponse**:
    - **200 OK**: Utilisateur activé avec succès.
    - **404 Not Found**: Utilisateur non trouvé.
    """
    return service.activate_user(user_id)


@router.put("/{user_id}/deactivate", response_model=UserInDB, status_code=status.HTTP_200_OK)
def deactivate_user(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Désactive un utilisateur par son identifiant.

    **Paramètres**:
    - `user_id` (UUID): Identifiant de l'utilisateur.

    **Réponse**:
    - **200 OK**: Utilisateur désactivé avec succès.
    - **404 Not Found**: Utilisateur non trouvé.
    """
    return service.deactivate_user(user_id)

from typing import Dict, Optional
from fastapi import HTTPException

class InvalidCredentialsException(HTTPException):
    """
    Exception levée lorsqu'il y a une erreur d'authentification.
    """
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=400, detail="Incorrect email or password", headers=headers)

class UserNotFoundException(HTTPException):
    """
    Exception levée lorsque l'utilisateur n'est pas trouvé.
    """
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class InvalidPasswordException(HTTPException):
    """
    Exception levée lorsqu'un mot de passe est invalide.
    """
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid password")

class InvalidOTPException(HTTPException):
    """
    Exception levée lorsqu'un OTP (One-Time Password) est invalide.
    """
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid OTP")

class UserAlreadyExistsException(HTTPException):
    """
    Exception levée lorsque l'utilisateur existe déjà.
    """
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

class UserNotValidException(HTTPException):
    """
    Exception levée lorsque l'utilisateur est dans une liste d'attente.
    """
    def __init__(self):
        super().__init__(status_code=409, detail="User in pending list")

class EmptyInputException(HTTPException):
    """
    Exception levée lorsqu'une entrée est vide.
    """
    def __init__(self):
        super().__init__(status_code=400, detail="Input cannot be empty")

class CustomBadGatewayException(HTTPException):
    """
    Exception levée pour les erreurs de passerelle personnalisées.
    """
    def __init__(self, status_code: int = 502, detail: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class InvalidTokenException(HTTPException):
    """
    Exception levée lorsqu'un token est requis mais absent ou invalide.
    """
    def __init__(self):
        super().__init__(status_code=400, detail="Token needed")

class SameUsernamePasswordException(HTTPException):
    """
    Exception levée lorsque le nom d'utilisateur et le mot de passe sont identiques.
    """
    def __init__(self):
        super().__init__(status_code=400, detail="Username and password cannot be the same")

class InactiveUserException(HTTPException):
    """
    Exception levée lorsque l'utilisateur est inactif.
    """
    def __init__(self):
        super().__init__(status_code=400, detail="Inactive user")

class EmailAlreadyUsedException(HTTPException):
    """
    Exception levée lorsque l'email est déjà utilisé.
    """
    def __init__(self):
        super().__init__(status_code=409, detail="Email already used")

class PhoneAlreadyUsedException(HTTPException):
    """
    Exception levée lorsque le numéro de téléphone est déjà utilisé.
    """
    def __init__(self):
        super().__init__(status_code=409, detail="Phone number already used")
        
class SessionNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Session not found")

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")
        
class InvalidOTPException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid OTP")

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

from typing import Dict, Optional
from fastapi import HTTPException


class InvalidCredentialsException(HTTPException):
    """
    Exception levée lorsqu'il y a une erreur d'authentification.
    """

    def __init__(self, headers: Optional[Dict[str, str]] = None):
        super().__init__(status_code=400,
                         detail="Email ou mot de passe incorrect", headers=headers)


class UserNotFoundException(HTTPException):
    """
    Exception levée lorsque l'utilisateur n'est pas trouvé.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Utilisateur non trouvé")


class InvalidPasswordException(HTTPException):
    """
    Exception levée lorsqu'un mot de passe est invalide.
    """

    def __init__(self):
        super().__init__(status_code=401, detail="Login ou mot de passe invalide")


class InvalidOTPException(HTTPException):
    """
    Exception levée lorsqu'un OTP (One-Time Password) est invalide.
    """

    def __init__(self):
        super().__init__(status_code=401, detail="OTP invalide ou expiré")


class UserAlreadyExistsException(HTTPException):
    """
    Exception levée lorsque l'utilisateur existe déjà.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="L'utilisateur existe déjà")


class UserNotValidException(HTTPException):
    """
    Exception levée lorsque l'utilisateur est dans une liste d'attente.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="Utilisateur en attente de validation")


class EmptyInputException(HTTPException):
    """
    Exception levée lorsqu'une entrée est vide.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="L'entrée ne peut pas être vide")


class InvalidTokenException(HTTPException):
    """
    Exception levée lorsqu'un token est requis mais absent ou invalide.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Token requis")


class SameUsernamePasswordException(HTTPException):
    """
    Exception levée lorsque le nom d'utilisateur et le mot de passe sont identiques.
    """

    def __init__(self):
        super().__init__(status_code=400,
                         detail="Le nom d'utilisateur et le mot de passe ne peuvent pas être identiques")


class InactiveUserException(HTTPException):
    """
    Exception levée lorsque l'utilisateur est inactif.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Utilisateur inactif")


class EmailAlreadyUsedException(HTTPException):
    """
    Exception levée lorsque l'email est déjà utilisé.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="Email déjà utilisé")


class PhoneAlreadyUsedException(HTTPException):
    """
    Exception levée lorsque le numéro de téléphone est déjà utilisé.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="Numéro de téléphone déjà utilisé")


class SessionNotFoundException(HTTPException):
    """
    Exception levée lorsque la session n'est pas trouvée.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Session non trouvée")


class EmailNotRegisterException(HTTPException):
    """
    Exception levée lorsque l'email n'est pas enregistré.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Email non enregistré")


class PasswordResetFailedException(HTTPException):
    """
    Exception levée lorsque la réinitialisation du mot de passe échoue.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Échec de la réinitialisation du mot de passe")


# Exceptions pour Profile


class ProfileNotFoundException(HTTPException):
    """
    Exception levée lorsque le profil n'est pas trouvé.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Profil non trouvé")


class ProfileAlreadyExistsException(HTTPException):
    """
    Exception levée lorsque le profil existe déjà.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="Le profil existe déjà")


class InvalidProfileDataException(HTTPException):
    """
    Exception levée lorsque les données du profil sont invalides.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Données de profil invalides")

# Exceptions pour Right


class RightNotFoundException(HTTPException):
    """
    Exception levée lorsque le droit n'est pas trouvé.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Droit non trouvé")


class RightAlreadyExistsException(HTTPException):
    """
    Exception levée lorsque le droit existe déjà.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="Le droit existe déjà")


class InvalidRightDataException(HTTPException):
    """
    Exception levée lorsque les données du droit sont invalides.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Données de droit invalides")

# Exceptions pour Category


class CategoryNotFoundException(HTTPException):
    """
    Exception levée lorsque la catégorie n'est pas trouvée.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Catégorie non trouvée")


class CategoryAlreadyExistsException(HTTPException):
    """
    Exception levée lorsque la catégorie existe déjà.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="La catégorie existe déjà")


class InvalidCategoryDataException(HTTPException):
    """
    Exception levée lorsque les données de la catégorie sont invalides.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Données de catégorie invalides")

# Exceptions pour SubCategory


class SubCategoryNotFoundException(HTTPException):
    """
    Exception levée lorsque la sous-catégorie n'est pas trouvée.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Sous-catégorie non trouvée")


class SubCategoryAlreadyExistsException(HTTPException):
    """
    Exception levée lorsque la sous-catégorie existe déjà.
    """

    def __init__(self):
        super().__init__(status_code=409, detail="La sous-catégorie existe déjà")


class InvalidSubCategoryDataException(HTTPException):
    """
    Exception levée lorsque les données de la sous-catégorie sont invalides.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Données de sous-catégorie invalides")

from typing import Optional
from fastapi import Depends, HTTPException, status
from pydantic import UUID4
from app.configuration.config import AuthSettings
from app.repository.user_repository import UserRepository
from app.models.data.user import User
from app.models.requests.user import UserParticular, UserProfessional
from app.exceptions.custom_exception import UserNotFoundException, UserAlreadyExistsException
from app.security.security import hash_password, verify_password

auth_settings = AuthSettings()

MAX_ATTEMPTS = auth_settings.MAX_ATTEMPTS

class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    def create_particular(self, user_data: UserParticular) -> User:
        """
        Crée un nouvel utilisateur.
        
        :param user_data: Données de l'utilisateur
        :return: Utilisateur créé
        :raises UserAlreadyExistsException: Si un utilisateur avec le même email existe déjà
        """
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException()

        hashed_password = hash_password(user_data.password)
        user_data.password = hashed_password
        return self.user_repo.create_particular(user_data)
    
    def create_professional(self, user_data: UserProfessional) -> User:
        """
        Crée un nouvel utilisateur.
        
        :param user_data: Données de l'utilisateur
        :return: Utilisateur créé
        :raises UserAlreadyExistsException: Si un utilisateur avec le même email existe déjà
        """
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException()

        hashed_password = hash_password(user_data.password)
        user_data.password = hashed_password
        return self.user_repo.create_professional(user_data)

    def update_user(self, user_id: UUID4, user_data: UserParticular) -> User:
        """
        Met à jour un utilisateur existant.
        
        :param user_id: Identifiant de l'utilisateur
        :param user_data: Nouvelles données de l'utilisateur
        :return: Utilisateur mis à jour
        :raises UserNotFoundException: Si l'utilisateur n'est pas trouvé
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        for key, value in user_data.dict().items():
            setattr(user, key, value)

        self.user_repo.update_user(user)
        return user

    def delete_user(self, user_id: UUID4) -> bool:
        """
        Supprime un utilisateur.
        
        :param user_id: Identifiant de l'utilisateur
        :return: True si l'utilisateur a été supprimé, sinon False
        :raises UserNotFoundException: Si l'utilisateur n'est pas trouvé
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        self.user_repo.delete_user(user_id)
        return True

    def get_all_users(self):
        """
        Récupère tous les utilisateurs.
        
        :return: Liste des utilisateurs
        """
        return self.user_repo.get_all_users()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Récupère un utilisateur par son email.
        
        :param email: Email de l'utilisateur
        :return: Utilisateur trouvé ou None
        """
        return self.user_repo.get_user_by_email(email)

    def get_user_by_id(self, user_id: UUID4) -> Optional[User]:
        """
        Récupère un utilisateur par son identifiant.
        
        :param user_id: Identifiant de l'utilisateur
        :return: Utilisateur trouvé ou None
        :raises UserNotFoundException: Si l'utilisateur n'est pas trouvé
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user

    def reset_password(self, email: str, new_password: str) -> User:
        """
        Réinitialise le mot de passe d'un utilisateur.
        
        :param email: Email de l'utilisateur
        :param new_password: Nouveau mot de passe
        :return: Utilisateur avec le mot de passe réinitialisé
        :raises UserNotFoundException: Si l'utilisateur n'est pas trouvé
        """
        user = self.user_repo.reset_password(email, hash_password(new_password))
        if not user:
            raise UserNotFoundException()
        return user

    def update_password(self, user: User, new_password: str) -> User:
        """
        Met à jour le mot de passe d'un utilisateur.
        
        :param user: Objet utilisateur
        :param new_password: Nouveau mot de passe
        :return: Utilisateur avec le mot de passe mis à jour
        """
        hashed_password = hash_password(new_password)
        self.user_repo.update_password(user, hashed_password)
        return user

    def authenticate_user(self, email: str, password: str) -> dict:
        """
        Authentifie un utilisateur.
        
        :param email: Email de l'utilisateur
        :param password: Mot de passe de l'utilisateur
        :return: l'utilisateur authentifié et les tentatives restantes
        :raises HTTPException: Si les informations d'authentification sont incorrectes ou si le compte est verrouillé
        """
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
        
        if user.login_attempts >= MAX_ATTEMPTS:
            user.login_attempts = 0
            self.user_repo.db.commit()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account locked. Please contact support.")
        
        if not verify_password(password, user.password):
            user.login_attempts += 1
            self.user_repo.db.commit()
            attempts_left = MAX_ATTEMPTS - user.login_attempts
            if attempts_left <= 0:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account locked. Please contact support.")
            return {"message": "Invalid login or password", "attempts_left": attempts_left}

        user.login_attempts = 0
        self.user_repo.db.commit()
        return {"user": user, "attempts_left": MAX_ATTEMPTS}
    
    

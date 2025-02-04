from typing import Optional
from fastapi import Depends, HTTPException, status
import logfire
from uuid import UUID
from app.configuration.config import AuthSettings
from app.repository.user_repository import UserRepository
from app.models.data.user import User
from app.models.requests.user import UserCreate, UserParticular, UserEnterprise, UserUpdate
from app.exceptions.custom_exception import InvalidCredentialsException, UserNotFoundException, UserAlreadyExistsException
from app.security.security import hash_password, verify_password

auth_settings = AuthSettings()

MAX_ATTEMPTS = auth_settings.MAX_ATTEMPTS


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self.user_repo = user_repo

    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException()

        hashed_password = hash_password(user_data.password)
        user_data.password = hashed_password
        return self.user_repo.create_user(user_data)

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
        return self.user_repo.create_user(user_data)

    def create_professional(self, user_data: UserEnterprise) -> User:
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

    def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        """
        Met à jour un utilisateur existant.

        :param user_id: Identifiant de l'utilisateur
        :param user_data: Nouvelles données de l'utilisateur
        :return: Utilisateur mis à jour
        :raises UserNotFoundException: Si l'utilisateur n'est pas trouvé
        """
        if user_data.password:
            hashed_password = hash_password(user_data.password)
            user_data.password = hashed_password

        user_updated = self.user_repo.update_user(user_id, user_data)
        if not user_updated:
            raise UserNotFoundException()
        return user_updated

    def delete_user(self, user_id: UUID) -> bool:
        """
        Supprime un utilisateur.

        :param user_id: Identifiant de l'utilisateur
        :return: True si l'utilisateur a été supprimé, sinon False
        :raises UserNotFoundException: Si l'utilisateur n'est pas trouvé
        """

        user = self.user_repo.delete_user(user_id)
        if not user:
            logfire.warn(f"Utilisateur non trouvé : {user_id}")
            raise UserNotFoundException()
        return user

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

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
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
        try:
            user = self.user_repo.reset_password(
                email, hash_password(new_password))
            if not user:
                raise UserNotFoundException()
            user.is_active = True
            self.user_repo.reset_login_attempts(user)
            return user
        except Exception as e:
            logfire.error(
                f"Erreur lors de la réinitialisation du mot de passe pour l'utilisateur avec email {email}: {str(e)}")
            raise

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

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Authentifie un utilisateur en vérifiant son email et son mot de passe.

        :param email: Email de l'utilisateur
        :param password: Mot de passe de l'utilisateur
        :return: L'utilisateur authentifié
        :raises HTTPException: Si les informations d'authentification sont incorrectes ou si le compte est verrouillé
        """
        try:
            user = self.user_repo.get_user_by_email(email)
            if not user:
                logfire.warn(
                    f"Échec de la connexion : utilisateur avec email {email} non trouvé.")
                raise InvalidCredentialsException()

            if user.login_attempts >= MAX_ATTEMPTS:
                logfire.warn(
                    f"Compte verrouillé pour l'utilisateur avec email {email}.")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Veuillez modifier votre mot de passe")

            if not verify_password(password, user.password):
                self.user_repo.increment_login_attempts(user)
                attempts_left = MAX_ATTEMPTS - user.login_attempts
                if attempts_left <= 0:
                    user.is_active = False
                    logfire.warn(
                        f"Trop de tentatives échouées pour l'utilisateur avec email {email}. Compte verrouillé.")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="Veuillez modifier votre mot de passe.")
                logfire.warn(
                    f"Échec de la connexion : mot de passe incorrect pour l'utilisateur avec email {email}.")
                raise InvalidCredentialsException()

            self.user_repo.reset_login_attempts(user)
            logfire.info(
                f"Connexion réussie pour l'utilisateur avec email {email}.")
            return user
        except Exception as e:
            logfire.error(
                f"Erreur lors de l'authentification pour l'utilisateur avec email {email}: {str(e)}")
            raise

    def deactivate_user(self, user_id: UUID) -> User:
        user = self.user_repo.deactivate_user(user_id)
        if not user:
            logfire.warn(f"Utilisateur non trouvé : {user_id}")
            raise UserNotFoundException()
        return user

    def activate_user(self, user_id: UUID) -> User:
        user = self.user_repo.activate_user(user_id)
        if not user:
            logfire.warn(f"Utilisateur non trouvé : {user_id}")
            raise UserNotFoundException()
        return user

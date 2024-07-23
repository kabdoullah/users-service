from typing import List
from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from app.models.requests.session import SessionCreate
from app.models.data.session import Session as SessionModel
from app.repository.session_repository import SessionRepository
from app.exceptions.custom_exception import (
    SessionNotFoundException,
    UserNotFoundException,
)
from app.repository.user_repository import UserRepository

class SessionService:
    def __init__(self, session_repo: SessionRepository = Depends(SessionRepository), user_repo: UserRepository = Depends(UserRepository)):
        """
        Initialise le service avec les repositories de session et utilisateur.
        
        :param session_repo: Repository de session
        :param user_repo: Repository d'utilisateur
        """
        self.session_repo = session_repo
        self.user_repo = user_repo

    def create_session(self, session_data: SessionCreate) -> SessionModel:
        """
        Crée une nouvelle session pour un utilisateur.
        
        :param session_data: Données de la session à créer
        :return: La session créée
        """
        user = self.user_repo.get_user_by_id(session_data.user_id)
        if not user:
            raise UserNotFoundException()
        
        return self.session_repo.create_session(session_data)

    def get_session(self, session_id: UUID) -> SessionModel:
        """
        Récupère une session par son identifiant.
        
        :param session_id: Identifiant de la session
        :return: La session trouvée
        """
        session = self.session_repo.get_session(session_id)
        if not session:
            raise SessionNotFoundException()
        
        return session

    def delete_session(self, session_id: UUID) -> bool:
        """
        Supprime une session par son identifiant.
        
        :param session_id: Identifiant de la session
        :return: True si la session est supprimée, sinon False
        """
        session = self.session_repo.get_session(session_id)
        if not session:
            raise SessionNotFoundException()
        
        return self.session_repo.delete_session(session_id)

    def get_sessions_by_user(self, user_id: UUID) -> List[SessionModel]:
        """
        Récupère toutes les sessions pour un utilisateur donné.
        
        :param user_id: Identifiant de l'utilisateur
        :return: Liste des sessions de l'utilisateur
        """
        return self.session_repo.get_sessions_by_user(user_id)

    def validate_token(self, user_id: UUID, token: str) -> bool:
        """
        Valide le token de l'utilisateur.
        
        :param user_id: Identifiant de l'utilisateur
        :param token: Token à valider
        :return: True si le token est valide, sinon False
        """
        sessions = self.session_repo.get_sessions_by_user(user_id)
        for session in sessions:
            if session.token == token and session.expired_at > datetime.now(timezone.utc):
                return True
        return False



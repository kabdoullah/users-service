from typing import List
from sqlalchemy.orm import Session as SQLAlchemySession
from fastapi import Depends
from uuid import UUID
import logfire
from app.models.data.session import Session as SessionModel
from app.models.requests.session import SessionCreate
from app.configuration.database import get_db


class SessionRepository:
    def __init__(self, db: SQLAlchemySession = Depends(get_db)):
        self.db = db

    def create_session(self, session: SessionCreate) -> SessionModel:
        db_session = SessionModel(session.model_dump())
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        logfire.info(f"Session créée avec succès : {db_session.id}")
        return db_session

    def get_session(self, session_id: UUID) -> SessionModel | None:
        db_session = self.db.query(SessionModel).filter(
            SessionModel.id == session_id).first()
        if not db_session:
            logfire.warn(f"Session non trouvée avec l'ID : {session_id}")
        return db_session

    def delete_session(self, session_id: UUID) -> bool:
        db_session = self.get_session(session_id)
        if db_session:
            self.db.delete(db_session)
            self.db.commit()
            logfire.info(f"Session supprimée avec succès : {session_id}")
            return True
        logfire.warn(f"Échec de la suppression de la session : {session_id}")
        return False

    def get_sessions_by_user(self, user_id: UUID) -> List[SessionModel]:
        sessions = self.db.query(SessionModel).filter(
            SessionModel.user_id == user_id).all()
        logfire.info(
            f"{len(sessions)} sessions récupérées pour l'utilisateur : {user_id}")
        return sessions

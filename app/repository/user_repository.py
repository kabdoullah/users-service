from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends
import logfire
from app.configuration.database import get_db
from app.models.data.user import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logfire.info(f"Utilisateur créé avec succès : {user.email}")
        return user

    def update_user(self, user: User) -> User:
        self.db.commit()
        logfire.info(f"Utilisateur mis à jour : {user.email}")
        return user

    def delete_user(self, user_id: UUID) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            logfire.warn(f"Utilisateur non trouvé : {user_id}")
            return False
        self.db.delete(user)
        self.db.commit()
        logfire.info(f"Utilisateur supprimé : {user.email}")
        return True

    def get_user_by_id(self, user_id: UUID) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            logfire.warn(f"Utilisateur non trouvé : {user_id}")
        return user

    def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        users = self.db.query(User).offset(skip).limit(limit).all()
        logfire.info(f"{len(users)} utilisateurs récupérés")
        return users

    def get_user_by_email(self, email: str) -> User | None:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            logfire.warn(f"Utilisateur non trouvé avec l'email : {email}")
        return user

    def reset_password(self, email: str, new_password: str) -> User | None:
        user = self.get_user_by_email(email)
        if not user:
            logfire.warn(
                f"Impossible de réinitialiser le mot de passe, utilisateur non trouvé : {email}")
            return None
        user.password = new_password
        self.db.commit()
        logfire.info(f"Mot de passe réinitialisé pour l'utilisateur : {email}")
        return user

    def update_password(self, user: User, new_password: str) -> User:
        user.password = new_password
        self.db.commit()
        logfire.info(
            f"Mot de passe mis à jour pour l'utilisateur : {user.email}")
        return user

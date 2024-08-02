from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends
import logfire
from app.configuration.database import get_db
from app.models.data.right import Right
from app.models.requests.right import RightCreate, RightUpdate


class RightRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_right(self, right: RightCreate) -> Right:
        db_right = Right(**right.model_dump())
        self.db.add(db_right)
        self.db.commit()
        self.db.refresh(db_right)
        logfire.info(f"Droit créé avec succès : {db_right.name}")
        return db_right

    def update_right(self, right_id: UUID, right: RightUpdate) -> Right | None:
        db_right = self.get_right_by_id(right_id)
        if not db_right:
            logfire.warn(f"Droit non trouvé : {right_id}")
            return None
        db_right.name = right.name
        self.db.commit()
        logfire.info(f"Droit mis à jour : {db_right.id}")
        return db_right

    def delete_right(self, right_id: UUID) -> bool:
        right = self.get_right_by_id(right_id)
        if not right:
            logfire.warn(f"Droit non trouvé : {right_id}")
            return False
        self.db.delete(right)
        self.db.commit()
        logfire.info(f"Droit supprimé : {right.id}")
        return True

    def get_right_by_id(self, right_id: UUID) -> Right | None:
        right = self.db.query(Right).filter(Right.id == right_id).first()
        if not right:
            logfire.warn(f"Droit non trouvé : {right_id}")
            return None
        return right

    def get_all_rights(self, skip: int = 0, limit: int = 10) -> List[Right]:
        rights = self.db.query(Right).offset(skip).limit(limit).all()
        logfire.info(f"{len(rights)} droits récupérés")
        return rights
    
    def get_right_by_name(self, name: str) -> Right | None:
        right = self.db.query(Right).filter(Right.name == name).first()
        if not right:
            logfire.warn(f"Droit non trouvé avec le nom : {name}")
            return None
        return right

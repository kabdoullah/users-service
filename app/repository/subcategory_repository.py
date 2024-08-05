from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
import logfire
from app.configuration.database import get_db
from app.models.data.category import SubCategory
from app.models.requests.category import SubCategoryCreate, SubCategoryUpdate


class SubCategoryRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_subcategories(self) -> list[SubCategory]:
        subcategories = self.db.query(SubCategory).all()
        logfire.info(f"{len(subcategories)} sous-catégories récupérées")
        return subcategories

    def get_subcategory_by_name(self, name: str) -> SubCategory | None:
        subcategory = self.db.query(SubCategory).filter(
            SubCategory.name == name).first()
        if not subcategory:
            logfire.warn(f"Sous-catégorie non trouvée avec le nom : {name}")
            return None
        return subcategory

    def get_subcategory_by_id(self, subcategory_id: UUID) -> SubCategory:
        subcategory = self.db.query(SubCategory).filter(
            SubCategory.id == subcategory_id).first()
        if not subcategory:
            logfire.warn(
                f"Sous-catégorie non trouvée avec l'ID : {subcategory_id}")
        return subcategory

    def create_subcategory(self, subcategory: SubCategoryCreate) -> SubCategory:
        db_subcategory = SubCategory(**subcategory.model_dump())
        self.db.add(db_subcategory)
        self.db.commit()
        self.db.refresh(db_subcategory)
        logfire.info(
            f"Sous-catégorie créée avec succès : {db_subcategory.name}")
        return db_subcategory

    def update_subcategory(self, subcategory_id: UUID, subcategory: SubCategoryUpdate) -> SubCategory:
        db_subcategory = self.get_subcategory_by_id(subcategory_id)
        if not db_subcategory:
            logfire.warn(
                f"Sous-catégorie non trouvée avec l'ID : {subcategory_id}")
            return None
        db_subcategory.name = subcategory.name
        self.db.commit()
        logfire.info(f"Sous-catégorie mise à jour : {db_subcategory.id}")
        return db_subcategory

    def delete_subcategory(self, subcategory_id: UUID) -> bool:
        subcategory = self.get_subcategory_by_id(subcategory_id)
        if not subcategory:
            logfire.warn(f"Sous-catégorie non trouvée avec l'ID : {subcategory_id}")
            return False
        self.db.delete(subcategory)
        self.db.commit()
        logfire.info(f"Sous-catégorie supprimée avec succès : {subcategory.id}")
        return True

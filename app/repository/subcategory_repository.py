from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
import logfire
from app.configuration.database import get_db
from app.models.data.category import SubCategory


class SubCategoryRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        
    def get_all_subcategories(self) -> list[SubCategory]:
        subcategories = self.db.query(SubCategory).all()
        logfire.info(f"{len(subcategories)} sous-catégories récupérées")
        return subcategories

    def get_subcategory_by_name(self, name: str) -> SubCategory:
        subcategory = self.db.query(SubCategory).filter(
            SubCategory.name == name).first()
        if not subcategory:
            logfire.warn(f"Sous-catégorie non trouvée avec le nom : {name}")
        return subcategory

    def get_subcategory_by_id(self, subcategory_id: UUID) -> SubCategory:
        subcategory = self.db.query(SubCategory).filter(
            SubCategory.id == subcategory_id).first()
        if not subcategory:
            logfire.warn(
                f"Sous-catégorie non trouvée avec l'ID : {subcategory_id}")
        return subcategory

    def create_subcategory(self, subcategory: SubCategory) -> SubCategory:
        self.db.add(subcategory)
        self.db.commit()
        self.db.refresh(subcategory)
        logfire.info(f"Sous-catégorie créée avec succès : {subcategory.name}")
        return subcategory

    def update_subcategory(self, subcategory: SubCategory) -> SubCategory:
        self.db.commit()
        logfire.info(f"Sous-catégorie mise à jour : {subcategory.id}")
        return subcategory

    def delete_subcategory(self, subcategory_id: UUID) -> bool:
        subcategory = self.get_subcategory_by_id(subcategory_id)
        if not subcategory:
            logfire.warn(
                f"Sous-catégorie non trouvée avec l'ID : {subcategory_id}")
            return False
        self.db.delete(subcategory)
        self.db.commit()
        logfire.info(
            f"Sous-catégorie supprimée avec succès : {subcategory.id}")
        return True

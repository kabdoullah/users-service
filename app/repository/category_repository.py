from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
import logfire
from app.configuration.database import get_db
from app.models.data.category import Category
from app.models.requests.category import CategoryCreate


class CategoryRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self):
        categories = self.db.query(Category).all()
        logfire.info(f"{len(categories)} catégories récupérées")
        return categories

    def get_by_id(self, id: UUID):
        category = self.db.query(Category).filter(Category.id == id).first()
        if not category:
            logfire.warn(f"Catégorie non trouvée avec l'ID : {id}")
        return category

    def get_by_name(self, name: str):
        category = self.db.query(Category).filter(
            Category.name == name).first()
        if not category:
            logfire.warn(f"Catégorie non trouvée avec le nom : {name}")
        return category

    def create(self, category: CategoryCreate):
        db_category = Category(**category.model_dump())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        logfire.info(f"Catégorie créée avec succès : {db_category.name}")
        return db_category

    def update(self, category_id: UUID, category: CategoryCreate):
        db_category = self.get_by_id(category_id)
        if not db_category:
            logfire.warn(f"Catégorie non trouvée avec l'ID : {category.id}")
            return None
        db_category.name = category.name
        self.db.commit()
        logfire.info(f"Catégorie mise à jour avec succès : {db_category.id}")
        return db_category

    def delete(self, category_id: UUID) -> bool:
        db_category = self.get_by_id(category_id)
        if not db_category:
            logfire.warn(f"Catégorie non trouvée avec l'ID : {category_id}")
            return False
        self.db.delete(db_category)
        self.db.commit()
        logfire.info(f"Catégorie supprimée avec succès : {db_category.id}")
        return True

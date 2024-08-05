from typing import Optional
from fastapi import Depends
import logfire
from uuid import UUID
from app.repository.category_repository import CategoryRepository
from app.models.data.category import Category
from app.models.requests.category import CategoryCreate, CategoryUpdate
from app.exceptions.custom_exception import (
    CategoryNotFoundException, CategoryAlreadyExistsException, InvalidCategoryDataException
)


class CategoryService:
    def __init__(self, category_repo: CategoryRepository = Depends(CategoryRepository)):
        self.category_repo = category_repo

    def create_category(self, category_data: CategoryCreate) -> Category:
        """
        Crée une nouvelle catégorie.
        """
        existing_category = self.category_repo.get_by_name(category_data.name)
        if existing_category:
            logfire.warn(f"Catégorie déjà existante : {category_data.name}")
            raise CategoryAlreadyExistsException()

        try:
            category = self.category_repo.create(category_data)
            logfire.info(f"Catégorie créée avec succès : {category.name}")
            return category
        except Exception as e:
            logfire.error(
                f"Erreur lors de la création de la catégorie : {str(e)}")
            raise InvalidCategoryDataException()

    def update_category(self, category_id: UUID, category_data: CategoryUpdate) -> Category:
        """
        Met à jour une catégorie existante.
        """
        try:
            category = self.category_repo.update(category_id, category_data)
            if not category:
                logfire.warn(f"Catégorie non trouvée : {category_id}")
                raise CategoryNotFoundException()
            logfire.info(f"Catégorie mise à jour : {category.id}")
            return category
        except Exception as e:
            logfire.error(
                f"Erreur lors de la mise à jour de la catégorie : {str(e)}")
            raise InvalidCategoryDataException()

    def delete_category(self, category_id: UUID) -> bool:
        """
        Supprime une catégorie.
        """

        category = self.category_repo.delete(category_id)
        if not category:
            logfire.warn(f"Catégorie non trouvée : {category_id}")
            return False
        logfire.info(f"Catégorie supprimée : {category_id}")
        return category

    def get_category_by_id(self, category_id: UUID) -> Optional[Category]:
        """
        Récupère une catégorie par son identifiant.
        """
        category = self.category_repo.get_by_id(category_id)
        if not category:
            logfire.warn(f"Catégorie non trouvée : {category_id}")
            raise CategoryNotFoundException()
        return category

    def get_all_categories(self):
        """
        Récupère toutes les catégories.
        """
        return self.category_repo.get_all()

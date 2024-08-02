from typing import Optional
from fastapi import Depends
import logfire
from uuid import UUID
from app.repository.subcategory_repository import SubCategoryRepository
from app.models.data.category import SubCategory
from app.models.requests.category import SubCategoryCreate, SubCategoryUpdate
from app.exceptions.custom_exception import (
    SubCategoryNotFoundException, SubCategoryAlreadyExistsException, InvalidSubCategoryDataException
)


class SubCategoryService:
    def __init__(self, subcategory_repo: SubCategoryRepository = Depends(SubCategoryRepository)):
        self.subcategory_repo = subcategory_repo

    def create_subcategory(self, subcategory_data: SubCategoryCreate) -> SubCategory:
        """
        Crée une nouvelle sous-catégorie.
        """
        existing_subcategory = self.subcategory_repo.get_subcategory_by_name(
            subcategory_data.name)
        if existing_subcategory:
            logfire.warn(
                f"Sous-catégorie déjà existante : {subcategory_data.name}")
            raise SubCategoryAlreadyExistsException()

        try:
            subcategory = self.subcategory_repo.create_subcategory(
                subcategory_data)
            logfire.info(
                f"Sous-catégorie créée avec succès : {subcategory.name}")
            return subcategory
        except Exception as e:
            logfire.error(
                f"Erreur lors de la création de la sous-catégorie : {str(e)}")
            raise InvalidSubCategoryDataException()

    def update_subcategory(self, subcategory_id: UUID, subcategory_data: SubCategoryUpdate) -> SubCategory:
        """
        Met à jour une sous-catégorie existante.
        """
        subcategory = self.subcategory_repo.get_subcategory_by_id(
            subcategory_id)
        if not subcategory:
            logfire.warn(f"Sous-catégorie non trouvée : {subcategory_id}")
            raise SubCategoryNotFoundException()

        for key, value in subcategory_data.dict(exclude_unset=True).items():
            setattr(subcategory, key, value)

        try:
            self.subcategory_repo.update_subcategory(subcategory)
            logfire.info(f"Sous-catégorie mise à jour : {subcategory_id}")
            return subcategory
        except Exception as e:
            logfire.error(
                f"Erreur lors de la mise à jour de la sous-catégorie : {str(e)}")
            raise InvalidSubCategoryDataException()

    def delete_subcategory(self, subcategory_id: UUID) -> bool:
        """
        Supprime une sous-catégorie.
        """
        subcategory = self.subcategory_repo.get_subcategory_by_id(
            subcategory_id)
        if not subcategory:
            logfire.warn(f"Sous-catégorie non trouvée : {subcategory_id}")
            raise SubCategoryNotFoundException()

        self.subcategory_repo.delete_subcategory(subcategory_id)
        logfire.info(f"Sous-catégorie supprimée : {subcategory_id}")
        return True

    def get_subcategory_by_id(self, subcategory_id: UUID) -> Optional[SubCategory]:
        """
        Récupère une sous-catégorie par son identifiant.
        """
        subcategory = self.subcategory_repo.get_subcategory_by_id(
            subcategory_id)
        if not subcategory:
            logfire.warn(f"Sous-catégorie non trouvée : {subcategory_id}")
            raise SubCategoryNotFoundException()
        return subcategory

    def get_all_subcategories(self):
        """
        Récupère toutes les sous-catégories.
        """
        return self.subcategory_repo.get_all_subcategories()

from typing import Optional
from fastapi import Depends
import logfire
from uuid import UUID
from app.repository.right_repository import RightRepository
from app.models.data.right import Right
from app.models.requests.right import RightCreate, RightUpdate
from app.exceptions.custom_exception import (
    RightNotFoundException, RightAlreadyExistsException, InvalidRightDataException
)


class RightService:
    def __init__(self, right_repo: RightRepository = Depends(RightRepository)):
        self.right_repo = right_repo

    def create_right(self, right_data: RightCreate) -> Right:
        """
        Crée un nouveau droit.
        """
        existing_right = self.right_repo.get_right_by_name(right_data.name)
        if existing_right:
            logfire.warn(f"Droit déjà existant : {right_data.name}")
            raise RightAlreadyExistsException()

        try:
            right = self.right_repo.create_right(right_data)
            logfire.info(f"Droit créé avec succès : {right.name}")
            return right
        except Exception as e:
            logfire.error(f"Erreur lors de la création du droit : {str(e)}")
            raise InvalidRightDataException()

    def update_right(self, right_id: UUID, right_data: RightUpdate) -> Right:
        """
        Met à jour un droit existant.
        """
        try:
            right = self.right_repo.update_right(right_id, right_data)
            if not right:
                logfire.warn(f"Droit non trouvé : {right_id}")
                raise RightNotFoundException()
            logfire.info(f"Droit mis à jour : {right.id}")
            return right
        except Exception as e:
            logfire.error(f"Erreur lors de la mise à jour du droit : {str(e)}")
            raise InvalidRightDataException()

    def delete_right(self, right_id: UUID) -> bool:
        """
        Supprime un droit.
        """

        is_deleted = self.right_repo.delete_right(right_id)
        if not is_deleted:
            logfire.warn(f"Droit non trouvé : {right_id}")
            raise RightNotFoundException()

        logfire.info(f"Droit supprimé : {right_id}")
        return is_deleted

    def get_right_by_id(self, right_id: UUID) -> Optional[Right]:
        """
        Récupère un droit par son identifiant.
        """
        right = self.right_repo.get_right_by_id(right_id)
        if not right:
            logfire.warn(f"Droit non trouvé : {right_id}")
            raise RightNotFoundException()
        return right

    def get_all_rights(self):
        """
        Récupère tous les droits.
        """
        return self.right_repo.get_all_rights()

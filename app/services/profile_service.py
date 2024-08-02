from typing import Optional
from fastapi import Depends
import logfire
from uuid import UUID
from app.repository.profile_repository import ProfileRepository
from app.models.data.profile import Profile
from app.models.requests.profile import ProfileCreate, ProfileUpdate
from app.exceptions.custom_exception import (
    ProfileNotFoundException, ProfileAlreadyExistsException, InvalidProfileDataException
)


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository = Depends(ProfileRepository)):
        self.profile_repo = profile_repo

    def create_profile(self, profile_data: ProfileCreate) -> Profile:
        """
        Crée un nouveau profil.
        """
        existing_profile = self.profile_repo.get_profile_by_name(
            profile_data.name)
        if existing_profile:
            logfire.warn(f"Profil déjà existant : {profile_data.name}")
            raise ProfileAlreadyExistsException()

        try:
            profile = self.profile_repo.create_profile(profile_data)
            logfire.info(f"Profil créé avec succès : {profile.name}")
            return profile
        except Exception as e:
            logfire.error(f"Erreur lors de la création du profil : {str(e)}")
            raise InvalidProfileDataException()

    def update_profile(self, profile_id: UUID, profile_data: ProfileUpdate) -> Profile:
        """
        Met à jour un profil existant.
        """

        try:
            profile_updated = self.profile_repo.update_profile(
                profile=profile_data, profile_id=profile_id)
            if not profile_updated:
                logfire.warn(f"Profil non trouvé : {profile_id}")
                raise ProfileNotFoundException()
            logfire.info(f"Profil mis à jour : {profile_id}")
            return profile_updated
        except Exception as e:
            logfire.error(
                f"Erreur lors de la mise à jour du profil : {str(e)}")
            raise InvalidProfileDataException()

    def delete_profile(self, profile_id: UUID) -> bool:
        """
        Supprime un profil.
        """

        is_deleted = self.profile_repo.delete_profile(profile_id)
        if not is_deleted:
            logfire.warn(f"Profil non trouvé : {profile_id}")
            raise ProfileNotFoundException()
        logfire.info(f"Profil supprimé : {profile_id}")
        return is_deleted

    def get_profile_by_id(self, profile_id: UUID) -> Optional[Profile]:
        """
        Récupère un profil par son identifiant.
        """
        profile = self.profile_repo.get_profile_by_id(profile_id)
        if not profile:
            logfire.warn(f"Profil non trouvé : {profile_id}")
            raise ProfileNotFoundException()
        return profile

    def get_all_profiles(self):
        """
        Récupère tous les profils.
        """
        return self.profile_repo.get_all_profiles()

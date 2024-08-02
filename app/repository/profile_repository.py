from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends
import logfire
from app.configuration.database import get_db
from app.models.data.profile import Profile
from app.models.requests.profile import ProfileCreate, ProfileUpdate


class ProfileRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_profile(self, profile: ProfileCreate) -> Profile:
        db_profile = Profile(**profile.model_dump())
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        logfire.info(f"Profil créé avec succès : {db_profile.name}")
        return db_profile

    def update_profile(self, profile_id: UUID, profile: ProfileUpdate) -> Profile:
        db_profile = self.get_profile_by_id(profile_id)
        if not db_profile:
            logfire.warn(f"Profil non trouvé : {profile_id}")
            return None
        db_profile.name = profile.name
        self.db.commit()
        logfire.info(f"Profil mis à jour : {profile_id}")
        return db_profile

    def delete_profile(self, profile_id: UUID) -> bool:
        profile = self.get_profile_by_id(profile_id)
        if not profile:
            logfire.warn(f"Profil non trouvé : {profile_id}")
            return False
        self.db.delete(profile)
        self.db.commit()
        logfire.info(f"Profil supprimé : {profile_id}")
        return True

    def get_profile_by_id(self, profile_id: UUID) -> Profile | None:
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            logfire.warn(f"Profil non trouvé : {profile_id}")
        return profile

    def get_all_profiles(self) -> List[Profile]:
        profiles = self.db.query(Profile).all()
        logfire.info(f"{len(profiles)} profils récupérés")
        return profiles

    def get_profile_by_name(self, name: str) -> Profile | None:
        profile = self.db.query(Profile).filter(Profile.name == name).first()
        if not profile:
            logfire.warn(f"Profil non trouvé avec le nom : {name}")
            return None
        return profile
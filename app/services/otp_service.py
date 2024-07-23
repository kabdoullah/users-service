from datetime import timedelta
from uuid import UUID
from fastapi import Depends
from app.repository.otp_repository import OTPRepository
from app.exceptions.custom_exception import InvalidOTPException, UserNotFoundException
from app.repository.user_repository import UserRepository

class OTPService:
    def __init__(self, otp_repo: OTPRepository = Depends(OTPRepository), user_repo: UserRepository = Depends(UserRepository)):
        """
        Initialise le service avec les repositories OTP et utilisateur.

        :param otp_repo: Repository OTP
        :param user_repo: Repository d'utilisateur
        """
        self.otp_repo = otp_repo
        self.user_repo = user_repo

    def generate_and_store_otp(self, user_id: UUID, otp: str, expiry_time: timedelta):
        """
        Génère et stocke un OTP pour un utilisateur spécifique.

        :param user_id: Identifiant unique de l'utilisateur
        :param otp: Le code OTP à stocker
        :param expiry_time: La durée après laquelle l'OTP expirera
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        
        self.otp_repo.store_otp(user_id, otp, expiry_time)

    def validate_otp(self, user_id: UUID, otp: str) -> bool:
        """
        Valide un OTP pour un utilisateur spécifique.

        :param user_id: Identifiant unique de l'utilisateur
        :param otp: Le code OTP à vérifier
        :return: True si l'OTP est valide, sinon False
        :raises InvalidOTPException: Si l'OTP est invalide
        """
        if not self.otp_repo.verify_otp(user_id, otp):
            raise InvalidOTPException()
        return True


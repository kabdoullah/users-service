from datetime import datetime, timedelta
from uuid import UUID
from fastapi import Depends
from redis import Redis
from app.configuration.database import get_redis

class OTPRepository:
    def __init__(self, redis: Redis = Depends(get_redis)) -> None:
        """
        Initialise l'OTPRepository avec une instance de client Redis.
        La dépendance est injectée automatiquement par FastAPI.
        
        :param redis: Instance de client Redis.
        """
        self.redis = redis

    def store_otp(self, user_id: UUID, otp: str, expiry_time: datetime):
        """
        Stocke un OTP (One Time Password) pour un utilisateur spécifique dans Redis avec un temps d'expiration.

        :param user_id: L'identifiant unique de l'utilisateur.
        :param otp: Le code OTP à stocker.
        :param expiry_time: La durée après laquelle l'OTP expirera.
        """
        current_time = int(expiry_time.timestamp())
        self.redis.setex(str(user_id), current_time, otp)

    def verify_otp(self, user_id: UUID, otp: str) -> bool:
        """
        Vérifie si un OTP fourni correspond à celui stocké pour un utilisateur spécifique.
        Si l'OTP est correct, il est supprimé de Redis.

        :param user_id: L'identifiant unique de l'utilisateur.
        :param otp: Le code OTP à vérifier.
        :return: True si l'OTP est correct, sinon False.
        """
        stored_otp = self.redis.get(str(user_id))
        if stored_otp and stored_otp.decode('utf-8') == otp:
            self.redis.delete(str(user_id))
            return True
        return False

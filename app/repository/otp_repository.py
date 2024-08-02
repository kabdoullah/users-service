from datetime import datetime
from uuid import UUID
from fastapi import Depends
from redis import Redis
import logfire
from app.configuration.database import get_redis


class OTPRepository:
    def __init__(self, redis: Redis = Depends(get_redis)) -> None:
        self.redis = redis

    def store_otp(self, user_id: UUID, otp: str, expiry_time: datetime) -> None:
        current_time = int(expiry_time.timestamp())
        self.redis.setex(str(user_id), current_time, otp)
        logfire.info(f"OTP stocké pour l'utilisateur : {user_id}")

    def store_register_otp(self, email: str, otp: str, expiry_time: datetime):
        current_time = int(expiry_time.timestamp())
        self.redis.setex(email, current_time, otp)
        logfire.info(f"OTP de registre stocké pour l'email : {email}")

    def verify_otp(self, user_id: UUID, otp: str) -> bool:
        stored_otp = self.redis.get(str(user_id))
        if stored_otp and stored_otp.decode('utf-8') == otp:
            self.redis.delete(str(user_id))
            logfire.info(
                f"OTP vérifié et supprimé pour l'utilisateur : {user_id}")
            return True
        logfire.warn(
            f"Échec de la vérification de l'OTP pour l'utilisateur : {user_id}")
        return False

    def verify_register_otp(self, email: str, otp: str) -> bool:
        stored_otp = self.redis.get(email)
        if stored_otp and stored_otp.decode('utf-8') == otp:
            self.redis.delete(email)
            logfire.info(f"OTP vérifié et supprimé pour l'email : {email}")
            return True
        logfire.warn(
            f"Échec de la vérification de l'OTP pour l'email : {email}")
        return False

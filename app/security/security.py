import random
import string
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import UUID4
from app.configuration.config import AuthSettings
from app.models.requests.session import SessionData
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.exceptions.custom_exception import InvalidTokenException


auth_settings = AuthSettings()


ALGORITHM = "HS256"
SECRET_KEY = auth_settings.SECRET_KEY
REFRESH_TOKEN_EXPIRE_MINUTES = auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str) -> SessionData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID4 = payload.get("sub")
        return SessionData(user_id=user_id)
    except InvalidTokenError:
        raise InvalidTokenException()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def generate_otp():
    otp_code = ''.join(random.choices(string.digits, k=6))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    return otp_code, expires_at
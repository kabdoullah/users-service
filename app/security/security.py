import jwt
from uuid import UUID
from datetime import datetime, timedelta, timezone
from pydantic import UUID4
from app.models.data.user import User
from app.models.requests.session import SessionData
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.repository.user_repository import UserRepository
from app.exceptions.custom_exception import InvalidTokenException,UserNotFoundException



SECRET_KEY="395b7bec78fa83c6ad70b17837994e29e37884c1a9f9fa241fef7991f489fef7"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], authservie: UserRepository = Depends(UserRepository)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID = payload.get("sub")
        token_data = SessionData(user_id=user_id)
    except InvalidTokenError:
        raise InvalidTokenException()
    user = authservie.get_user_by_id(token_data.user_id)
    if user is None:
        raise UserNotFoundException()
    return user



async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
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

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID4 = payload.get("sub")
        SessionData(user_id=user_id)
    except InvalidTokenError:
        raise InvalidTokenException()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
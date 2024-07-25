from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import UUID4

from app.exceptions.custom_exception import InvalidTokenException
from app.models.data.user import User
from app.models.requests.session import SessionData
from app.repository.user_repository import UserRepository
from app.security.security import ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], authservie: UserRepository = Depends(UserRepository)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID4 = payload.get("sub")
        token_data = SessionData(user_id=user_id)
    except jwt.InvalidTokenError:
        raise InvalidTokenException()
    
    user = authservie.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user



async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

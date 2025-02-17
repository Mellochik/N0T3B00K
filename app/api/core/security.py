from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

import jwt
from passlib.context import CryptContext

from api.repositories.users import get_user
from api.models.users import User
from api.setup import get_db
from api.utils.hash import verify_password
from settings import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    data: dict, 
    expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    """
    Создание токена.
    """
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Расшифровка токена.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        return payload
    except jwt.PyJWTError:
        return None
    
async def authenticate_user(
    db: AsyncSession, 
    username: str, 
    password: str
) -> User | bool:
    """
    Проверка пользователя.
    """
    
    user = await get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False
    
    return user
    
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Получение авторизированного пользователя по токену.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, username)
    if user is None:
        raise credentials_exception
    
    return user
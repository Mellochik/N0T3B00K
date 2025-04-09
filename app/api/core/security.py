from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

from api.core.config import get_auth_data
from api.core.exceptions import UnauthorizedException
from api.models.users import User
from api.repositories.users import UserDAO
from api.utils.hash import verify_password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict) -> str:
    """
    Создание токена.
    """
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Расшифровка токена.
    """
    
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        
        return payload
    except ExpiredSignatureError:
        raise UnauthorizedException(detail="Токен истек")
    except JWTError:
        raise UnauthorizedException(detail="Ошибка токена")

    
async def authenticate_user(username: str, password: str) -> User | None:
    """
    Проверка пользователя.
    """
    
    user = await UserDAO.find_one_or_none(username=username)
    if not user or not verify_password(password, user.password):
        return False
    
    return user
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Получение авторизированного пользователя по токену.
    """
    
    payload: dict = decode_access_token(token)

    username: str = payload.get('sub')
    if not username:
        raise UnauthorizedException(detail='Не найден username пользователя')

    user = await UserDAO.find_one_or_none(username=username)
    if not user:
        raise UnauthorizedException(detail='Пользователь не найден')

    return user

async def get_current_superuser(user: User = Depends(get_current_user)) -> User:
    """
    Получение авторизированного суперпользователя.
    """
    
    if not user.is_superuser:
        raise UnauthorizedException(detail='Недостаточно прав')

    return user
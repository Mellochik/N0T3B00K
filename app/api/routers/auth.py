from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.core.security import create_access_token, get_current_user, \
                              authenticate_user, OAuth2PasswordRequestForm
from api.core.exceptions import BadRequestException, InternalServerErrorException, UnauthorizedException
from api.repositories.users import UserDAO
from api.schemas.users import UserRegister, User
from api.schemas.token import Token
from api.utils.hash import get_password_hash


router = APIRouter(
    tags=["Auth"]
)

# Роуты для работы с аутентификацией пользователя
@router.post(
    "/register", 
    summary="Регистрация пользователя",
    response_class=JSONResponse,
)
async def sign_up_user(new_user: UserRegister) -> JSONResponse:
    """Регистрация пользователя"""
    
    try:
        existing_user = await UserDAO.find_one_or_none(username=new_user.username)
        if existing_user:
            raise BadRequestException
        
        user_dict = new_user.model_dump()
        user_dict['password'] = get_password_hash(new_user.password)
        
        await UserDAO.add(**user_dict)
    except BadRequestException:
        raise BadRequestException(
            detail="Пользователь уже существует"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail="Ошибка регистрации пользователя"
        )

    
    return JSONResponse(content={"message": "Пользователь успешно зарегистрирован"})

@router.post(
    "/login", 
    summary="Авторизация пользователя",
    response_model=Token,
)
async def sign_in_user(user: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Авторизация пользователя"""
    
    existing_user = await authenticate_user(user.username, user.password)
    if existing_user is False:
        raise UnauthorizedException(detail="Неверный логин или пароль")
    access_token = create_access_token(data={"sub": str(existing_user.username)})
    
    return Token(access_token=access_token, token_type="bearer")

@router.get(
    "/me",
    summary="Получение информации о текущем пользователе",
    response_model=User
)
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user

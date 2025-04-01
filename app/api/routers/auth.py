from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from api.core.security import create_access_token, get_current_user, \
                              authenticate_user
from api.core.exceptions import BadRequestException, UnauthorizedException
from api.repositories.users import UserDAO
from api.schemas import UserSignIn, UserSignUp, User, Token
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
async def sign_up_user(new_user: UserSignUp) -> JSONResponse:
    """Регистрация пользователя."""
    
    existing_user = await UserDAO.find_one_or_none(login=new_user.login)
    if existing_user:
        raise BadRequestException(detail="Пользователь уже существует")
    
    user_dict = new_user.model_dump()
    user_dict['password'] = get_password_hash(new_user.password)
    
    await UserDAO.add(**user_dict)
    
    return JSONResponse(content={"message": "Пользователь успешно зарегистрирован"})

@router.post(
    "/login", 
    summary="Авторизация пользователя",
    response_model=Token,
)
async def sign_in_user(response: Response, user: UserSignIn) -> Token:
    """Авторизация пользователя."""
    
    existing_user = await authenticate_user(user.login, user.password)
    if existing_user is False:
        raise UnauthorizedException(detail="Неверный логин или пароль")
    access_token = create_access_token(data={"sub": str(existing_user.login)})
    
    response.set_cookie(
        key="access_token", 
        value=access_token
    )
    
    return Token(access_token=access_token, token_type="jwt")

@router.post(
    "/logout", 
    summary="Выход пользователя из системы",
    response_class=JSONResponse
)
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return JSONResponse(content={'message': 'Пользователь успешно вышел из системы'})

@router.get(
    "/me",
    summary="Получение информации о текущем пользователе",
    response_model=User,
    responses={
        401: {"description": "Не авторизованный пользователь"}
    }
)
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data
from pydantic import BaseModel, ConfigDict, EmailStr, Field

import datetime


class UserSignUp(BaseModel):
    """
    Представляет схему создания пользователя.
    
    Атрибуты:
        login (str): Логин пользователя.
        password (str): Пароль пользователя.
        email (EmailStr): Email пользователя.
        name (str): Имя пользователя.
        surname (str): Фамилия пользователя.
        created_at (date): Дата создания пользователя, по умолчанию - сегодня.
        is_active (bool): Флаг активного пользователя, по умолчанию - False.
    """
    
    login: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime.date = datetime.date.today()
    is_active: bool = True
    

class UserSignIn(BaseModel):
    """
    Представляет схему входа пользователя.
    
    Атрибуты:
        login (str): Логин пользователя.
        password (str): Пароль пользователя.
    """
    
    login: str
    password: str
    
    
class User(BaseModel):
    """
    Представляет схему чтения пользователя.
    
    Атрибуты:
        id (int): Первичный ключ пользователя, автоинкремент.
    """
    
    login: str
    email: str
    first_name: str
    last_name: str
    
    model_config = ConfigDict(from_attributes=True)
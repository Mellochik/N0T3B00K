from pydantic import BaseModel

import datetime


class UserCreate(BaseModel):
    """
    Представляет схему создания пользователя.
    
    Атрибуты:
        created_at (date): Дата создания пользователя, по умолчанию - сегодня.
        is_superuser (bool): Флаг суперпользователя, по умолчанию - False.
        is_active (bool): Флаг активности пользователя, по умолчанию - True.
    """
    
    login: str
    password: str
    email: str
    name: str
    surname: str
    created_at: datetime.date = datetime.date.today()
    is_superuser: bool = False
    is_active: bool = True
    
    
class UserRead(BaseModel):
    """
    Представляет схему чтения пользователя.
    
    Атрибуты:
        id (int): Первичный ключ пользователя, автоинкремент.
    """
    
    id: int
    login: str
    email: str
    name: str
    surname: str
    
    
class User(BaseModel):
    """
    Представляет схему чтения пользователя.
    
    Атрибуты:
        id (int): Первичный ключ пользователя, автоинкремент.
    """
    
    id: int
    name: str
    surname: str
    
    
class UserAuth(BaseModel):
    """
    Представляет схему аутентификации пользователя.
    """
    
    login: str
    password: str
    

class UserUpdate(BaseModel):
    """
    Представляет схему обновления пользователя.
    """
    
    id: int
    password: str
    email: str
    name: str
    surname: str


class UserDelete(BaseModel):
    """
    Представляет схему удаления пользователя.
    """
    
    id: int
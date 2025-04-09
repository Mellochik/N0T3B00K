from pydantic import BaseModel, ConfigDict, EmailStr, Field

import datetime


class UserRegister(BaseModel):
    """
    Схема для создания пользователя.
    
    ```json
    {
        "username": "string",      # Логин пользователя
        "password": "string",      # Пароль пользователя
        "email": "string",         # Email пользователя
        "first_name": "string",    # Имя пользователя
        "last_name": "string",     # Фамилия пользователя
        "created_at": "date"       # Дата создания пользователя (по умолчанию - сегодня)
    }
    ```
    """
    
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime.date = datetime.date.today()
    
    
class User(BaseModel):
    """
    Схема для отображения пользователя.
    
    ```json
    {
        "username": "string",      # Логин пользователя
        "email": "string",         # Email пользователя
        "first_name": "string",    # Имя пользователя
        "last_name": "string"      # Фамилия пользователя
    }
    ```
    """
    
    username: str
    email: str
    first_name: str
    last_name: str
    
    model_config = ConfigDict(from_attributes=True)
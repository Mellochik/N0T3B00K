from pydantic import BaseModel


class Token(BaseModel):
    """
    Схема для отображения токена.
    
    Атрибуты:
        access_token (str): Токен.
        token_type (str): Тип токена.
    """
    
    access_token: str
    token_type: str

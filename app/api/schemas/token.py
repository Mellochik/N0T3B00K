from pydantic import BaseModel


class Token(BaseModel):
    """
    Схема для отображения токена.
    
    ```json
    {
        "access_token": "string", # Токен доступа
        "token_type": "string"    # Тип токена
    }
    ```
    """
    
    access_token: str
    token_type: str

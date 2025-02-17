from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Параметры программы.
    
    Атрибуты:
        secret_key (str): Секретный ключ.
        algorithm (str): Тип алгоритма.
        access_token_expire_minutes (int): Жизнь токена в минутах.
        database_url_for_alembic (str): Строка подключения к БД для alembic.
        database_url_for_api (str): Строка подключения к БД для api.
    """
    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url_for_alembic: str
    database_url_for_api: str

    class Config:
        env_file = ".env"
        
        
settings = Settings()
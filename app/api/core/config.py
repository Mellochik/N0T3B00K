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
    
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        
        
settings = Settings()

def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    
def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
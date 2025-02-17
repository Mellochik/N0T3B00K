from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url_for_alembic: str
    database_url_for_api: str

    class Config:
        env_file = ".env"
        
        
settings = Settings()
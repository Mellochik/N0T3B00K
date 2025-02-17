from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from settings import settings


SQLALCHEMY_DATABASE_URL = settings.database_url_for_api

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def check_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("Соединение успешно!")
    except Exception as e:
        print(f"Ошибка соединения: {e}")


if __name__ == '__main__':
    import asyncio
    asyncio.run(check_connection())
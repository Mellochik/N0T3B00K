from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.models.users import User
from api.schemas.users import UserCreate
from api.utils.hash import get_password_hash

# User
async def create_user(
    user: UserCreate,
    db: AsyncSession
) -> User:
    """Создание пользователя."""
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        login=user.login,
        password=hashed_password,
        email=user.email,
        name=user.name,
        surname=user.surname,
        created_at=user.created_at,
        is_superuser=user.is_superuser,
        is_active=user.is_active,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(
    username: str,
    db: AsyncSession
) -> User:
    """Получение пользователя."""
    
    result = await db.execute(select(User).filter(User.login == username))
    return result.scalar_one_or_none()
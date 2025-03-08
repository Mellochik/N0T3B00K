from sqlalchemy import select as sql_select, update as sql_update, delete as sql_delete
from sqlalchemy.exc import SQLAlchemyError

from api.core.dao import BaseDAO
from api.core.database import async_session_maker
from api.models import User, Space, SpaceUsers


class SpacesDAO(BaseDAO):
    model = Space
    
    @classmethod
    async def add(cls, users_id: list[int] = [], **values) -> object:
        """
        Добавление нового пространства.
        """
        
        async with async_session_maker() as session:
            space: Space = cls.model(**values)
            session.add(space)
            
            for user_id in users_id:
                query = sql_select(User).where(User.id == user_id)
                result = await session.execute(query)
                user: User = result.scalar_one_or_none()
                if user:
                    space_users = SpaceUsers(user_id=user_id, space_id=space.id)
                    session.add(space_users)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            await session.refresh(space)
            return space
        
    @classmethod
    async def update(cls, users_id: list[int], where: dict, **values) -> object:
        """
        Обновление записи в базе данных.
        """
        
        if where is None:
            raise ValueError("Укажите параметры для фильтрации записи.")
        
        async with async_session_maker() as session:
            query = (
                sql_update(cls.model)
                .where(*[getattr(cls.model, k) == v for k, v in where.items()])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            
            space_query = sql_select(cls.model).where(*[getattr(cls.model, k) == v for k, v in where.items()])
            space_result = await session.execute(space_query)
            space = space_result.scalar_one_or_none()
            
            if space:
                current_users_query = sql_select(SpaceUsers).where(SpaceUsers.space_id == space.id)
                current_users_result = await session.execute(current_users_query)
                current_users = {su.user_id for su in current_users_result.scalars().all()}
                
                users_to_remove = current_users - set(users_id)
                for user_id in users_to_remove:
                    delete_query = sql_delete(SpaceUsers).where(SpaceUsers.space_id == space.id, SpaceUsers.user_id == user_id)
                    await session.execute(delete_query)
                
                users_to_add = set(users_id) - current_users
                for user_id in users_to_add:
                    space_user = SpaceUsers(user_id=user_id, space_id=space.id)
                    session.add(space_user)
            
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            return space
        
    @classmethod
    async def find_one_or_none(cls, user_id: int | None = None, **filter_by) -> object:
        """
        Поиск всех записей по фильтру.
        """
        
        async with async_session_maker() as session:
            if user_id is not None:
                query = sql_select(cls.model). \
                    join(SpaceUsers, cls.model.id == SpaceUsers.space_id, isouter=True). \
                    where((cls.model.owner_id == user_id) | (SpaceUsers.user_id == user_id)). \
                    order_by(cls.model.id). \
                    filter_by(**filter_by)
            else:
                query = sql_select(cls.model).order_by(cls.model.id).filter_by(**filter_by)
                
            result = await session.execute(query)
            
            return result.scalar_one_or_none()  
        
    @classmethod
    async def find_all(cls, user_id: int | None = None, **filter_by) -> list[Space]:
        """
        Получение всех пространств пользователя.
        """
        
        async with async_session_maker() as session:
            if user_id is not None:
                query = sql_select(cls.model). \
                    join(SpaceUsers, cls.model.id == SpaceUsers.space_id, isouter=True). \
                    where((cls.model.owner_id == user_id) | (SpaceUsers.user_id == user_id)). \
                    order_by(cls.model.id). \
                    filter_by(**filter_by)
            else:
                query = sql_select(cls.model).order_by(cls.model.id).filter_by(**filter_by)
                
            result = await session.execute(query)
            
            return result.scalars().all()

from sqlalchemy import select as sql_select, update as sql_update, delete as sql_delete
from sqlalchemy.exc import SQLAlchemyError
from api.core.database import async_session_maker
from api.core.logging import logger


class BaseDAO:
    """
    Базовый класс для работы с базой данных.
    """
    
    model = None
    
    @classmethod
    @logger.log_dao_method
    async def add(cls, **values) -> object:
        """
        Добавление новой записи в базу данных.
        """
        
        async with async_session_maker() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.commit()
                await session.refresh(new_instance)
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            return new_instance
        
    @classmethod
    @logger.log_dao_method
    async def update(cls, where: dict, **values) -> object:
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
            
            query = sql_select(cls.model).where(*[getattr(cls.model, k) == v for k, v in where.items()])
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.scalar_one_or_none()
        
    @classmethod
    @logger.log_dao_method
    async def delete(cls, **filter_by) -> int:
        """
        Удаление записи из базы данных.
        """
        
        if filter_by is None:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        async with async_session_maker() as session:
            query = sql_delete(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount
        
    @classmethod
    @logger.log_dao_method
    async def find_one_or_none(cls, **filter_by) -> object:
        """
        Поиск одной записи по идентификатору.
        """
        
        async with async_session_maker() as session:
            query = sql_select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    @logger.log_dao_method
    async def find_all(cls, **filter_by) -> object:
        """
        Поиск всех записей по фильтру.
        """
        
        async with async_session_maker() as session:
            query = sql_select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
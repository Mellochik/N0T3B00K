from sqlalchemy import select as sql_select, update as sql_update, delete as sql_delete
from sqlalchemy.exc import SQLAlchemyError

from api.core.dao import BaseDAO
from api.core.logging import logger
from api.core.database import async_session_maker
import api.models.tasks as models


class BoardDAO(BaseDAO):
    model = models.Board


class StackDAO(BaseDAO):
    model = models.Stack
    

class PriorityDAO(BaseDAO):
    model = models.Priority


class TagDAO(BaseDAO):
    model = models.Tag
    
    
class TaskDAO(BaseDAO):
    model = models.Task
    
    @classmethod
    @logger.log_dao_method
    async def add(cls, tags_id: list[int] | None, **values) -> models.Task:
        """
        Добавление новой задачи.
        """
        
        async with async_session_maker() as session:
            task = cls.model(**values)
            session.add(task)
        
            for tag_id in tags_id:
                query = sql_select(models.Label).where(models.Label.id == tag_id)
                result = await session.execute(query)
                tag = result.scalar_one_or_none()
                if tag:
                    task_tags = models.TaskTags(task_id=task.id, tag_id=tag_id)
                    session.add(task_tags)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            await session.refresh(task)
            return task
        
    @classmethod
    @logger.log_dao_method
    async def update(cls, tags_id: list[int] | None, where: dict, **values) -> models.Task | None:
        """
        Обновление задачи.
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
            
            task_query = sql_select(cls.model).where(*[getattr(cls.model, k) == v for k, v in where.items()])
            task_result = await session.execute(task_query)
            task = task_result.scalar_one_or_none()
            
            if task and tags_id:
                current_tags_query = sql_select(models.TaskTags) \
                    .where(models.TaskTags.task_id == task.id)
                current_tags_result = await session.execute(current_tags_query)
                current_tags = {tl.tag_id for tl in current_tags_result.scalars().all()}
                
                tags_to_remove = current_tags - set(tags_id)
                for tag_id in tags_to_remove:
                    delete_query = sql_delete(models.TaskTags) \
                        .where(models.TaskTags.task_id == task.id, models.TaskTags.tag_id == tag_id)
                    await session.execute(delete_query)
                
                tags_to_add = set(tags_id) - current_tags
                for tag_id in tags_to_add:
                    task_tag = models.TaskTags(task_id=task.id, tag_id=tag_id)
                    session.add(task_tag)
            
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            return task
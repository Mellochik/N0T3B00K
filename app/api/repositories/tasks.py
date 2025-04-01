from sqlalchemy import select as sql_select, update as sql_update, delete as sql_delete
from sqlalchemy.exc import SQLAlchemyError

from api.core.dao import BaseDAO
from api.core.logging import logger
from api.core.database import async_session_maker
from api.models.users import User
import api.models.tasks as models


class SpaceDAO(BaseDAO):
    model = models.Space
    
    @classmethod
    @logger.log_dao_method
    async def add(cls, users_id: list[int] = [], **values) -> models.Space:
        """
        Добавление нового пространства.
        """
        
        async with async_session_maker() as session:
            space = cls.model(**values)
            session.add(space)
            
            for user_id in users_id:
                query = sql_select(User).where(User.id == user_id)
                result = await session.execute(query)
                user = result.scalar_one_or_none()
                if user:
                    space_users = models.SpaceUsers(user_id=user_id, space_id=space.id)
                    session.add(space_users)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            await session.refresh(space)
            return space
        
    @classmethod
    @logger.log_dao_method
    async def update(cls, users_id: list[int], where: dict, **values) -> models.Space | None:
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
                current_users_query = sql_select(models.SpaceUsers) \
                    .where(models.SpaceUsers.space_id == space.id)
                current_users_result = await session.execute(current_users_query)
                current_users = {su.user_id for su in current_users_result.scalars().all()}
                
                users_to_remove = current_users - set(users_id)
                for user_id in users_to_remove:
                    delete_query = sql_delete(models.SpaceUsers) \
                        .where(models.SpaceUsers.space_id == space.id, models.SpaceUsers.user_id == user_id)
                    await session.execute(delete_query)
                
                users_to_add = set(users_id) - current_users
                for user_id in users_to_add:
                    space_user = models.SpaceUsers(user_id=user_id, space_id=space.id)
                    session.add(space_user)
            
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            return space
        
    @classmethod
    @logger.log_dao_method
    async def find_all(cls, user_id: int | None = None, **filter_by) -> list[models.Space] | None:
        """
        Получение всех пространств пользователя.
        """
        
        async with async_session_maker() as session:
            if user_id is not None:
                query = sql_select(cls.model). \
                    join(models.SpaceUsers, cls.model.id == models.SpaceUsers.space_id, isouter=True). \
                    where((cls.model.owner_id == user_id) | (models.SpaceUsers.user_id == user_id)). \
                    order_by(cls.model.id). \
                    filter_by(**filter_by)
            else:
                query = sql_select(cls.model).order_by(cls.model.id).filter_by(**filter_by)
                
            result = await session.execute(query)
            
            return result.scalars().all()


class StackDAO(BaseDAO):
    model = models.Stack
    

class PriorityDAO(BaseDAO):
    model = models.Priority


class StatusDAO(BaseDAO):
    model = models.Status


class LabelDAO(BaseDAO):
    model = models.Label
    
    
class TaskDAO(BaseDAO):
    model = models.Task
    
    @classmethod
    @logger.log_dao_method
    async def add(cls, labels_id: list[int], **values) -> models.Task:
        """
        Добавление новой задачи.
        """
        
        async with async_session_maker() as session:
            task = cls.model(**values)
            session.add(task)
        
            for label_id in labels_id:
                query = sql_select(models.Label).where(models.Label.id == label_id)
                result = await session.execute(query)
                label = result.scalar_one_or_none()
                if label:
                    task_labels = models.TaskLabels(task_id=task.id, label_id=label_id)
                    session.add(task_labels)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            await session.refresh(task)
            return task
        
    @classmethod
    @logger.log_dao_method
    async def update(cls, labels_id: list[int], where: dict, **values) -> models.Task | None:
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
            
            if task:
                current_labels_query = sql_select(models.TaskLabels) \
                    .where(models.TaskLabels.task_id == task.id)
                current_labels_result = await session.execute(current_labels_query)
                current_labels = {tl.label_id for tl in current_labels_result.scalars().all()}
                
                labels_to_remove = current_labels - set(labels_id)
                for label_id in labels_to_remove:
                    delete_query = sql_delete(models.TaskLabels) \
                        .where(models.TaskLabels.task_id == task.id, models.TaskLabels.label_id == label_id)
                    await session.execute(delete_query)
                
                labels_to_add = set(labels_id) - current_labels
                for label_id in labels_to_add:
                    task_label = models.TaskLabels(task_id=task.id, label_id=label_id)
                    session.add(task_label)
            
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            
            return task
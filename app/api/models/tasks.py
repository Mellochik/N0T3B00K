from sqlalchemy import Integer, String, Date, ForeignKey, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import text

from api.models.users import User

import datetime


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(schema="tasks")
    
    @classmethod
    async def create_schema(cls, conn):
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {cls.metadata.schema}"))


class SpaceUser(Base):
    """
    Представляет таблицу ассоциаций между пространствами и пользователями.
    
    Атрибуты:
        id (int): Первичный ключ ассоциации.
        space_id (int): Внешний ключ, ссылающийся на пространство.
        user_id (int): Внешний ключ, ссылающийся на пользователя.
    """
    
    __tablename__ = 'space_user'
    __table_args__ = {'comment': 'Таблица для связи пространств и пользователей'}


    id:       Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    space_id: Mapped[int] = mapped_column(Integer, ForeignKey('spaces.id', ondelete='CASCADE'), nullable=False)
    user_id:  Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return f"SpaceUser(id={self.id}, space_id={self.space_id}, user_id={self.user_id})"

    def __repr__(self):
        return f"<SpaceUser(id={self.id}, space_id={self.space_id}, user_id={self.user_id})>"
    
    
class Space(Base):
    """
    Представляет таблицу пространств.
    
    Атрибуты:
        id (int): Первичный ключ пространства, автоинкремент.
        name (str): Название пространства, не может быть null.
        users (relationship): Связь с моделью User через ассоциативную таблицу SpaceUser.
        columns (relationship): Связь с моделью Column, с back_populates, установленным на "space".
    """
    
    __tablename__ = 'spaces'
    __table_args__ = {'comment': 'Таблица для хранения пространств'}
    

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    
    users = relationship("User", secondary=SpaceUser.__tablename__)
    columns = relationship("Column", back_populates="space", cascade="all, delete-orphan")

    def __str__(self):
        return f"Space(id={self.id}, name={self.name})"

    def __repr__(self):
        return f"<Space(id={self.id}, name={self.name})>"
    

class Column(Base):
    """
    Представляет таблицу колонок.
    
    Атрибуты:
        id (int): Первичный ключ колонки, автоинкремент.
        name (str): Название колонки, не может быть null.
        space_id (int): Внешний ключ, ссылающийся на пространство.
        space (relationship): Связь с моделью Space, с back_populates, установленным на "columns".
        tasks (relationship): Связь с моделью Task, с back_populates, установленным на "column".
    """
    
    __tablename__ = 'columns'
    __table_args__ = {'comment': 'Таблица для хранения колонок'}
    

    id:       Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:     Mapped[str] = mapped_column(String(20), nullable=False)
    space_id: Mapped[int] = mapped_column(Integer, ForeignKey('spaces.id', ondelete="CASCADE"), nullable=False)
    
    space = relationship("Space", back_populates="columns")
    tasks = relationship("Task", back_populates="column", cascade="all, delete-orphan")
    
    def __str__(self):
        return f"Column(id={self.id}, name={self.name}, space_id={self.space_id})"
    
    def __repr__(self):
        return f"<Column(id={self.id}, name={self.name}, space_id={self.space_id})>"


class TaskLabel(Base):
    """
    Представляет таблицу ассоциаций между задачами и метками.
    
    Атрибуты:
        id (int): Первичный ключ ассоциации.
        label_id (int): Внешний ключ, ссылающийся на метку.
        task_id (int): Внешний ключ, ссылающийся на задачу
    """
    
    __tablename__ = 'tasks_labels'
    __table_args__ = {'comment': 'Таблица для связи задач и меток'}
    

    id:       Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label_id: Mapped[int] = mapped_column(Integer, ForeignKey('labels.id'), nullable=False)
    task_id:  Mapped[int] = mapped_column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    
    def __str__(self):
        return f"TaskLabel(id={self.id}, label_id={self.label_id}, task_id={self.task_id})"
    
    def __repr__(self):
        return f"<TaskLabel(id={self.id}, label_id={self.label_id}, task_id={self.task_id})>"


class Task(Base):
    """
    Представляет таблицу задач.
    
    Атрибуты:
        id (int): Первичный ключ задачи, автоинкремент.
        column_id (int): Внешний ключ, ссылающийся на колонку.
        author_id (int): Внешний ключ, ссылающийся на автора задачи.
        title (str): Название задачи, не может быть null.
        description (str): Описание задачи.
        create_date (datetime.date): Дата создания задачи, по умолчанию - сегодняшняя дата.
        date_end (datetime.date): Дата завершения задачи.
        status_id (int): Внешний ключ, ссылающийся на статус задачи.
        priority_id (int): Внешний ключ, ссылающийся на приоритет задачи.
        column (relationship): Связь с моделью Column, с back_populates, установленным на "tasks".
        status (relationship): Связь с моделью Status, с back_populates, установленным на "tasks".
        priority (relationship): Связь с моделью Priority, с back_populates, установленным на "tasks".
        labels (relationship): Связь с моделью Label через ассоциативную таблицу TaskLabel.
    """
    
    __tablename__ = "tasks"
    __table_args__ = {'comment': 'Таблица для хранения задач'}
    

    id:          Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    column_id:   Mapped[int] = mapped_column(Integer, ForeignKey('columns.id', ondelete="CASCADE"), nullable=False)
    author_id:   Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    title:       Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    create_date: Mapped[datetime.date] = mapped_column(Date, nullable=False, default=datetime.date.today)
    date_end:    Mapped[datetime.date] = mapped_column(Date, nullable=True)
    status_id:   Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'), nullable=False)
    priority_id: Mapped[int] = mapped_column(Integer, ForeignKey('priorities.id'), nullable=False)

    column = relationship("Column", back_populates="tasks")
    status = relationship("Status", back_populates="tasks")
    priority = relationship("Priority", back_populates="tasks")
    labels = relationship("Label", secondary=TaskLabel.__tablename__, back_populates="tasks")
    
    def __str__(self):
        return (f"Task(id={self.id}, column_id={self.column_id}, author_id={self.author_id}, title={self.title},"
                f"create_date={self.create_date}, date_end={self.date_end}, status_id={self.status_id}, priority_id={self.priority_id})")
    
    def __repr__(self):
        return (f"<Task(id={self.id}, column_id={self.column_id}, author_id={self.author_id}, title={self.title}," 
                f"create_date={self.create_date}, date_end={self.date_end}, status_id={self.status_id}, priority_id={self.priority_id})>")


class Status(Base):
    """
    Представляет таблицу статусов задач.
    
    Атрибуты:
        id (int): Первичный ключ статуса, автоинкремент.
        name (str): Название статуса, не может быть null.
        tasks (relationship): Связь с моделью Task, с back_populates, установленным на "status".
    """
    
    __tablename__ = "statuses"
    __table_args__ = {'comment': 'Таблица для хранения статусов задач'}
    

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    tasks = relationship("Task", back_populates="status")
    
    def __str__(self):
        return f"Status(id={self.id}, name={self.name})"
    
    def __repr__(self):
        return f"<Status(id={self.id}, name={self.name})>"


class Priority(Base):
    """
    Представляет таблицу приоритетов задач.
    
    Атрибуты:
        id (int): Первичный ключ приоритета, автоинкремент.
        name (str): Название приоритета, не может быть null.
        tasks (relationship): Связь с моделью Task, с back_populates, установленным на "priority".
    """
    
    __tablename__ = "priorities"
    __table_args__ = {'comment': 'Таблица для хранения приоритетов задач'}
    

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    tasks = relationship("Task", back_populates="priority")
    
    def __str__(self):
        return f"Priority(id={self.id}, name={self.name})"
    
    def __repr__(self):
        return f"<Priority(id={self.id}, name={self.name})>"


class Label(Base):
    """
    Представляет таблицу меток задач.
    
    Атрибуты:
        id (int): Первичный ключ метки, автоинкремент.
        name (str): Название метки, не может быть null.
        tasks (relationship): Связь с моделью Task через ассоциативную таблицу TaskLabel.
    """
    
    __tablename__ = "labels"
    __table_args__ = {'comment': 'Таблица для хранения меток задач'}
    

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    tasks = relationship("Task", secondary=TaskLabel.__tablename__, back_populates="labels")
    
    def __str__(self):
        return f"Label(id={self.id}, name={self.name})"
    
    def __repr__(self):
        return f"<Label(id={self.id}, name={self.name})>"

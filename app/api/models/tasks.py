from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.core.database import Base
from api.models.users import User

import datetime


class SpaceUsers(Base):
    """
    Представляет таблицу пространств и пользователей.
    
    Атрибуты:
        id (int): Первичный ключ ассоциации.
        space_id (int): Внешний ключ, ссылающийся на пространство.
        user_id (int): Внешний ключ, ссылающийся на пользователя.
    """
    
    __tablename__ = 'space_users'
    
    id:       Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    space_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.spaces.id", ondelete='CASCADE'),
        nullable=False
    )
    user_id:  Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('space_id', 'user_id', name='uq_space_user'),
        {
            'schema': 'tasks',
            'comment': 'Таблица для связи пространств и пользователей'
        }
    )
    
    def __str__(self):
        return f"SpaceUser(space_id={self.space_id}, user_id={self.user_id})"
    
    def __repr__(self):
        return f"<SpaceUser(space_id={self.space_id}, user_id={self.user_id})>"


class Space(Base):
    """
    Представляет таблицу пространств.
    
    Атрибуты:
        id (int): Первичный ключ пространства, автоинкремент.
        name (str): Название пространства, не может быть null.
        owner_id (int): Внешний ключ, ссылающийся на владельца пространства.
    """
    
    __tablename__ = 'spaces'

    id:       Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:     Mapped[str] = mapped_column(String(20), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    
    owner:  Mapped[User] = relationship(
        User, 
        uselist=False,
        lazy='joined'
    )
    users:  Mapped[list[User]] = relationship(
        User, 
        secondary=SpaceUsers.__table__,
        lazy='joined'
    )
    stacks: Mapped[list["Stack"]] = relationship(
        "Stack", 
        back_populates="space", 
        cascade="all, delete-orphan", 
        lazy='joined'
    )
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения пространств'
    }

    def __str__(self):
        return f"Space(id={self.id}, name={self.name})"

    def __repr__(self):
        return f"<Space(id={self.id}, name={self.name})>"
    

class Stack(Base):
    """
    Представляет таблицу колонок.
    
    Атрибуты:
        id (int): Первичный ключ колонки, автоинкремент.
        name (str): Название колонки, не может быть null.
        space_id (int): Внешний ключ, ссылающийся на пространство.
    """
    
    __tablename__ = 'stacks'
    
    id:       Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:     Mapped[str] = mapped_column(String(20), nullable=False)
    space_id: Mapped[int] = mapped_column(ForeignKey(Space.id, ondelete="CASCADE"), 
                                          nullable=False)
    
    space = relationship("Space", back_populates="stacks")
    tasks = relationship("Task", back_populates="stack", cascade="all, delete-orphan", 
                         lazy='selectin', sync_backref=False)
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения колонок'
    }
    
    def __str__(self):
        return f"Column(id={self.id}, name={self.name}, space_id={self.space_id})"
    
    def __repr__(self):
        return f"<Column(id={self.id}, name={self.name}, space_id={self.space_id})>"


class Status(Base):
    """
    Представляет таблицу статусов задач.
    
    Атрибуты:
        id (int): Первичный ключ статуса, автоинкремент.
        name (str): Название статуса, не может быть null.
    """
    
    __tablename__ = "statuses"

    id:   Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    tasks = relationship("Task", back_populates="status", lazy='selectin')
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения статусов задач'
    }
    
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
    """
    
    __tablename__ = "priorities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    tasks = relationship("Task", back_populates="priority", lazy='selectin')
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения приоритетов задач'
    }
    
    def __str__(self):
        return f"Priority(id={self.id}, name={self.name})"
    
    def __repr__(self):
        return f"<Priority(id={self.id}, name={self.name})>"
    

class TaskLabels(Base):
    """
    Представляет таблицу пространств и пользователей.
    
    Атрибуты:
        id (int): Первичный ключ аcсоциации.
        space_id (int): Внешний ключ, ссылающийся на пространство.
        user_id (int): Внешний ключ, ссылающийся на пользователя.
    """
    
    __tablename__ = 'task_labels'
    
    id:       Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id:  Mapped[int] = mapped_column(ForeignKey("tasks.tasks.id", ondelete='CASCADE'))
    label_id: Mapped[int] = mapped_column(ForeignKey("tasks.labels.id", ondelete='CASCADE'))
    
    __table_args__ = (
        UniqueConstraint('label_id', 'task_id', name='uq_task_labels'),{
            'schema': 'tasks',
            'comment': 'Таблица для связи пространств и пользователей'
        }
    )
    
    def __str__(self):
        return f"SpaceUser(space_id={self.space_id}, user_id={self.user_id})"
    
    def __repr__(self):
        return f"<SpaceUser(space_id={self.space_id}, user_id={self.user_id})>"


class Label(Base):
    """
    Представляет таблицу меток задач.
    
    Атрибуты:
        id (int): Первичный ключ метки, автоинкремент.
        name (str): Название метки, не может быть null.
    """
    
    __tablename__ = "labels"
    
    id:   Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    tasks = relationship("Task", secondary=TaskLabels.__table__, 
                         back_populates="labels", lazy='selectin')
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения меток задач'
    }
    
    def __str__(self):
        return f"Label(id={self.id}, name={self.name})"
    
    def __repr__(self):
        return f"<Label(id={self.id}, name={self.name})>"
    

class Task(Base):
    """
    Представляет таблицу задач.
    
    Атрибуты:
        id (int): Первичный ключ задачи, автоинкремент.
        stack_id (int): Внешний ключ, ссылающийся на колонку.
        author_id (int): Внешний ключ, ссылающийся на автора задачи.
        title (str): Название задачи, не может быть null.
        description (str): Описание задачи.
        create_date (datetime.date): Дата создания задачи, по умолчанию - сегодняшняя дата.
        date_end (datetime.date): Дата завершения задачи.
        status_id (int): Внешний ключ, ссылающийся на статус задачи.
        priority_id (int): Внешний ключ, ссылающийся на приоритет задачи.
    """
    
    __tablename__ = "tasks"

    id:          Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stack_id:   Mapped[int] = mapped_column(ForeignKey(Stack.id, ondelete="CASCADE"), 
                                            nullable=False)
    author_id:   Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    title:       Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    create_date: Mapped[datetime.date] = mapped_column(nullable=False, 
                                                       default=datetime.date.today)
    date_end:    Mapped[datetime.date] = mapped_column(nullable=True)
    status_id:   Mapped[int] = mapped_column(ForeignKey(Status.id), nullable=False)
    priority_id: Mapped[int] = mapped_column(ForeignKey(Priority.id), nullable=False)

    stack = relationship("Stack", back_populates="tasks")
    status = relationship("Status", back_populates="tasks")
    priority = relationship("Priority", back_populates="tasks")
    labels = relationship("Label", secondary=TaskLabels.__table__, 
                          back_populates="tasks", lazy='selectin')
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения задач'
    }
    
    def __str__(self):
        return (f"Task(id={self.id}, column_id={self.column_id}, author_id={self.author_id}, title={self.title},"
                f"create_date={self.create_date}, date_end={self.date_end}, status_id={self.status_id}, priority_id={self.priority_id})")
    
    def __repr__(self):
        return (f"<Task(id={self.id}, column_id={self.column_id}, author_id={self.author_id}, title={self.title}," 
                f"create_date={self.create_date}, date_end={self.date_end}, status_id={self.status_id}, priority_id={self.priority_id})>")

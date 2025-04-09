from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.core.database import Base
from api.models.users import User

import datetime


class Board(Base):
    """
    Представляет таблицу досок.
    
    Атрибуты:
        id (int): Первичный ключ пространства, автоинкремент.
        name (str): Название доски, не может быть null.
    """
    
    __tablename__ = 'boards'

    id:       Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор доски")
    name:     Mapped[str] = mapped_column(nullable=False, comment="Название доски")
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False, comment="Идентификатор владельца доски")
    
    owner:  Mapped[User] = relationship(lazy='selectin')
    stacks: Mapped[list['Stack']] = relationship(
        back_populates='board', 
        cascade='all, delete-orphan', 
        lazy='selectin'
    )
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения досок'
    }

    def __str__(self):
        return f'Board(id={self.id}, name={self.name})'

    def __repr__(self):
        return f'<Board(id={self.id}, name={self.name})>'
    

class Stack(Base):
    """
    Представляет таблицу стопок задач.
    
    Атрибуты:
        id (int): Первичный ключ колонки, автоинкремент.
        name (str): Название колонки, не может быть null.
        board_id (int): Внешний ключ, ссылающийся на доску.
    """
    
    __tablename__ = 'stacks'
    
    id:       Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор стопки")
    name:     Mapped[str] = mapped_column(nullable=False, comment="Название стопки")
    board_id: Mapped[int] = mapped_column(ForeignKey('tasks.boards.id', ondelete='CASCADE'), 
                                          nullable=False, comment="Идентификатор доски")
    
    board: Mapped['Board'] = relationship('Board', back_populates='stacks', lazy='selectin')
    tasks: Mapped[list['Task']] = relationship(
        back_populates='stack', 
        cascade='all, delete-orphan', 
        lazy='selectin'
    )
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения стопок задач'
    }
    
    def __str__(self):
        return f'Stack(id={self.id}, name={self.name}, board_id={self.board_id})'
    
    def __repr__(self):
        return f'<Stack(id={self.id}, name={self.name}, board_id={self.board_id})>'


class Priority(Base):
    '''
    Представляет таблицу приоритетов задач.
    
    Атрибуты:
        id (int): Первичный ключ приоритета, автоинкремент.
        name (str): Название приоритета, не может быть null.
    '''
    
    __tablename__ = 'priorities'

    id:   Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор приоритета")
    name: Mapped[str] = mapped_column(nullable=False, unique=True, comment="Название приоритета")
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения приоритетов задач'
    }
    
    def __str__(self):
        return f'Priority(id={self.id}, name={self.name})'
    
    def __repr__(self):
        return f'<Priority(id={self.id}, name={self.name})>'
    

class TaskTags(Base):
    '''
    Представляет таблицу задач и меток.
    
    Атрибуты:
        id (int): Первичный ключ аcсоциации.
        task_id (int): Внешний ключ, ссылающийся на задачу.
        tag_id (int): Внешний ключ, ссылающийся на метку.
    '''
    
    __tablename__ = 'task_labels'
    
    id:      Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор связи")
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.tasks.id', ondelete='CASCADE'), comment="Идентификатор задачи")
    tag_id:  Mapped[int] = mapped_column(ForeignKey('tasks.labels.id', ondelete='CASCADE'), comment="Идентификатор метки")
    
    __table_args__ = (
        UniqueConstraint('task_id', 'tag_id', name='uq_task_tags'),{
            'schema': 'tasks',
            'comment': 'Таблица для связи задач и меток'
        }
    )
    
    def __str__(self):
        return f'TaskTags(task_id={self.task_id}, tag_id={self.tag_id})'
    
    def __repr__(self):
        return f'<TaskTags(task_id={self.task_id}, tag_id={self.tag_id})>'


class Tag(Base):
    '''
    Представляет таблицу меток задач.
    
    Атрибуты:
        id (int): Первичный ключ метки, автоинкремент.
        name (str): Название метки, не может быть null.
        board_id (int): Внешний ключ, ссылающийся на доску.
    '''
    
    __tablename__ = 'tags'
    
    id:       Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор метки")
    name:     Mapped[str] = mapped_column(nullable=False, unique=True, comment="Название метки")
    board_id: Mapped[int] = mapped_column(ForeignKey('tasks.boards.id', ondelete='CASCADE'),
                                          nullable=False, comment="Идентификатор доски")
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения меток задач'
    }
    
    def __str__(self):
        return f'Tag(id={self.id}, name={self.name})'
    
    def __repr__(self):
        return f'<Tag(id={self.id}, name={self.name})>'
    

class Task(Base):
    '''
    Представляет таблицу задач.
    
    Атрибуты:
        id (int): Первичный ключ задачи, автоинкремент.
        stack_id (int): Внешний ключ, ссылающийся на стопку.
        title (str): Название задачи, не может быть null.
        create_date (datetime.date): Дата создания задачи, по умолчанию - сегодняшняя дата.
        date_end (datetime.date): Дата завершения задачи.
        status_id (int): Внешний ключ, ссылающийся на статус задачи.
        priority_id (int): Внешний ключ, ссылающийся на приоритет задачи.
        description (str): Описание задачи.
        solution (str): Решение задачи.
        archived (bool): Флаг, указывающий на архивирование задачи.
    '''
    
    __tablename__ = 'tasks'

    id:          Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор задачи")
    stack_id:    Mapped[int] = mapped_column(ForeignKey(Stack.id, ondelete="CASCADE"), 
                                             nullable=False, comment="Идентификатор стопки")
    title:       Mapped[str] = mapped_column(nullable=False, comment="Название задачи")
    create_date: Mapped[datetime.datetime] = mapped_column(nullable=False, 
                                                           default=datetime.datetime.today, comment="Дата создания задачи")
    date_end:    Mapped[datetime.datetime] = mapped_column(nullable=True, comment="Дата завершения задачи")
    priority_id: Mapped[int] = mapped_column(ForeignKey('tasks.priorities.id'), nullable=False, comment="Идентификатор приоритета задачи")
    description: Mapped[str] = mapped_column(nullable=True, comment="Описание задачи")
    solution:    Mapped[str] = mapped_column(nullable=True, comment="Решение задачи")
    archived:    Mapped[bool] = mapped_column(nullable=False, default=False, comment="Флаг архивирования задачи")

    stack:    Mapped['Stack'] = relationship(back_populates='tasks', lazy='selectin')
    priority: Mapped['Priority'] = relationship(lazy='selectin')
    tags:     Mapped[list['Tag']] = relationship(secondary='tasks.task_labels', lazy='selectin')
    
    __table_args__ = {
        'schema': 'tasks',
        'comment': 'Таблица для хранения задач'
    }
    
    @property
    def has_solution(self) -> bool:
        return bool(self.solution)
    
    def __str__(self):
        return (f'Task(id={self.id}, stack_id={self.stack_id}, title={self.title}, create_date={self.create_date}, '
                f'date_end={self.date_end}, status_id={self.status_id}, priority_id={self.priority_id})')
    
    def __repr__(self):
        return (f'<Task(id={self.id}, stack_id={self.stack_id}, title={self.title}, create_date={self.create_date}, ' 
                f'date_end={self.date_end}, status_id={self.status_id}, priority_id={self.priority_id})>')

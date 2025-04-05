from pydantic import BaseModel, ConfigDict
from pydantic import Field

import datetime

from api.schemas.users import User


# Space
class SpaceBase(BaseModel):
    """
    Базовая модель для пространства.
    
    Атрибуты:
        name (str): Название пространства.
    """
    
    name: str
    

class SpaceCreate(SpaceBase):
    """
    Модель для создания пространства.
    
    Атрибуты:
        users_id (list[int]): Список идентификаторов пользователей, которые будут добавлены в пространство.
    """
    
    users_id: list[int]
    
    
class Space(SpaceBase):  
    id: int
    users: list[User]
    
    model_config = ConfigDict(from_attributes=True)
        

class SpaceUpdate(SpaceBase):
    """
    Модель для обновления пространства.
    
    Атрибуты:
        id (int): Идентификатор пространства.
        users_id (list[int]): Список идентификаторов пользователей, которые будут добавлены в пространство.
    """
    
    id: int
    users_id: list[int]


# Stack
class StackBase(BaseModel):
    """
    Базовая модель для стопки.
    
    Атрибуты:
        name (str): Название стопки.
    """
    
    name: str
    

class StackCreate(StackBase):
    """
    Модель для создания стопки.
    
    Атрибуты:
        space_id (int): Идентификатор пространства, к которому будет привязана стопка.
    """
    
    space_id: int
    
    
class Stack(StackBase):
    """
    Модель для чтения стопки.
    
    Атрибуты:
        id (int): Идентификатор стопки.
        space (SpaceBase): Пространство, к которому привязана стопка.
        tasks (list[TaskRead]): Список задач, привязанных к стопке.
    """
    
    id: int
    tasks: list["TaskCard"]
    
    model_config = ConfigDict(from_attributes=True)
        

class StackUpdate(StackBase):
    """
    Модель для обновления стопки.
    
    Атрибуты:
        id (int): Идентификатор стопки.
        space_id (int): Идентификатор пространства, к которому будет привязана колонка.
    """
    
    id: int
    space_id: int
    

class StackDelete(BaseModel):
    """
    Модель для удаления стопки.
    
    Атрибуты:
        id (int): Идентификатор стопки.
    """
    
    id: int
    

# Task
class TaskCard(BaseModel):
    """
    Модель для карточки задачи.
    
    Атрибуты:
        id (int): Идентификатор задачи.
        title (str): Заголовок задачи.
        date_end (datetime.date | None): Дата завершения задачи.
    """
    
    id: int
    title: str
    date_end: datetime.date | None
    status: "Status"
    priority: "Priority"
    labels: list["Label"]


class TaskBase(BaseModel):
    """
    Базовая модель для задачи.
    
    Атрибуты:
        title (str): Заголовок задачи.
        description (str): Описание задачи.
        date_end (datetime.date | None): Дата завершения задачи.
    """
    
    title: str
    description: str
    date_end: datetime.date | None


class TaskCreate(TaskBase):
    """
    Модель для создания задачи.
    
    Атрибуты:
        stack_id (int): Идентификатор колонки, к которой будет привязана задача.
        author_id (int): Идентификатор автора задачи.
        priority_id (int): Идентификатор приоритета задачи.
        status_id (int): Идентификатор статуса задачи.
        labels_id (list[int]): Список идентификаторов меток задачи.
    """
    
    stack_id: int
    author_id: int
    create_date: datetime.date = datetime.date.today()
    priority_id: int
    status_id: int
    labels_id: list[int]
    

class Task(TaskBase):
    """
    Модель для чтения задачи.
    
    Атрибуты:
        id (int): Идентификатор задачи.
        column (StackBase): Колонка, к которой привязана задача.
        author (UserRead): Автор задачи.
        status (Status): Статус задачи.
        priority (Priority): Приоритет задачи.
        labels (list[Label]): Список меток задачи.
    """
    
    id: int
    stack: StackBase
    author: User
    status: "Status"
    priority: "Priority"
    labels: list["Label"]
    
    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(TaskBase):
    """
    Модель для обновления задачи.
    
    Атрибуты:
        id (int): Идентификатор задачи.
        stack_id (int): Идентификатор колонки, к которой будет привязана задача.
        priority_id (int): Идентификатор приоритета задачи.
        status_id (int): Идентификатор статуса задачи.
        labels_id (list[int]): Список идентификаторов меток задачи.
    """
    
    id: int
    stack_id: int
    priority_id: int
    status_id: int
    labels_id: list[int]
    
    
class TaskDelete(BaseModel):
    """
    Модель для удаления задачи.
    
    Атрибуты:
        id (int): Идентификатор задачи.
    """
    
    id: int
    

# Priority
class PriorityBase(BaseModel):
    """
    Базовая модель для приоритета.
    
    Атрибуты:
        name (str): Название приоритета.
    """
    
    name: str


class PriorityCreate(PriorityBase):
    """
    Модель для создания приоритета.
    """
    
    pass


class Priority(PriorityBase):
    """
    Модель для чтения приоритета.
    
    Атрибуты:
        id (int): Идентификатор приоритета.
    """
    
    id: int

    model_config = ConfigDict(from_attributes=True)


# Status
class StatusBase(BaseModel):
    """
    Базовая модель для статуса.
    
    Атрибуты:
        name (str): Название статуса.
    """
    
    name: str


class StatusCreate(StatusBase):
    """
    Модель для создания статуса.
    """
    
    pass


class Status(StatusBase):
    """
    Модель для чтения статуса.
    
    Атрибуты:
        id (int): Идентификатор статуса.
    """
    
    id: int

    model_config = ConfigDict(from_attributes=True)


# Labels
class LabelBase(BaseModel):
    """
    Базовая модель для метки.
    
    Атрибуты:
        name (str): Название метки.
    """
    
    name: str


class LabelCreate(LabelBase):
    """
    Модель для создания метки.
    """
    
    pass


class Label(LabelBase):
    """
    Модель для чтения метки.
    
    Атрибуты:
        id (int): Идентификатор метки.
    """
    
    id: int

    model_config = ConfigDict(from_attributes=True)


class LabelUpdate(LabelBase):
    """
    Модель для обновления метки.
    
    Атрибуты:
        id (int): Идентификатор метки.
    """
    
    id: int
    
    
class LabelDelete(BaseModel):
    """
    Модель для удаления метки.
    
    Атрибуты:
        id (int): Идентификатор метки.
    """
    
    id: int
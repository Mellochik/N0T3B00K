from pydantic import BaseModel

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
    
    
class SpaceRead(SpaceBase):  
    id: int
    users: list["User"]
    columns: list["ColumnRead"]
    
    class Config:
        from_attributes = True
        

class SpaceUpdate(SpaceBase):
    """
    Модель для обновления пространства.
    
    Атрибуты:
        id (int): Идентификатор пространства.
        users_id (list[int]): Список идентификаторов пользователей, которые будут добавлены в пространство.
    """
    
    id: int
    users_id: list[int]
    
    
class SpaceDelete(BaseModel):
    """
    Модель для удаления пространства.
    
    Атрибуты:
        id (int): Идентификатор пространства.
    """
    
    id: int


# Column
class ColumnBase(BaseModel):
    """
    Базовая модель для колонки.
    
    Атрибуты:
        name (str): Название колонки.
    """
    
    name: str
    

class ColumnCreate(ColumnBase):
    """
    Модель для создания колонки.
    
    Атрибуты:
        space_id (int): Идентификатор пространства, к которому будет привязана колонка.
    """
    
    space_id: int
    
    
class ColumnRead(ColumnBase):
    """
    Модель для чтения колонки.
    
    Атрибуты:
        id (int): Идентификатор колонки.
        space (SpaceBase): Пространство, к которому привязана колонка.
        tasks (list[TaskRead]): Список задач, привязанных к колонке.
    """
    
    id: int
    space: "SpaceBase"
    tasks: list["TaskRead"]
    
    class Config:
        from_attributes = True
        

class ColumnUpdate(ColumnBase):
    """
    Модель для обновления колонки.
    
    Атрибуты:
        id (int): Идентификатор колонки.
        space_id (int): Идентификатор пространства, к которому будет привязана колонка.
    """
    
    id: int
    space_id: int
    

class ColumnDelete(BaseModel):
    """
    Модель для удаления колонки.
    
    Атрибуты:
        id (int): Идентификатор колонки.
    """
    
    id: int
    

# Task
class TaskBase(BaseModel):
    """
    Базовая модель для задачи.
    
    Атрибуты:
        title (str): Заголовок задачи.
        description (str): Описание задачи.
        create_date (datetime): Дата создания задачи.
        date_end (datetime.date | None): Дата завершения задачи.
    """
    
    title: str
    description: str
    date_end: datetime.date | None


class TaskCreate(TaskBase):
    """
    Модель для создания задачи.
    
    Атрибуты:
        column_id (int): Идентификатор колонки, к которой будет привязана задача.
        author_id (int): Идентификатор автора задачи.
        priority_id (int): Идентификатор приоритета задачи.
        status_id (int): Идентификатор статуса задачи.
        labels_id (list[int]): Список идентификаторов меток задачи.
    """
    
    column_id: int
    author_id: int
    create_date: datetime.date = datetime.date.today()
    priority_id: int
    status_id: int
    labels_id: list[int]
    

class TaskRead(TaskBase):
    """
    Модель для чтения задачи.
    
    Атрибуты:
        id (int): Идентификатор задачи.
        column (ColumnBase): Колонка, к которой привязана задача.
        author (UserRead): Автор задачи.
        status (Status): Статус задачи.
        priority (Priority): Приоритет задачи.
        labels (list[Label]): Список меток задачи.
    """
    
    id: int
    column: ColumnBase
    author: User
    status: "StatusRead"
    priority: "PriorityRead"
    labels: list["LabelRead"]
    
    class Config:
        from_attributes = True


class TaskUpdate(TaskBase):
    """
    Модель для обновления задачи.
    
    Атрибуты:
        id (int): Идентификатор задачи.
        column_id (int): Идентификатор колонки, к которой будет привязана задача.
        priority_id (int): Идентификатор приоритета задачи.
        status_id (int): Идентификатор статуса задачи.
        labels_id (list[int]): Список идентификаторов меток задачи.
    """
    
    id: int
    column_id: int
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


class PriorityRead(PriorityBase):
    """
    Модель для чтения приоритета.
    
    Атрибуты:
        id (int): Идентификатор приоритета.
    """
    
    id: int

    class Config:
        from_attributes = True


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


class StatusRead(StatusBase):
    """
    Модель для чтения статуса.
    
    Атрибуты:
        id (int): Идентификатор статуса.
    """
    
    id: int

    class Config:
        from_attributes = True


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


class LabelRead(LabelBase):
    """
    Модель для чтения метки.
    
    Атрибуты:
        id (int): Идентификатор метки.
    """
    
    id: int

    class Config:
        from_attributes = True


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
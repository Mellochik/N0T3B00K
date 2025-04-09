import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Board
class BoardCreate(BaseModel):
    """
    Схема создания доски.

    ```json
    {
        "name": "str",    # Название доски
        "owner_id": "int" # Идентификатор владельца
    }
    ```
    """
    
    name: str = Field(..., title="Название доски", min_length=1, max_length=100)
    owner_id: int = Field(..., title="Идентификатор владельца", ge=1)


class BoardRead(BaseModel):
    """
    Схема чтения доски.

    ```json
    {
        "id": "int",  # Идентификатор доски
        "name": "str" # Название доски
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор доски", ge=1)
    name: str = Field(..., title="Название доски", max_length=100)

    model_config = ConfigDict(from_attributes=True)


class BoardUpdate(BaseModel):
    """
    Схема обновления доски.

    ```json
    {
        "id": "int",  # Идентификатор доски
        "name": "str" # Название доски
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор доски", ge=1)
    name: str = Field(..., title="Название доски", min_length=1, max_length=100)


# Stack
class StackCreate(BaseModel):
    """
    Схема создания стопки.

    ```json
    {
        "name": "str",    # Название стопки
        "board_id": "int" # Идентификатор доски
    }
    ```
    """
    
    name: str = Field(..., title="Название стопки", max_length=50)
    board_id: int = Field(..., title="Идентификатор доски", ge=1)


class StackRead(BaseModel):
    """
    Схема чтения стопки.

    ```json
    {
        "id": "int",                           # Идентификатор стопки
        "name": "str",                         # Название стопки
        "tasks": [                             # Список задач
            {
                "id": "int",                   # Идентификатор задачи
                "title": "str",                # Заголовок задачи
                "date_end": "datetime | None", # Дата завершения
                "priority": {                  # Приоритет задачи
                    "id": "int",               # Идентификатор приоритета
                    "name": "str"              # Название приоритета
                },
                "tags": [                      # Список меток
                    {
                        "id": "int",           # Идентификатор метки
                        "name": "str"          # Название метки
                    }
                ],
                "has_solution": "bool"         # Наличие решения
            }
        ]
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор стопки", ge=1)
    name: str = Field(..., title="Название стопки", max_length=50)
    tasks: list["TaskCardRead"] = Field(..., title="Список задач")

    model_config = ConfigDict(from_attributes=True)


class StackUpdate(BaseModel):
    """
    Схема обновления стопки.

    ```json
    {
        "id": "int",      # Идентификатор стопки
        "name": "str",    # Название стопки
        "board_id": "int" # Идентификатор доски
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор стопки", ge=1)
    name: str = Field(..., title="Название стопки", max_length=50)
    board_id: int = Field(..., title="Идентификатор доски", ge=1)


# Priority
class PriorityRead(BaseModel):
    """
    Схема чтения приоритета.

    ```json
    {
        "id": "int",  # Идентификатор приоритета
        "name": "str" # Название приоритета
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор приоритета", ge=1)
    name: str = Field(..., title="Название приоритета", max_length=50)

    model_config = ConfigDict(from_attributes=True)


# Tags
class TagCreate(BaseModel):
    """
    Схема создания метки.

    ```json
    {
        "name": "str",    # Название метки
        "board_id": "int" # Идентификатор доски
    }
    ```
    """
    
    name: str = Field(..., title="Название метки", min_length=1, max_length=50)
    board_id: int = Field(..., title="Идентификатор доски", ge=1)


class TagRead(BaseModel):
    """
    Схема чтения метки.

    ```json
    {
        "id": "int",  # Идентификатор метки
        "name": "str" # Название метки
    }
    ```
    """
    id: int = Field(..., title="Идентификатор метки", ge=1)
    name: str = Field(..., title="Название метки", max_length=50)

    model_config = ConfigDict(from_attributes=True)


class TagUpdate(BaseModel):
    """
    Схема обновления метки.

    ```json
    {
        "id": "int",      # Идентификатор метки
        "name": "str",    # Название 
        "board_id": "int" # Идентификатор доски
    }
    ```
    """
    id: int = Field(..., title="Идентификатор метки", ge=1)
    name: str = Field(..., title="Название метки", min_length=1, max_length=50)
    board_id: int = Field(..., title="Идентификатор доски", ge=1)


# Task
class TaskCreate(BaseModel):
    """
    Схема создания задачи.

    ```json
    {
        "stack_id": "int",             # Идентификатор стопки
        "title": "str",                # Заголовок задачи
        "create_date": "datetime",     # Дата создания
        "date_end": "datetime | None", # Дата завершения
        "priority_id": "int",          # Идентификатор приоритета
        "tags_id": "list[int]"         # Список идентификаторов меток
    }
    ```
    """
    
    stack_id: int = Field(..., title="Идентификатор стопки", ge=1)
    title: str = Field(..., title="Заголовок задачи", min_length=1, max_length=200)
    create_date: datetime.datetime = Field(default_factory=datetime.datetime.today, title="Дата создания")
    date_end: Optional[datetime.datetime] = Field(None, title="Дата завершения")
    priority_id: int = Field(..., title="Идентификатор приоритета", ge=1)
    tags_id: list[int] = Field(..., title="Список идентификаторов меток")
    description: Optional[str] = Field(None, title="Описание задачи", max_length=500)

    @field_validator("date_end")
    def validate_date_end(cls, value, values):
        if value and value < values.get("create_date"):
            raise ValueError("Дата завершения не может быть раньше даты создания.")
        return value


class TaskRead(BaseModel):
    """
    Схема чтения задачи.

    ```json
    {
        "id": "int",                   # Идентификатор задачи
        "title": "str",                # Заголовок задачи
        "create_date": "datetime",     # Дата создания
        "date_end": "datetime | None", # Дата завершения
        "priority": {                  # Приоритет задачи
            "id": "int",               # Идентификатор приоритета
            "name": "str"              # Название приоритета
        },
        "tags": [                      # Список меток
            {
                "id": "int",           # Идентификатор метки
                "name": "str"          # Название метки
            }
        ],
        "description": "str | None",   # Описание задачи
        "solution": "str | None"       # Решение задачи
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор задачи", ge=1)
    title: str = Field(..., title="Заголовок задачи", max_length=200)
    create_date: datetime.datetime = Field(..., title="Дата создания")
    date_end: Optional[datetime.datetime] = Field(None, title="Дата завершения")
    priority: "PriorityRead" = Field(..., title="Приоритет задачи")
    tags: list["TagRead"] = Field(..., title="Список меток")
    description: Optional[str] = Field(None, title="Описание задачи", max_length=500)
    solution: Optional[str] = Field(None, title="Решение задачи", max_length=500)

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """
    Схема обновления задачи.

    ```json
    {
        "id": "int",                   # Идентификатор задачи
        "stack_id": "int",             # Идентификатор стопки
        "title": "str",                # Заголовок задачи
        "date_end": "datetime | None", # Дата завершения
        "priority_id": "int",          # Идентификатор приоритета
        "tags_id": "list[int]",        # Список идентификаторов меток
        "description": "str | None",   # Описание задачи
        "solution": "str | None",      # Решение задачи
        "archived": "bool"             # Архивный статус
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор задачи", ge=1)
    stack_id: int = Field(..., title="Идентификатор стопки", ge=1)
    title: str = Field(..., title="Заголовок задачи", min_length=1, max_length=200)
    date_end: Optional[datetime.datetime] = Field(None, title="Дата завершения")
    priority_id: int = Field(..., title="Идентификатор приоритета", ge=1)
    tags_id: list[int] = Field(..., title="Список идентификаторов меток")
    description: Optional[str] = Field(None, title="Описание задачи", max_length=500)
    solution: Optional[str] = Field(None, title="Решение задачи", max_length=500)
    archived: bool = Field(default=False, title="Архивный статус")

    @field_validator("date_end")
    def validate_date_end(cls, value, values):
        if value and value < values.get("create_date"):
            raise ValueError("Дата завершения не может быть раньше даты создания.")
        return value


class TaskCardCreate(BaseModel):
    """
    Схема создания карточки задачи.

    ```json
    {
        "stack_id": "int", # Идентификатор стопки
        "title": "str"     # Заголовок задачи
    }
    ```
    """
    
    stack_id: int = Field(..., title="Идентификатор стопки", ge=1)
    title: str = Field(..., title="Заголовок задачи", min_length=1, max_length=200)


class TaskCardRead(BaseModel):
    """
    Схема чтения карточки задачи.

    ```json
    {
        "id": "int",                   # Идентификатор задачи
        "title": "str",                # Заголовок задачи
        "date_end": "datetime | None", # Дата завершения
        "priority": {                  # Приоритет задачи
            "id": "int",               # Идентификатор приоритета
            "name": "str"              # Название приоритета
        },
        "tags": [                      # Список меток
            {
                "id": "int",           # Идентификатор метки
                "name": "str"          # Название метки
            }
        ],
        "has_solution": "bool"         # Наличие решения
    }
    ```
    """
    
    id: int = Field(..., title="Идентификатор задачи", ge=1)
    title: str = Field(..., title="Заголовок задачи", max_length=200)
    date_end: datetime.date | None = Field(None, title="Дата завершения")
    priority: "PriorityRead" = Field(..., title="Приоритет задачи")
    tags: list["TagRead"] = Field(..., title="Список меток")
    has_solution: bool = Field(..., title="Наличие решения")

    model_config = ConfigDict(from_attributes=True)
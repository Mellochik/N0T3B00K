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
    documents: list["DocumentRead"]
    
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
    
    
# Document
class DocumentBase(BaseModel):
    """
    Базовая модель для документа.
    
    Атрибуты:
        title (str): Название документа.
        content (str): Содержимое документа.
    """
    
    title: str
    content: str
    

class DocumentCreate(DocumentBase):
    """
    Модель для создания документа.
    
    Атрибуты:
        space_id (int): Идентификатор пространства.
        parent_id (int): Идентификатор родительского документа.
        author_id (int): Идентификатор автора документа.
    """
    
    space_id: int
    parent_id: int
    author_id: int
    created_at: datetime.date = datetime.date.today()
    
    
class DocumentRead(DocumentBase):
    """
    Модель для чтения документа.
    
    Атрибуты:
        id (int): Идентификатор документа.
        space_id (int): Идентификатор пространства.
        parent_id (int): Идентификатор родительского документа.
        author (UserRead): Автор документа.
        created_at (datetime.date): Дата создания документа.
    """
    
    id: int
    space_id: int
    parent_id: int
    author: User
    created_at: datetime.date = datetime.date.today()
    
    
class DocumentUpdate(DocumentBase):
    """
    Модель для обновления документа.
    
    Атрибуты:
        id (int): Идентификатор документа.
        space_id (int): Идентификатор пространства.
        parent_id (int): Идентификатор родительского документа.
        author_id (int): Идентификатор автора документа.
    """
    
    id: int
    space_id: int
    parent_id: int
    
    
class DocumentDelete(BaseModel):
    """
    Модель для удаления документа.
    
    Атрибуты:
        id (int): Идентификатор документа.
    """
    
    id: int
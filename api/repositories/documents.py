from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.documents as schemas
import api.models.documents as models


# Space
async def create_space(
    space: schemas.SpaceCreate,
    db: AsyncSession 
) -> schemas.SpaceRead:
    """
    Создание пространства.
    
    Аргументы:
        space (SpaceCreate): Модель для создания пространства.
        db (AsyncSession): Сессия базы данных.
    """
    
    new_space = models.Space(name=space.name)
    db.add(new_space)
    for user_id in space.users_id:
        user = await db.get(models.User, user_id)
        new_space.users.append(user)
        
    await db.commit()
    await db.refresh(new_space)
    
    return new_space

async def read_spaces(
    db: AsyncSession
) -> list[schemas.SpaceRead]:
    """
    Получение списка пространств.
    
    Аргументы:
        db (AsyncSession): Сессия базы данных.
    """
    
    spaces = await db.query(models.Space).all()
    
    return spaces

async def read_space(
    space_id: int,
    db: AsyncSession 
) -> schemas.SpaceRead:
    """
    Получение пространства.
    
    Аргументы:
        space_id (int): Идентификатор пространства.
        db (AsyncSession): Сессия базы данных.
    """
    
    space = await db.query(models.Space).filter(models.Space.id == space_id).first()
    
    return space

async def update_space(
    space: schemas.SpaceUpdate,
    db: AsyncSession 
) -> schemas.SpaceRead:
    """
    Обновление пространства.
    
    Аргументы:
        space (SpaceUpdate): Модель для обновления пространства.
        db (AsyncSession): Сессия базы данных.
    """
    
    existing_space = await db.get(models.Space, space.id)
    existing_space.name = space.name
    
    existing_user_ids = {user.id for user in existing_space.users}
    new_user_ids = set(space.users_id)
    
    for user_id in new_user_ids - existing_user_ids:
        user = await db.get(models.User, user_id)
        existing_space.users.append(user)
    
    for user_id in existing_user_ids - new_user_ids:
        user = await db.get(models.User, user_id)
        existing_space.users.remove(user)
    
    await db.commit()
    await db.refresh(existing_space)
    
    return existing_space

async def delete_space(
    space: schemas.SpaceDelete,
    db: AsyncSession 
) -> schemas.SpaceRead:
    """
    Удаление пространства.
    
    Аргументы:
        space_id (int): Идентификатор пространства.
        db (AsyncSession): Сессия базы данных.
    """
    
    space = await db.get(models.Space, space.id)
    db.delete(space)
    
    await db.commit()
    
    return space

# Document
async def create_document(
    document: schemas.DocumentCreate,
    db: AsyncSession 
) -> schemas.DocumentRead:
    """
    Создание документа.
    
    Аргументы:
        document (DocumentCreate): Модель для создания документа.
        db (AsyncSession): Сессия базы данных.
    """
    
    new_document = models.Document(
        space_id=document.space_id,
        parent_id=document.parent_id,
        author_id=document.author_id,
        title=document.title,
        content=document.content,
        created_at=document.created_at
    )
    db.add(new_document)
    
    await db.commit()
    await db.refresh(new_document)
    
    return new_document

async def read_documents(
    db: AsyncSession
) -> list[schemas.DocumentRead]:
    """
    Получение списка документов.
    
    Аргументы:
        db (AsyncSession): Сессия базы данных.
    """
    
    documents = await db.query(models.Document).all()
    
    return documents

async def read_document(
    document_id: int,
    db: AsyncSession 
) -> schemas.DocumentRead:
    """
    Получение документа.
    
    Аргументы:
        document_id (int): Идентификатор документа.
        db (AsyncSession): Сессия базы данных.
    """
    
    document = await db.query(models.Document).filter(models.Document.id == document_id).first()
    
    return document

async def update_document(
    document: schemas.DocumentUpdate,
    db: AsyncSession 
) -> schemas.DocumentRead:
    """
    Обновление документа.
    
    Аргументы:
        document (DocumentUpdate): Модель для обновления документа.
        db (AsyncSession): Сессия базы данных.
    """
    
    existing_document = await db.get(models.Document, document.id)
    existing_document.space_id = document.space_id
    existing_document.parent_id = document.parent_id
    existing_document.title = document.title
    existing_document.content = document.content
    
    await db.commit()
    await db.refresh(existing_document)
    
    return existing_document

async def delete_document(
    document: schemas.DocumentDelete,
    db: AsyncSession 
) -> schemas.DocumentRead:
    """
    Удаление документа.
    
    Аргументы:
        document_id (int): Идентификатор документа.
        db (AsyncSession): Сессия базы данных.
    """
    
    document = await db.get(models.Document, document.id)
    db.delete(document)
    
    await db.commit()
    
    return document
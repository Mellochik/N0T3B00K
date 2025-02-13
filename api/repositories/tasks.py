from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import api.schemas.tasks as schemas
import api.models.tasks as models


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
        result = await db.execute(select(models.User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        if user:
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
    
    result = await db.execute(select(models.Space))
    spaces = result.scalars().all()
    
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
    
    result = await db.execute(select(models.Space).filter_by(id=space_id))
    space = result.scalar_one_or_none()
    
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
        result = await db.execute(select(models.User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        if user:
            existing_space.users.append(user)
    
    for user_id in existing_user_ids - new_user_ids:
        result = await db.execute(select(models.User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        if user:
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

# Column
async def create_column(
    column: schemas.ColumnCreate,
    db: AsyncSession 
) -> schemas.ColumnRead:
    """
    Создание колонки.
    
    Аргументы:
        column (ColumnCreate): Модель для создания колонки.
        db (AsyncSession): Сессия базы данных.
    """
    
    new_column = models.Column(name=column.name, space_id=column.space_id)
    db.add(new_column)
    
    await db.commit()
    await db.refresh(new_column)
    
    return new_column

async def read_columns(
    db: AsyncSession
) -> list[schemas.ColumnRead]:
    """
    Получение списка колонок.
    
    Аргументы:
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Column))
    columns = result.scalars().all()
    
    return columns

async def read_column(
    column_id: int,
    db: AsyncSession 
) -> schemas.ColumnRead:
    """
    Получение колонки.
    
    Аргументы:
        column_id (int): Идентификатор колонки.
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Column).filter_by(id=column_id))
    column = result.scalar_one_or_none()
    
    return column

async def update_column(
    column: schemas.ColumnUpdate,
    db: AsyncSession 
) -> schemas.ColumnRead:
    """
    Обновление колонки.
    
    Аргументы:
        column (ColumnUpdate): Модель для обновления колонки.
        db (AsyncSession): Сессия базы данных.
    """
    
    existing_column = await db.get(models.Column, column.id)
    existing_column.name = column.name
    existing_column.space_id = column.space_id
    
    await db.commit()
    await db.refresh(existing_column)
    
    return existing_column

async def delete_column(
    column: schemas.ColumnDelete,
    db: AsyncSession 
) -> schemas.ColumnRead:
    """
    Удаление колонки.
    
    Аргументы:
        column_id (int): Идентификатор колонки.
        db (AsyncSession): Сессия базы данных.
    """
    
    column = await db.get(models.Column, column.id)
    db.delete(column)
    
    await db.commit()
    
    return column

# Task
async def create_task(
    task: schemas.TaskCreate,
    db: AsyncSession 
) -> schemas.TaskRead:
    """
    Создание задачи.
    
    Аргументы:
        task (TaskCreate): Модель для создания задачи.
        db (AsyncSession): Сессия базы данных.
    """
    
    new_task = models.Task(
        column_id=task.column_id,
        author_id=task.author_id,
        title=task.title,
        description=task.description,
        create_date=task.create_date,
        date_end=task.date_end,
        status_id=task.status_id,
        priority_id=task.priority_id
    )
    db.add(new_task)
    for label_id in task.labels_id:
        db.add(models.TaskLabel(label_id=label_id, task_id=new_task.id))
    
    await db.commit()
    await db.refresh(new_task)
    
    return new_task

async def read_tasks(
    db: AsyncSession
) -> list[schemas.TaskRead]:
    """
    Получение списка задач.
    
    Аргументы:
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Task))
    tasks = result.scalars().all()
    
    return tasks

async def read_task(
    task_id: int,
    db: AsyncSession 
) -> schemas.TaskRead:
    """
    Получение задачи.
    
    Аргументы:
        task_id (int): Идентификатор задачи.
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Task).filter_by(id=task_id))
    task = result.scalar_one_or_none()
    
    return task

async def update_task(
    task: schemas.TaskUpdate,
    db: AsyncSession 
) -> schemas.TaskRead:
    """
    Обновление задачи.
    
    Аргументы:
        task (TaskUpdate): Модель для обновления задачи.
        db (AsyncSession): Сессия базы данных.
    """
    
    existing_task = await db.get(models.Task, task.id)
    existing_task.column_id = task.column_id
    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.date_end = task.date_end
    existing_task.status_id = task.status_id
    existing_task.priority_id = task.priority_id
    
    result = await db.execute(select(models.TaskLabel).filter_by(task_id=task.id))
    existing_label_ids = {label.label_id for label in result.scalars().all()}
    new_label_ids = set(task.labels_id)
    
    for label_id in new_label_ids - existing_label_ids:
        db.add(models.TaskLabel(label_id=label_id, task_id=task.id))
    
    for label_id in existing_label_ids - new_label_ids:
        result = await db.execute(select(models.TaskLabel).filter_by(task_id=task.id, label_id=label_id))
        label = result.scalar_one_or_none()
        if label:
            db.delete(label)
    
    await db.commit()
    await db.refresh(existing_task)
    
    return existing_task

async def delete_task(
    task: schemas.TaskDelete,
    db: AsyncSession 
) -> schemas.TaskRead:
    """
    Удаление задачи.
    
    Аргументы:
        task_id (int): Идентификатор задачи.
        db (AsyncSession): Сессия базы данных.
    """
    
    task = await db.get(models.Task, task.id)
    db.delete(task)
    
    await db.commit()
    
    return task

# Priority
async def create_priority(
    priority: schemas.PriorityCreate,
    db: AsyncSession 
) -> schemas.PriorityRead:
    """
    Создание приоритета.
    
    Аргументы:
        priority (PriorityCreate): Модель для создания приоритета.
        db (AsyncSession): Сессия базы данных.
    """
    
    new_priority = models.Priority(name=priority.name)
    db.add(new_priority)
    
    await db.commit()
    await db.refresh(new_priority)
    
    return new_priority

async def read_priorities(
    db: AsyncSession
) -> list[schemas.PriorityRead]:
    """
    Получение списка приоритетов.
    
    Аргументы:
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Priority))
    priorities = result.scalars().all()
    
    return priorities

async def read_priority(
    priority_id: int,
    db: AsyncSession 
) -> schemas.PriorityRead:
    """
    Получение приоритета.
    
    Аргументы:
        priority_id (int): Идентификатор приоритета.
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Priority).filter_by(id=priority_id))
    priority = result.scalar_one_or_none()
    
    return priority

# Status
async def create_status(
    status: schemas.StatusCreate,
    db: AsyncSession 
) -> schemas.StatusRead:
    """
    Создание статуса.
    
    Аргументы:
        status (StatusCreate): Модель для создания статуса.
        db (AsyncSession): Сессия базы данных.
    """
    
    new_status = models.Status(name=status.name)
    db.add(new_status)
    
    await db.commit()
    await db.refresh(new_status)
    
    return new_status

async def read_statuses(
    db: AsyncSession
) -> list[schemas.StatusRead]:
    """
    Получение списка статусов.
    
    Аргументы:
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Status))
    statuses = result.scalars().all()
    
    return statuses

async def read_status(
    status_id: int,
    db: AsyncSession 
) -> schemas.StatusRead:
    """
    Получение статуса.
    
    Аргументы:
        status_id (int): Идентификатор статуса.
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Status).filter_by(id=status_id))
    status = result.scalar_one_or_none()
    
    return status

# Label
async def create_label(
    label: schemas.LabelCreate,
    db: AsyncSession 
) -> schemas.LabelRead:
    """
    Создание метки.
    
    Аргументы:
        label (LabelCreate): Модель для создания метки.
        db (AsyncSession): Сессия базы данных.
    """
    
    new_label = models.Label(name=label.name)
    db.add(new_label)
    
    await db.commit()
    await db.refresh(new_label)
    
    return new_label

async def read_labels(
    db: AsyncSession
) -> list[schemas.LabelRead]:
    """
    Получение списка меток.
    
    Аргументы:
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Label))
    labels = result.scalars().all()
    
    return labels

async def read_label(
    label_id: int,
    db: AsyncSession 
) -> schemas.LabelRead:
    """
    Получение метки.
    
    Аргументы:
        label_id (int): Идентификатор метки.
        db (AsyncSession): Сессия базы данных.
    """
    
    result = await db.execute(select(models.Label).filter_by(id=label_id))
    label = result.scalar_one_or_none()
    
    return label

async def update_label(
    label: schemas.LabelUpdate,
    db: AsyncSession 
) -> schemas.LabelRead:
    """
    Обновление метки.
    
    Аргументы:
        label (LabelUpdate): Модель для обновления метки.
        db (AsyncSession): Сессия базы данных.
    """
    
    existing_label = await db.get(models.Label, label.id)
    existing_label.name = label.name
    
    await db.commit()
    await db.refresh(existing_label)
    
    return existing_label

async def delete_label(
    label: schemas.LabelDelete,
    db: AsyncSession 
) -> schemas.LabelRead:
    """
    Удаление метки.
    
    Аргументы:
        label (LabelDelete): Идентификатор метки.
        db (AsyncSession): Сессия базы данных.
    """
    
    label = await db.get(models.Label, label.id)
    db.delete(label)
    
    await db.commit()
    
    return label

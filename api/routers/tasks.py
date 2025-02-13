from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.setup import get_db
from fastapi import HTTPException, status
import api.schemas.tasks as schemas
import api.repositories.tasks as repositories


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


# Роуты для работы с пространствами
@router.post(
    "/space",
    response_model=schemas.SpaceRead,
    responses={
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при создании пространства"}
    }
)
async def create_space(
    space: schemas.SpaceCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.SpaceRead:
    """Создание пространства"""
    
    try:
        space = await repositories.create_space(space, db)
        return space
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при создании пространства: {str(e)}"
        )

@router.get(
    "/spaces", 
    response_model=list[schemas.SpaceRead], 
    responses={
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при получении пространств"}
    }
)
async def read_spaces(
    db: AsyncSession = Depends(get_db)
) -> list[schemas.SpaceRead]:
    """Получение списка пространств"""
    
    try:
        spaces = await repositories.read_spaces(db)
        return spaces
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при получении пространств: {str(e)}"
        )


@router.get(
    "/space/{space_id}", 
    response_model=schemas.SpaceRead, 
    responses={
        404: {"description": "Пространство с указанным ID не найдено"},
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при получении пространства"}
    }
)
async def read_space(
    space_id: int, 
    db: AsyncSession = Depends(get_db)
) -> schemas.SpaceRead:
    """Получение пространства по ID"""
    
    try:
        space = await repositories.read_space(space_id, db)
        if not space:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пространство с ID {space_id} не найдено"
            )
        return space
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при получении пространства с ID {space_id}: {str(e)}"
        )
        
@router.put(
    "/space",
    response_model=schemas.SpaceRead,
    responses={
        404: {"description": "Пространство с указанным ID не найдено"},
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при обновлении пространства"}
    }
)
async def update_space(
    space: schemas.SpaceUpdate,
    db: AsyncSession = Depends(get_db)
) -> schemas.SpaceRead:
    """Обновление пространства"""
    
    try:
        space = await repositories.update_space(space, db)
        if not space:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пространство с ID {space.id} не найдено"
            )
        return space
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при обновлении пространства с ID {space.id}: {str(e)}"
        )
        
@router.delete(
    "/space",
    response_model=schemas.SpaceRead,
    responses={
        404: {"description": "Пространство с указанным ID не найдено"},
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при удалении пространства"}
    }
)
async def delete_space(
    space: schemas.SpaceDelete,
    db: AsyncSession = Depends(get_db)
) -> schemas.SpaceRead:
    """Удаление пространства"""
    
    try:
        space = await repositories.delete_space(space, db)
        if not space:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пространство с ID {space.id} не найдено"
            )
        return space
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при удалении пространства с ID {space.id}: {str(e)}"
        )

# Роуты для работы с колонками
@router.post(
    "/column",
    response_model=schemas.ColumnRead,
    responses={
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при создании колонки"}
    }
)
async def create_column(
    column: schemas.ColumnCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.ColumnRead:
    """Создание колонки"""
    
    try:
        column = await repositories.create_column(column, db)
        return column
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при создании колонки: {str(e)}"
        )

@router.get(
    "/columns",
    response_model=list[schemas.ColumnRead],
    responses={
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при получении колонок"}
    }
)
async def read_columns(
    db: AsyncSession = Depends(get_db)
) -> list[schemas.ColumnRead]:
    """Получение списка колонок"""
    
    try:
        columns = await repositories.read_columns(db)
        return columns
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при получении колонок: {str(e)}"
        )

# Роуты для работы с задачами
@router.post(
    "/task",
    response_model=schemas.TaskRead,
    responses={
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при создании задачи"}
    }
)
async def create_task(
    task: schemas.TaskCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.TaskRead:
    """Создание задачи"""
    
    try:
        task = await repositories.create_task(task, db)
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при создании задачи: {str(e)}"
        )
        
@router.get(
    "/tasks",
    response_model=list[schemas.TaskRead],
    responses={
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при получении задач"}
    }
)
async def read_tasks(
    db: AsyncSession = Depends(get_db)
) -> list[schemas.TaskRead]:
    """Получение списка задач"""
    
    try:
        tasks = await repositories.read_tasks(db)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при получении задач: {str(e)}"
        )
        
@router.get(
    "/task/{task_id}",
    response_model=schemas.TaskRead,
    responses={
        404: {"description": "Задача с указанным ID не найдена"},
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при получении задачи"}
    }
)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.TaskRead:
    """Получение задачи по ID"""
    
    try:
        task = await repositories.read_task(task_id, db)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с ID {task_id} не найдена"
            )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при получении задачи с ID {task_id}: {str(e)}"
        )
        
@router.put(
    "/task",
    response_model=schemas.TaskRead,
    responses={
        404: {"description": "Задача с указанным ID не найдена"},
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при обновлении задачи"}
    }
)
async def update_task(
    task: schemas.TaskUpdate,
    db: AsyncSession = Depends(get_db)
) -> schemas.TaskRead:
    """Обновление задачи"""
    
    try:
        task = await repositories.update_task(task, db)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с ID {task.id} не найдена"
            )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при обновлении задачи с ID {task.id}: {str(e)}"
        )
        
@router.delete(
    "/task",
    response_model=schemas.TaskRead,
    responses={
        404: {"description": "Задача с указанным ID не найдена"},
        422: {"description": "Ошибка валидации запроса"},
        500: {"description": "Произошла ошибка при удалении задачи"}
    }
)
async def delete_task(
    task: schemas.TaskDelete,
    db: AsyncSession = Depends(get_db)
) -> schemas.TaskRead:
    """Удаление задачи"""
    
    try:
        task = await repositories.delete_task(task, db)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с ID {task.id} не найдена"
            )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при удалении задачи с ID {task.id}: {str(e)}"
        )
        

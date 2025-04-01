from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.core.security import get_current_user
from api.core.logging import Logger
from api.errors.exceptions import NotFoundException, \
                                  InternalServerErrorException
from api.repositories.tasks import SpacesDAO
import api.models.users as models
import api.schemas.tasks as schemas


logger = Logger()

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# Роуты для работы с пространствами
@router.post(
    "/space",
    summary="Создание пространства пользователем",
    response_model=schemas.SpaceRead
)
async def create_space(
    space: schemas.SpaceCreate,
    user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.SpaceRead:
    """Создание пространства"""
    
    try:
        new_space = await SpacesDAO.add(
            users_id=space.users_id, 
            name=space.name, 
            owner_id=user.id
        )
        
        logger.info(
            func=create_space, 
            parameters={
                'space': repr(space),
                'user': user.login
            }, 
            result=new_space
        )
        
        return new_space
    except Exception as e:
        logger.error(
            func=create_space, 
            parameters={
                'space': repr(space),
                'user': user.login
            }, 
            message=str(e)
        )
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании пространства"
        )

@router.get(
    "/spaces/user", 
    summary="Получение списка пространств пользователя",
    response_model=list[schemas.SpaceRead]
)
async def read_spaces_by_user(
    user: Annotated[models.User, Depends(get_current_user)]
) -> list[schemas.SpaceRead]:
    """Получение списка пространств"""
    
    try:
        spaces = await SpacesDAO.find_all(user_id=user.id)
        
        logger.info(
            func=read_spaces_by_user,
            parameters={
                'user': user.login
            },
            result=repr(spaces)
        )
        
        return spaces
    except Exception as e:
        logger.error(
            func=read_spaces_by_user,
            parameters={
                'user': user.login
            },
            message=str(e)
        )
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении пространств: {str(e)}"
        )

@router.get(
    "/space/user",
    summary="Получение пространства пользователя по ID",
    response_model=schemas.SpaceRead
)
async def read_space_by_user_and_id(
    space_id: int,
    user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.SpaceRead:
    """Получение пространства по ID"""
    
    try:
        space = await SpacesDAO.find_one_or_none(user_id=user.id, id=space_id)
        
        if not space:
            logger.error(
                func=read_space_by_user_and_id,
                parameters={
                    'space_id': space_id,
                    'user': user.login
                },
                message=f"Пространство с ID {space_id} не найдено"
            )
            raise NotFoundException(
                detail=f"Пространство с ID {space_id} не найдено"
            ) 
            
        logger.info(
            func=read_space_by_user_and_id,
            parameters={
                'space_id': space_id,
                'user': user.login
            },
            result=repr(space)
        )
        
        return space
    except Exception as e:
        logger.error(
            func=read_space_by_user_and_id,
            parameters={
                'space_id': space_id,
                'user': user.login
            },
            message=str(e)
        )
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении пространства с ID {space_id}: {str(e)}"
        )
        
@router.put(
    "/space",
    summary="Изменение пространства",
    response_model=schemas.SpaceUpdate
)
async def update_space(
    space: schemas.SpaceUpdate,
    user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.SpaceRead:
    """Обновление пространства"""
    
    try:
        existing_space = await SpacesDAO.update(users_id=space.users_id, where={'id': space.id}, name=space.name)
        
        if not space:
            logger.error(
                func=update_space,
                parameters={
                    'space': repr(space),
                    'user': user.login
                },
                message=f"Пространство с ID {space.id} не найдено"
            )
            raise NotFoundException(
                detail=f"Пространство с ID {space.id} не найдено"
            )
            
        logger.info(
            func=update_space,
            parameters={
                'space': repr(space),
                'user': user.login
            },
            result=repr(existing_space)
        )
        
        return existing_space
    except Exception as e:
        logger.error(
            func=update_space,
            parameters={
                'space': repr(space),
                'user': user.login
            },
            message=str(e)
        )
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при обновлении пространства с ID {space.id}: {str(e)}"
        )
        
@router.delete(
    "/space",
    summary="Удаление пространства",
    response_class=JSONResponse
)
async def delete_space(
    space_id: int,
    user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.SpaceRead:
    """Удаление пространства"""
    
    try:
        count = await SpacesDAO.delete(id=space_id)
        
        if not count:
            logger.error(
                func=delete_space,
                parameters={
                    'space_id': space_id,
                    'user': user.login
                },
                message=f"Пространство с ID {space_id} не найдено"
            )
            raise NotFoundException(
                detail=f"Пространство с ID {space_id} не найдено"
            )
        
        logger.info(
            func=delete_space,
            parameters={
                'space_id': space_id,
                'user': user.login
            },
            result=count
        )
            
        return JSONResponse(content={"message": "Пространство успешно удалено"})
    except Exception as e:
        logger.error(
            func=delete_space,
            parameters={
                'space_id': space_id,
                'user': user.login
            },
            message=str(e)
        )
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении пространства с ID {space_id}: {str(e)}"
        )

# Роуты для работы с колонками
# @router.post(
#     "/column",
#     response_model=schemas.ColumnRead,
#     responses={
#         422: {"description": "Ошибка валидации запроса"},
#         500: {"description": "Произошла ошибка при создании колонки"}
#     }
# )
# async def create_column(
#     column: schemas.ColumnCreate,
#     db: AsyncSession = Depends(get_db)
# ) -> schemas.ColumnRead:
#     """Создание колонки"""
    
#     try:
#         column = await repositories.create_column(column, db)
#         return column
#     except Exception as e:
#         raise InternalServerErrorException(
#             detail=f"Произошла ошибка при создании колонки: {str(e)}"
#         )

# @router.get(
#     "/columns",
#     response_model=list[schemas.ColumnRead],
#     responses={
#         422: {"description": "Ошибка валидации запроса"},
#         500: {"description": "Произошла ошибка при получении колонок"}
#     }
# )
# async def read_columns(
#     db: AsyncSession = Depends(get_db)
# ) -> list[schemas.ColumnRead]:
#     """Получение списка колонок"""
    
#     try:
#         columns = await repositories.read_columns(db)
#         return columns
#     except Exception as e:
#         raise InternalServerErrorException(
#             detail=f"Произошла ошибка при получении колонок: {str(e)}"
#         )

# # Роуты для работы с задачами
# @router.post(
#     "/task",
#     response_model=schemas.TaskRead,
#     responses={
#         422: {"description": "Ошибка валидации запроса"},
#         500: {"description": "Произошла ошибка при создании задачи"}
#     }
# )
# async def create_task(
#     task: schemas.TaskCreate,
#     db: AsyncSession = Depends(get_db)
# ) -> schemas.TaskRead:
#     """Создание задачи"""
    
#     try:
#         task = await repositories.create_task(task, db)
#         return task
#     except Exception as e:
#         raise InternalServerErrorException(
#             detail=f"Произошла ошибка при создании задачи: {str(e)}"
#         )
        
# @router.get(
#     "/tasks",
#     response_model=list[schemas.TaskRead],
#     responses={
#         422: {"description": "Ошибка валидации запроса"},
#         500: {"description": "Произошла ошибка при получении задач"}
#     }
# )
# async def read_tasks(
#     db: AsyncSession = Depends(get_db)
# ) -> list[schemas.TaskRead]:
#     """Получение списка задач"""
    
#     try:
#         tasks = await repositories.read_tasks(db)
#         return tasks
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Произошла ошибка при получении задач: {str(e)}"
#         )
        
# @router.get(
#     "/task/{task_id}",
#     response_model=schemas.TaskRead,
#     responses={
#         404: {"description": "Задача с указанным ID не найдена"},
#         422: {"description": "Ошибка валидации запроса"},
#         500: {"description": "Произошла ошибка при получении задачи"}
#     }
# )
# async def read_task(
#     task_id: int,
#     db: AsyncSession = Depends(get_db)
# ) -> schemas.TaskRead:
#     """Получение задачи по ID"""
    
#     try:
#         task = await repositories.read_task(task_id, db)
#         if not task:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Задача с ID {task_id} не найдена"
#             )
#         return task
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Произошла ошибка при получении задачи с ID {task_id}: {str(e)}"
#         )
        
# @router.put(
#     "/task",
#     response_model=schemas.TaskRead,
#     responses={
#         404: {"description": "Задача с указанным ID не найдена"},
#         422: {"description": "Ошибка валидации запроса"},
#         500: {"description": "Произошла ошибка при обновлении задачи"}
#     }
# )
# async def update_task(
#     task: schemas.TaskUpdate,
#     db: AsyncSession = Depends(get_db)
# ) -> schemas.TaskRead:
#     """Обновление задачи"""
    
#     try:
#         task = await repositories.update_task(task, db)
#         if not task:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Задача с ID {task.id} не найдена"
#             )
#         return task
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Произошла ошибка при обновлении задачи с ID {task.id}: {str(e)}"
#         )
        
# @router.delete(
#     "/task",
#     response_model=schemas.TaskRead,
#     responses={
#         404: {"description": "Задача с указанным ID не найдена"},
#         422: {"description": "Ошибка валидации запроса"},
#         500: {"description": "Произошла ошибка при удалении задачи"}
#     }
# )
# async def delete_task(
#     task: schemas.TaskDelete,
#     db: AsyncSession = Depends(get_db)
# ) -> schemas.TaskRead:
#     """Удаление задачи"""
    
#     try:
#         task = await repositories.delete_task(task, db)
#         if not task:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Задача с ID {task.id} не найдена"
#             )
#         return task
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Произошла ошибка при удалении задачи с ID {task.id}: {str(e)}"
#         )


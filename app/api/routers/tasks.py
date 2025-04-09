from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.core.security import User, get_current_user
from api.core.exceptions import NotFoundException, \
                                InternalServerErrorException
import api.repositories.tasks as repositories
import api.schemas.tasks as schemas


router = APIRouter(
    tags=["Tasks"]
)


# Роуты для работы с досками
@router.post(
    "/boards",
    summary="Создание доски",
    response_model=schemas.BoardRead
)
async def create_board(
    board: schemas.BoardCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.BoardRead:
    """Создание доски"""
    
    try:
        new_board = await repositories.BoardDAO.add(
            name=board.name, 
            owner_id=user.id
        )
        
        return new_board
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании доски"
        )

@router.get(
    "/boards", 
    summary="Получение списка досок пользователя",
    response_model=list[schemas.BoardRead]
)
async def read_boards_by_user(
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.BoardRead]:
    """Получение списка досок"""
    
    try:
        boards = await repositories.BoardDAO.find_all(owner_id=user.id)
        
        return boards
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении досок: {str(e)}"
        )
        
@router.put(
    "/boards",
    summary="Изменение доски",
    response_model=schemas.BoardRead
)
async def update_board(
    board: schemas.BoardUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.BoardRead:
    """Обновление пространства"""
    
    try:
        existing_board = await repositories.BoardDAO.update(
            where={'id': board.id}, 
            name=board.name
        )
        
        if not existing_board:
            raise NotFoundException
        
        return existing_board
    except NotFoundException:
        raise NotFoundException(
            detail=f"Пространство с ID {board.id} не найдено"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при обновлении доски с ID {board.id}: {str(e)}"
        )
        
@router.delete(
    "/boards",
    summary="Удаление доски",
    response_class=JSONResponse
)
async def delete_board(
    board_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> JSONResponse:
    """Удаление пространства"""
    
    try:
        count = await repositories.BoardDAO.delete(id=board_id)
        
        if not count:
            raise NotFoundException
            
        return JSONResponse(content={"message": "Пространство успешно удалено"})
    except NotFoundException:
        raise NotFoundException(
            detail=f"Пространство с ID {board_id} не найдено"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении доски с ID {board_id}: {str(e)}"
        )

# Роуты для работы со стопками
@router.post(
    "/stacks",
    summary="Создание стопки",
    response_model=schemas.StackRead
)
async def create_stack(
    stack: schemas.StackCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.StackRead:
    """Создание стопки"""
    
    try:
        new_stack = await repositories.StackDAO.add(
            board_id=stack.board_id, 
            name=stack.name
        )
        
        return new_stack
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании колонки: {str(e)}"
        )

@router.get(
    "/stacks",
    summary="Получение списка стопок задач по доске",
    response_model=list[schemas.StackRead],
)
async def read_stacks_by_board_id(
    board_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.StackRead]:
    """Получение списка стопок"""
    
    try:
        stacks = await repositories.StackDAO.find_all(board_id=board_id)
        
        return stacks
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении стопок: {str(e)}"
        )
        
@router.put(
    "/stacks",
    summary="Изменение стопки",
    response_model=schemas.StackRead
)
async def update_stack(
    stack: schemas.StackUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.StackRead:
    """Обновление колонки"""
    
    try:
        existing_stack = await repositories.StackDAO.update(
            where={'id': stack.id}, 
            name=stack.name, 
            board_id=stack.board_id
        )
        
        if not existing_stack:
            raise NotFoundException
        
        return existing_stack
    except NotFoundException:
        raise NotFoundException(
            detail=f"Стопка с ID {stack.id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при обновлении стопки с ID {stack.id}: {str(e)}"
        )
        
@router.delete(
    "/stacks",
    summary="Удаление стопки",
    response_class=JSONResponse
)
async def delete_stack(
    stack_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> JSONResponse:
    """Удаление колонки"""
    
    try:
        count = await repositories.StackDAO.delete(id=stack_id)
        
        if not count:
            raise NotFoundException
        
        return JSONResponse(content={"message": "Стопка успешно удалена"})
    except NotFoundException:
        raise NotFoundException(
            detail=f"Стопка с ID {stack_id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении стопки с ID {stack_id}: {str(e)}"
        )

# Роуты для работы с приоритетами
@router.get(
    "/priorities",
    summary="Получение списка приоритетов",
    response_model=list[schemas.PriorityRead]
)
async def read_priorities(
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.PriorityRead]:
    """Получение списка приоритетов"""
    
    try:
        priorities = await repositories.PriorityDAO.find_all()
        
        return priorities
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении приоритетов: {str(e)}"
        )

# Роуты для работы с метками
@router.post(
    "/tags",
    summary="Создание метки",
    response_model=schemas.TagRead
)
async def create_tag(
    tag: schemas.TagCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.TagRead:
    """Создание метки"""
    
    try:
        new_tag = await repositories.TagDAO.add(name=tag.name)
        
        return new_tag
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании метки: {str(e)}"
        )
        
@router.get(
    "/tags",
    summary="Получение списка меток доски",
    response_model=list[schemas.TagRead]
)
async def read_tags_by_board_id(
    board_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.TagRead]:
    """Получение списка меток"""
        
    try:
        tags = await repositories.TagDAO.find_all()
        
        return tags
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении меток: {str(e)}"
        )

@router.put(
    "/tags",
    summary="Изменение метки",
    response_model=schemas.TagRead
)
async def update_tag(
    tag: schemas.TagUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.TagRead:
    """Обновление метки"""
    
    try:
        existing_tag = await repositories.TagDAO.update(
            where={'id': tag.id}, 
            name=tag.name,
            board_id=tag.board_id
        )
        
        if not existing_tag:
            raise NotFoundException
        
        return existing_tag
    except NotFoundException:
        raise NotFoundException(
            detail=f"Метка с ID {tag.id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при обновлении метки с ID {tag.id}: {str(e)}"
        )

@router.delete(
    "/tags",
    summary="Удаление метки",
    response_class=JSONResponse
)
async def delete_tag(
    tag_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> JSONResponse:
    """Удаление метки"""
    
    try:
        count = await repositories.TagDAO.delete(id=tag_id)
        
        if not count:
            raise NotFoundException
        
        return JSONResponse(content={"message": "Метка успешно удалена"})
    except NotFoundException:
        raise NotFoundException(
            detail=f"Метка с ID {tag_id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении метки с ID {tag_id}: {str(e)}"
        ) 
 
# Роуты для работы с задачами
@router.post(
    "/tasks",
    summary="Создание задачи",
    response_model=schemas.TaskRead
)
async def create_task(
    task: schemas.TaskCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.TaskRead:
    """Создание задачи"""
    
    try:
        task = await repositories.TaskDAO.add(
            tags_id=task.tags_id,
            stack_id=task.stack_id, 
            title=task.title,
            priority_id=task.priority_id,
            create_date=task.create_date,
            date_end=task.date_end
        )
        
        return task
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании задачи: {str(e)}"
        )
        
@router.get(
    "/tasks",
    summary="Получение задачи по ID",
    response_model=schemas.TaskRead
)
async def read_task_by_id(
    task_id: int,
    user: Annotated[User, Depends(get_current_user)],
) -> schemas.TaskRead:
    """Получение задачи по ID"""
    
    try:
        task = await repositories.TaskDAO.find_one_or_none(id=task_id)
        
        if not task:
            raise NotFoundException(
                detail=f"Задача с ID {task_id} не найдена"
            )
        
        return task
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении задачи с ID {task_id}: {str(e)}"
        )
        
@router.put(
    "/tasks",
    summary="Изменение задачи",
    response_model=schemas.TaskRead
)
async def update_task(
    task: schemas.TaskUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.TaskRead:
    """Обновление задачи"""
        
    try:
        existing_task = await repositories.TaskDAO.update(
            tags_id=task.tags_id,
            where={'id': task.id}, 
            title=task.title,
            stack_id=task.stack_id,
            create_date=task.create_date,
            date_end=task.date_end,
            priority_id=task.priority_id,
            description=task.description,
            solution=task.solution,
            archived=task.archived
        )
        
        if not existing_task:
            raise NotFoundException
        
        return existing_task
    except NotFoundException:
        raise NotFoundException(
            detail=f"Задача с ID {task.id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при обновлении задачи с ID {task.id}: {str(e)}"
        )
        
@router.delete(
    "/tasks",
    summary="Удаление задачи",
    response_model=schemas.TaskRead
)
async def delete_task(
    task_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.TaskRead:
    """Удаление задачи"""
    
    try:
        count = await repositories.TaskDAO.delete(id=task_id)
        
        if not count:
            raise NotFoundException
        
        return JSONResponse(content={"message": "Задача успешно удалена"})
    except NotFoundException:
        raise NotFoundException(
            detail=f"Задача с ID {task_id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении задачи с ID {task_id}: {str(e)}"
        )

@router.post(
    "/task_cards",
    summary="Создание карточки задачи",
    response_model=schemas.TaskCardRead
)
async def create_task_card(
    task_card: schemas.TaskCardCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.TaskCardRead:
    """Создание карточки задачи"""
    
    try:
        task = await repositories.TaskDAO.add(
            stack_id=task_card.stack_id,
            title=task_card.title
        )
        
        return task
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании задачи: {str(e)}"
        )
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.core.security import get_current_user
from api.core.exceptions import NotFoundException, \
                                  InternalServerErrorException
from api.models.users import User
import api.repositories.tasks as repositories
import api.schemas.tasks as schemas


router = APIRouter(
    tags=["Tasks"]
)


# Роуты для работы с пространствами
@router.post(
    "/space",
    summary="Создание пространства пользователем",
    response_model=schemas.Space
)
async def create_space(
    space: schemas.SpaceCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Space:
    """Создание пространства"""
    
    try:
        new_space = await repositories.SpaceDAO.add(
            users_id=space.users_id, 
            name=space.name, 
            owner_id=user.id
        )
        
        return new_space
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании пространства"
        )

@router.get(
    "/spaces", 
    summary="Получение списка пространств пользователя",
    response_model=list[schemas.Space]
)
async def read_spaces_by_user(
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.Space]:
    """Получение списка пространств"""
    
    try:
        spaces = await repositories.SpaceDAO.find_all(user_id=user.id)
        
        return spaces
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении пространств: {str(e)}"
        )

@router.get(
    "/space",
    summary="Получение пространства пользователя по ID",
    response_model=schemas.Space
)
async def read_space_by_user_and_id(
    space_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Space:
    """Получение пространства по ID"""
    
    try:
        space = await repositories.SpaceDAO.find_one_or_none(id=space_id)
        
        if not space:
            raise NotFoundException
        
        return space
    except NotFoundException:
        raise NotFoundException(
            detail=f"Пространство с ID {space_id} не найдено"
        ) 
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении пространства с ID {space_id}: {str(e)}"
        )
        
@router.put(
    "/space",
    summary="Изменение пространства",
    response_model=schemas.Space
)
async def update_space(
    space: schemas.SpaceUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Space:
    """Обновление пространства"""
    
    try:
        existing_space = await repositories.SpaceDAO.update(
            users_id=space.users_id, 
            where={'id': space.id}, 
            name=space.name
        )
        
        if not existing_space:
            raise NotFoundException
        
        return existing_space
    except NotFoundException:
        raise NotFoundException(
            detail=f"Пространство с ID {space.id} не найдено"
        )
    except Exception as e:
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
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Space:
    """Удаление пространства"""
    
    try:
        count = await repositories.SpaceDAO.delete(id=space_id)
        
        if not count:
            raise NotFoundException
            
        return JSONResponse(content={"message": "Пространство успешно удалено"})
    except NotFoundException:
        raise NotFoundException(
            detail=f"Пространство с ID {space_id} не найдено"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении пространства с ID {space_id}: {str(e)}"
        )

# Роуты для работы со стопками
@router.post(
    "/stack",
    summary="Создание стопки",
    response_model=schemas.Stack
)
async def create_stack(
    stack: schemas.StackCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Stack:
    """Создание стопки"""
    
    try:
        new_stack = await repositories.StackDAO.add(
            space_id=stack.space_id, 
            name=stack.name
        )
        
        return new_stack
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании колонки: {str(e)}"
        )

@router.get(
    "/stacks",
    summary="Получение списка стопок пространства",
    response_model=list[schemas.Stack],
)
async def read_stacks_by_space_id(
    space_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.Stack]:
    """Получение списка колонок"""
    
    try:
        stacks = await repositories.StackDAO.find_all(space_id=space_id)
        
        return stacks
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении колонок: {str(e)}"
        )
        
@router.get(
    "/stack",
    summary="Получение стопки по ID",
    response_model=schemas.Stack
)
async def read_stack_by_id(
    stack_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Stack:
    """Получение колонки по ID"""
    
    try:
        stack = await repositories.StackDAO.find_one_or_none(id=stack_id)
        
        if not stack:
            raise NotFoundException
        
        return stack
    except NotFoundException:
        raise NotFoundException(
            detail=f"Стопка с ID {stack_id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении стопки с ID {stack_id}: {str(e)}"
        )
        
@router.put(
    "/stack",
    summary="Изменение стопки",
    response_model=schemas.Stack
)
async def update_stack(
    stack: schemas.StackUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Stack:
    """Обновление колонки"""
    
    try:
        existing_stack = await repositories.StackDAO.update(
            where={'id': stack.id}, 
            name=stack.name, 
            space_id=stack.space_id
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
    "/stack",
    summary="Удаление стопки",
    response_class=JSONResponse
)
async def delete_stack(
    stack_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Stack:
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
    response_model=list[schemas.Priority]
)
async def read_priorities(
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.Priority]:
    """Получение списка приоритетов"""
    
    try:
        priorities = await repositories.PriorityDAO.find_all()
        
        return priorities
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении приоритетов: {str(e)}"
        )

@router.post(
    "/priority",
    summary="Создание приоритета",
    response_model=schemas.Priority
)
async def create_priority(
    priority: schemas.PriorityCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Priority:
    """Создание приоритета"""
    
    try:
        new_priority = await repositories.PriorityDAO.add(name=priority.name)
        
        return new_priority
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании приоритета: {str(e)}"
        )
        
# Роуты для работы со статусами
@router.get(
    "/statuses",
    summary="Получение списка статусов",
    response_model=list[schemas.Status]
)
async def read_statuses(
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.Status]:
    """Получение списка статусов"""
    
    try:
        statuses = await repositories.StatusDAO.find_all()
        
        return statuses
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении статусов: {str(e)}"
        )
        
@router.post(
    "/status",
    summary="Создание статуса",
    response_model=schemas.Status
)
async def create_status(
    status: schemas.StatusCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Status:
    """Создание статуса"""
        
    try:
        new_status = await repositories.StatusDAO.add(name=status.name)
        
        return new_status
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании статуса: {str(e)}"
        )

# Роуты для работы с метками
@router.get(
    "/labels",
    summary="Получение списка меток",
    response_model=list[schemas.Label]
)
async def read_labels(
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.Label]:
    """Получение списка меток"""
        
    try:
        labels = await repositories.LabelDAO.find_all()
        
        return labels
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении меток: {str(e)}"
        )

@router.post(
    "/label",
    summary="Создание метки",
    response_model=schemas.Label
)
async def create_label(
    label: schemas.LabelCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Label:
    """Создание метки"""
    
    try:
        new_label = await repositories.LabelDAO.add(name=label.name)
        
        return new_label
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании метки: {str(e)}"
        )

@router.put(
    "/label",
    summary="Изменение метки",
    response_model=schemas.Label
)
async def update_label(
    label: schemas.LabelUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Label:
    """Обновление метки"""
    
    try:
        existing_label = await repositories.LabelDAO.update(
            where={'id': label.id}, 
            name=label.name
        )
        
        if not existing_label:
            raise NotFoundException
        
        return existing_label
    except NotFoundException:
        raise NotFoundException(
            detail=f"Метка с ID {label.id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при обновлении метки с ID {label.id}: {str(e)}"
        )

@router.delete(
    "/label",
    summary="Удаление метки",
    response_class=JSONResponse
)
async def delete_label(
    label_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Label:
    """Удаление метки"""
    
    try:
        count = await repositories.LabelDAO.delete(id=label_id)
        
        if not count:
            raise NotFoundException
        
        return JSONResponse(content={"message": "Метка успешно удалена"})
    except NotFoundException:
        raise NotFoundException(
            detail=f"Метка с ID {label_id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении метки с ID {label_id}: {str(e)}"
        ) 
 
# Роуты для работы с задачами
@router.post(
    "/task",
    response_model=schemas.Task
)
async def create_task(
    task: schemas.TaskCreate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Task:
    """Создание задачи"""
    
    try:
        task = await repositories.TaskDAO.add(
            labels_id=task.labels_id,
            stack_id=task.stack_id, 
            author_id=user.id,
            title=task.title,
            description=task.description,
            create_date=task.create_date,
            date_end=task.date_end,
            priority_id=task.priority_id,
            status_id=task.status_id
        )
        
        return task
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при создании задачи: {str(e)}"
        )
        
@router.get(
    "/tasks",
    summary="Получение списка задач по стопке",
    response_model=list[schemas.Task],
)
async def read_tasks(
    stack_id: int,
    user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.Task]:
    """Получение списка задач"""
    
    try:
        tasks = await repositories.TaskDAO.find_all(stack_id=stack_id)
        
        return tasks
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при получении задач: {str(e)}"
        )
        
@router.get(
    "/task",
    summary="Получение задачи по ID",
    response_model=schemas.Task
)
async def read_task(
    task_id: int,
    user: Annotated[User, Depends(get_current_user)],
) -> schemas.Task:
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
    "/task",
    summary="Изменение задачи",
    response_model=schemas.Task
)
async def update_task(
    task: schemas.TaskUpdate,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Task:
    """Обновление задачи"""
        
    try:
        existing_task = await repositories.TaskDAO.update(
            labels_id=task.labels_id,
            where={'id': task.id}, 
            title=task.title,
            description=task.description,
            stack_id=task.stack_id,
            create_date=task.create_date,
            date_end=task.date_end,
            priority_id=task.priority_id,
            status_id=task.status_id
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
    "/task",
    response_model=schemas.Task
)
async def delete_task(
    task: schemas.TaskDelete,
    user: Annotated[User, Depends(get_current_user)]
) -> schemas.Task:
    """Удаление задачи"""
    
    try:
        count = await repositories.TaskDAO.delete(id=task.id)
        
        if not count:
            raise NotFoundException
        
        return JSONResponse(content={"message": "Задача успешно удалена"})
    except NotFoundException:
        raise NotFoundException(
            detail=f"Задача с ID {task.id} не найдена"
        )
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Произошла ошибка при удалении задачи с ID {task.id}: {str(e)}"
        )

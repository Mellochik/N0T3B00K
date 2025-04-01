import datetime
import functools
import logging
from typing import Any, Callable, TypeVar


DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])


class Log:
    logger = logging.getLogger('uvicorn')
    
    def info(self, func: str, parameters: dict, result: str) -> None:
        self.logger.info(f"{datetime.datetime.now()} - {func}("
                         f"{', '.join([f'{key}={value}' for key, value in parameters.items()])}"
                         f") -> {result}")
    
    def error(self, func: str, parameters: dict, message: str) -> None:
        self.logger.error(f"{datetime.datetime.now()} - {func}("
                          f"{', '.join([f'{key}={value}' for key, value in parameters.items()])}"
                          f") -> {message}")
    
    def log_dao_method(self, dao_method: Callable) -> DecoratedCallable:
        """Обертка для логгирования методов DAO."""
        
        @functools.wraps(dao_method)
        async def wrapper(*args, **kwargs):
            dao_class = args[0]
            try:
                result = await dao_method(*args, **kwargs)
                self.info(
                    dao_class.__name__ + '.' + dao_method.__name__,
                    kwargs,
                    f"{repr(result)}"
                )
                return result
            except Exception as e:
                self.error(
                    dao_class.__name__ + '.' + dao_method.__name__,
                    kwargs,
                    f"{str(e)}"
                )
                raise e
        return wrapper
    

logger = Log()
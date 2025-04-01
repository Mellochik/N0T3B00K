import datetime
import logging
from typing import Callable


class Logger:
    logger = logging.getLogger('uvicorn')
    
    def info(self, func: Callable, parameters: dict, result: str) -> None:
        self.logger.info(f"{datetime.datetime.now()} - {func.__name__}("
                         f"{', '.join([f'{key}={value}' for key, value in parameters.items()])}"
                         f") -> {result}")
    
    def error(self, func: Callable, parameters: dict, message: str) -> None:
        self.logger.error(f"{datetime.datetime.now()} - {func.__name__}("
                          f"{', '.join([f'{key}={value}' for key, value in parameters.items()])}"
                          f") -> {message}")
    
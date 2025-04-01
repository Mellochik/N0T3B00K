from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    """
    Исключение для ошибки 400 Bad Request.
    """
    
    def __init__(self, detail: str = "Bad request", headers: dict = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)

class UnauthorizedException(HTTPException):
    """
    Исключение для ошибки 401 Unauthorized.
    """
    
    def __init__(self, detail: str = "Unauthorized", headers: dict = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)

class ForbiddenException(HTTPException):
    """
    Исключение для ошибки 403 Forbidden.
    """
    
    def __init__(self, detail: str = "Forbidden", headers: dict = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers)

class NotFoundException(HTTPException):
    """
    Исключение для ошибки 404 Not Found.
    """
    
    def __init__(self, detail: str = "Not found", headers: dict = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)

class ConflictException(HTTPException):
    """
    Исключение для ошибки 409 Conflict.
    """
    
    def __init__(self, detail: str = "Conflict", headers: dict = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, headers=headers)

class UnprocessableEntityException(HTTPException):
    """
    Исключение для ошибки 422 Unprocessable Entity.
    """
    
    def __init__(self, detail: str = "Unprocessable entity", headers: dict = None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail, headers=headers)

class TooManyRequestsException(HTTPException):
    """
    Исключение для ошибки 429 Too Many Requests.
    """
    
    def __init__(self, detail: str = "Too many requests", headers: dict = None):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail, headers=headers)

class InternalServerErrorException(HTTPException):
    """
    Исключение для ошибки 500 Internal Server Error.
    """
    
    def __init__(self, detail: str = "Internal server error", headers: dict = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, headers=headers)

class ServiceUnavailableException(HTTPException):
    """
    Исключение для ошибки 503 Service Unavailable.
    """
    
    def __init__(self, detail: str = "Service unavailable", headers: dict = None):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail, headers=headers)

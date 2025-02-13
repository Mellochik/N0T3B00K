from .documents import Base as documents_base
from .tasks import Base as tasks_base
from .users import Base as users_base
from sqlalchemy import text

__all__ = ["users_base", "documents_base", "tasks_base", "get_all_bases", "create_schemas"]

def get_all_bases():
    return [users_base, documents_base, tasks_base]

from api.core.dao import BaseDAO
from api.models.users import User


class UserDAO(BaseDAO):
    model = User
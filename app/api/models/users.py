import datetime

from sqlalchemy.orm import Mapped, mapped_column

from api.core.database import Base


class User(Base):
    """
    Представляет таблицу пользователей.
    
    Атрибуты:
        id (int): Первичный ключ пользователя, автоинкремент.
        username (str): Логин пользователя, уникальный, не может быть null.
        password (str): Пароль пользователя, не может быть null.
        email (str): Email пользователя, уникальный, не может быть null.
        name (str): Имя пользователя, не может быть null.
        surname (str): Фамилия пользователя, не может быть null.
        created_at (date): Дата создания пользователя, по умолчанию - сегодня.
        is_superuser (bool): Флаг суперпользователя, по умолчанию - False.
        is_active (bool): Флаг активности пользователя, по умолчанию - True.
    """
    
    __tablename__ = 'users'
    __table_args__ = {
        'schema': 'users',
        'comment': 'Таблица для хранения пользователей'
    }


    id:           Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Идентификатор пользователя")
    username:     Mapped[str] = mapped_column(unique=True, nullable=False, comment="Логин пользователя")
    password:     Mapped[str] = mapped_column(nullable=False, comment="Пароль пользователя")
    email:        Mapped[str] = mapped_column(unique=True, nullable=False, comment="Email пользователя")
    first_name:   Mapped[str] = mapped_column(nullable=False, comment="Имя пользователя")
    last_name:    Mapped[str] = mapped_column(nullable=False, comment="Фамилия пользователя")
    created_at:   Mapped[datetime.date] = mapped_column(default=datetime.date.today, comment="Дата создания пользователя")
    
    is_superuser: Mapped[bool] = mapped_column(default=False, server_default='false', nullable=False, comment="Флаг суперпользователя")
    
    
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
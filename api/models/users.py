from sqlalchemy import String, Date, Boolean, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import text

import datetime


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(schema="users")
    
    @classmethod
    async def create_schema(cls, conn):
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {cls.metadata.schema}"))


class User(Base):
    """
    Представляет таблицу пользователей.
    
    Атрибуты:
        id (int): Первичный ключ пользователя, автоинкремент.
        login (str): Логин пользователя, уникальный, не может быть null.
        password (str): Пароль пользователя, не может быть null.
        email (str): Email пользователя, уникальный, не может быть null.
        name (str): Имя пользователя, не может быть null.
        surname (str): Фамилия пользователя, не может быть null.
        created_at (date): Дата создания пользователя, по умолчанию - сегодня.
        is_superuser (bool): Флаг суперпользователя, по умолчанию - False.
        is_active (bool): Флаг активности пользователя, по умолчанию - True.
    """
    
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Таблица для хранения пользователей'}

    id:           Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login:        Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password:     Mapped[str] = mapped_column(String(255), nullable=False)
    email:        Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name:         Mapped[str] = mapped_column(String(20), nullable=False)
    surname:      Mapped[str] = mapped_column(String(50), nullable=False)
    created_at:   Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active:    Mapped[bool] = mapped_column(Boolean, default=True)
    
    def __str__(self):
        return f"User(id={self.id}, login={self.login}, email={self.email}, name={self.name}, surname={self.surname})"

    def __repr__(self):
        return f"<User(id={self.id}, login={self.login}, email={self.email}, name={self.name}, surname={self.surname})>"
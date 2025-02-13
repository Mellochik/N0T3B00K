from sqlalchemy import Integer, String, Date, ForeignKey, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.sql import text

from api.models.users import User

import datetime


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(schema="docs")

    @classmethod
    async def create_schema(cls, conn):
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {cls.metadata.schema}"))


class SpaceUser(Base):
    """
    Представляет таблицу ассоциаций между пространствами и пользователями.
    
    Атрибуты:
        id (int): Первичный ключ ассоциации.
        space_id (int): Внешний ключ, ссылающийся на пространство.
        user_id (int): Внешний ключ, ссылающийся на пользователя.
    """
    
    __tablename__ = 'space_user'
    __table_args__ = {'comment': 'Таблица для связи пространств и пользователей'}


    id:       Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    space_id: Mapped[int] = mapped_column(Integer, ForeignKey('spaces.id', ondelete="CASCADE"), nullable=False)
    user_id:  Mapped[int] = mapped_column(Integer, ForeignKey('users.users.id'), nullable=False)

    def __str__(self):
        return f"SpaceUser(id={self.id}, space_id={self.space_id}, user_id={self.user_id})"

    def __repr__(self):
        return f"<SpaceUser(id={self.id}, space_id={self.space_id}, user_id={self.user_id})>"
    
    
class Space(Base):
    """
    Представляет таблицу пространств.
    
    Атрибуты:
        id (int): Первичный ключ пространства, автоинкремент.
        name (str): Название пространства, не может быть null.
        users (relationship): Связь с моделью User через ассоциативную таблицу SpaceUser.
        columns (relationship): Связь с моделью Column, с back_populates, установленным на "space".
    """
    
    __tablename__ = 'spaces'
    __table_args__ = {'comment': 'Таблица для хранения пространств'}

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    
    users = relationship("User", secondary=SpaceUser.__tablename__)
    documents = relationship("Document", back_populates="space", cascade="all, delete-orphan")

    def __str__(self):
        return f"Space(id={self.id}, name={self.name})"

    def __repr__(self):
        return f"<Space(id={self.id}, name={self.name})>"
    

class Document(Base):
    """
    Представляет таблицу документов.
    
    Атрибуты:
        id (int): Первичный ключ документа, автоинкремент.
        space_id (int): Внешний ключ, ссылающийся на пространство.
        parent_id (int): Внешний ключ, ссылающийся на родительский документ.
        author_id (int): Внешний ключ, ссылающийся на пользователя.
        title (str): Название документа, не может быть null.
        content (str): Содержимое документа, не может быть null.
        created_at (date): Дата создания документа, по умолчанию - сегодня.
    """
    
    __tablename__ = 'documents'
    __table_args__ = {'comment': 'Таблица для хранения документов'}

    id:         Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    space_id:   Mapped[int] = mapped_column(Integer, ForeignKey('spaces.id', ondelete="CASCADE"), nullable=False)
    parent_id:  Mapped[int] = mapped_column(Integer, ForeignKey('documents.id', ondelete="CASCADE"), nullable=True)
    author_id:  Mapped[int] = mapped_column(Integer, ForeignKey('users.users.id'), nullable=False)
    title:      Mapped[str] = mapped_column(String(50), nullable=False)
    content:    Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    
    space = relationship("Space", back_populates="documents")
    documents = relationship("Document", back_populates="documents", cascade="all, delete-orphan")

    def __str__(self):
        return (f"Document(id={self.id}, space_id={self.space_id}, parent_id={self.parent_id}, author_id={self.author_id}, title={self.title},"
                f"content={self.content}, created_at={self.created_at})")
                 
    def __repr__(self):
        return (f"<Document(id={self.id}, space_id={self.space_id}, parent_id={self.parent_id}, author_id={self.author_id}, title={self.title},"
                f"content={self.content}, created_at={self.created_at})>")
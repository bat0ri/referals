from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.model import User
from config import db


class UserRepository:
    """
    Репозиторий пользователей.
    """

    @staticmethod
    async def insert(new_user: User) -> User:
        """
        Вставляет нового пользователя в базу данных.

        Args:
            new_user (User): Новый пользователь.

        Returns:
            User: Вставленный пользователь.
        """
        async with db as session:
            async with session.begin():
                session.add(new_user)
            await db.commit_rollback()

    @staticmethod
    async def get_all() -> List[User]:
        """
        Получает всех пользователей из базы данных.

        Returns:
            List[User]: Список всех пользователей.
        """
        async with db as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_email(email: str) -> User:
        """
        Получает пользователя по его адресу электронной почты.

        Args:
            email (str): Адрес электронной почты пользователя.

        Returns:
            User: Пользователь с указанным адресом электронной почты.
        """
        async with db as session:
            query = select(User).filter(User.email == email)
            result = await session.execute(query)
            return result.scalars().first()

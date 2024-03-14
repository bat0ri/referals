from fastapi import Depends
from sqlalchemy import select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from referal.models import ReferalCode, Referalship
from config import db


class CodeRepository:
    """
    Репозиторий для работы с реферальными кодами.
    """

    @staticmethod
    async def insert(new_code: ReferalCode) -> ReferalCode:
        """
        Вставка нового реферального кода в базу данных.

        Args:
            new_code (ReferalCode): Новый реферальный код для вставки.

        Returns:
            ReferalCode: Вставленный реферальный код.
        """
        async with db as session:
            async with session.begin():
                session.add(new_code)
            await db.commit_rollback()

    @staticmethod
    async def get_all():
        """
        Получение всех реферальных кодов из базы данных.

        Returns:
            List[ReferalCode]: Список всех реферальных кодов.
        """
        async with db as session:
            query = select(ReferalCode)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_id(id: str):
        """
        Получение реферального кода по его идентификатору.

        Args:
            id (str): Идентификатор реферального кода.

        Returns:
            ReferalCode: Реферальный код с указанным идентификатором.
        """
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.id==id)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def get_by_parent_id(parent_id: str):
        """
        Получение реферального кода по идентификатору родительского пользователя.

        Args:
            parent_id (str): Идентификатор родительского пользователя.

        Returns:
            ReferalCode: Реферальный код родительского пользователя.
        """
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.parent_id==parent_id, ReferalCode.is_active==True)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def get_all_by_parent_id(parent_id: str):
        """
        Получение всех реферальных кодов по идентификатору родительского пользователя.

        Args:
            parent_id (str): Идентификатор родительского пользователя.

        Returns:
            List[ReferalCode]: Список всех реферальных кодов родительского пользователя.
        """
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.parent_id==parent_id)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_code(code: str):
        """
        Получение реферального кода по его коду.

        Args:
            code (str): Код реферального кода.

        Returns:
            ReferalCode: Реферальный код с указанным кодом.
        """
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.code==code, ReferalCode.is_active==True)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def update_active_code(parent_id: str):
        """
        Обновление активного статуса реферальных кодов для указанного родительского пользователя.

        Args:
            parent_id (str): Идентификатор родительского пользователя.
        """
        async with db as session:
            query = update(ReferalCode).where(ReferalCode.is_active==True, ReferalCode.parent_id==parent_id).values(is_active=False)
            result = await session.execute(query)
            await db.commit_rollback()


class ReferalshipRepository:
    """
    Репозиторий для работы с отношениями между реферальными кодами и пользователями.
    """

    @staticmethod
    async def insert(new_ref: Referalship) -> Referalship:
        """
        Вставка нового отношения между реферальным кодом и пользователем в базу данных.

        Args:
            new_ref (Referalship): Новое отношение между реферальным кодом и пользователем для вставки.

        Returns:
            Referalship: Вставленное отношение между реферальным кодом и пользователем.
        """
        async with db as session:
            async with session.begin():
                session.add(new_ref)
            await db.commit_rollback()

    @staticmethod
    async def get_all():
        """
        Получение всех отношений между реферальными кодами и пользователями из базы данных.

        Returns:
            List[Referalship]: Список всех отношений между реферальными кодами и пользователями.
        """
        async with db as session:
            query = select(Referalship)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_id(id: str):
        """
        Получение отношения между реферальным кодом и пользователем по его идентификатору.

        Args:
            id (str): Идентификатор отношения между реферальным кодом и пользователем.

        Returns:
            Referalship: Отношение между реферальным кодом и пользователем с указанным идентификатором.
        """
        async with db as session:
            query = select(Referalship).filter(Referalship.id==id)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def get_by_some_ids(ids: List[str]):
        """
        Получение отношений между реферальным кодом и пользователем по списку идентификаторов кодов.

        Args:
            ids (List[str]): Список идентификаторов реферальных кодов.

        Returns:
            List[Referalship]: Список отношений между реферальным кодом и пользователем с указанными идентификаторами кодов.
        """
        async with db as session:
            query = select(Referalship).filter(Referalship.code_id.in_(ids))
            result = await session.execute(query)
            return result.scalars().all()

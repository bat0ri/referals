from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from referal.models import ReferalCode, Referalship
from config import db


class Repository:
    """
    Общий репозиторий для операций с базой данных.
    """
    def __init__(self, model):
        self.model = model

    async def insert(self, item):
        """
        Вставляет элемент в базу данных.
        """
        async with db as session:
            async with session.begin():
                session.add(item)
            await db.commit_rollback()

    async def get_all(self):
        """
        Получает все элементы из базы данных.
        """
        async with db as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_id(self, id):
        """
        Получает элемент из базы данных по его идентификатору.
        """
        async with db as session:
            query = select(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            return result.scalars().first()

    async def get_by_some_ids(self, ids: List[str]):
        """
        Получает элементы из базы данных по списку идентификаторов.
        """
        async with db as session:
            query = select(self.model).filter(self.model.id.in_(ids))
            result = await session.execute(query)
            return result.scalars().all()


class CodeRepository(Repository):
    """
    Репозиторий для работы с реферальными кодами.
    """
    def __init__(self):
        super().__init__(ReferalCode)

    async def get_by_parent_id(self, parent_id: str):
        """
        Получает реферальный код по идентификатору родителя.
        """
        async with db as session:
            query = select(self.model).filter(
                self.model.parent_id == parent_id, 
                self.model.is_active == True
            )
            result = await session.execute(query)
            return result.scalars().first()

    async def get_all_by_parent_id(self, parent_id: str):
        """
        Получает все реферальные коды по идентификатору родителя.
        """
        async with db as session:
            query = select(self.model).filter(self.model.parent_id == parent_id)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_code(self, code: str):
        """
        Получает реферальный код по его значению.
        """
        async with db as session:
            query = select(self.model).filter(
                self.model.code == code, 
                self.model.is_active == True
            )
            result = await session.execute(query)
            return result.scalars().first()

    async def update_active_code(self, parent_id: str):
        """
        Обновляет статус активности реферального кода по идентификатору родителя.
        """
        async with db as session:
            query = update(self.model).where(
                self.model.is_active == True, 
                self.model.parent_id == parent_id
            ).values(is_active=False)
            result = await session.execute(query)
            await db.commit_rollback()


class ReferalshipRepository(Repository):
    """
    Репозиторий для работы с связями между реферальными кодами и пользователями.
    """
    def __init__(self):
        super().__init__(Referalship)

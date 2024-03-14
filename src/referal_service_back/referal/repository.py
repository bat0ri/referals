from fastapi import Depends
from sqlalchemy import select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from referal.models import ReferalCode, Referalship
from config import db


class CodeRepository:

    @staticmethod
    async def insert(new_code: ReferalCode) -> ReferalCode:
        async with db as session:
            async with session.begin():
                session.add(new_code)
            await db.commit_rollback()

    @staticmethod
    async def get_all():
        async with db as session:
            query = select(ReferalCode)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_id(id: str):
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.id==id)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def get_by_parent_id(parent_id: str):
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.parent_id==parent_id, ReferalCode.is_active==True)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def get_all_by_parent_id(parent_id: str):
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.parent_id==parent_id)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_code(code: str):
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.code==code, ReferalCode.is_active==True)
            result = await session.execute(query)
            return result.scalars().first()


    @staticmethod
    async def update_active_code(parent_id: str):
        async with db as session:
            query = update(ReferalCode).where(ReferalCode.is_active==True, ReferalCode.parent_id==parent_id).values(is_active=False)
            result = await session.execute(query)
            await db.commit_rollback()



class ReferalshipRepository:

    @staticmethod
    async def insert(new_ref: Referalship) -> Referalship:
        async with db as session:
            async with session.begin():
                session.add(new_ref)
            await db.commit_rollback()


    @staticmethod
    async def get_all():
        async with db as session:
            query = select(Referalship)
            result = await session.execute(query)
            return result.scalars().all()


    @staticmethod
    async def get_by_id(id: str):
        async with db as session:
            query = select(Referalship).filter(Referalship.id==id)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def get_by_some_ids(ids: List[str]):
        async with db as session:
            query = select(Referalship).filter(Referalship.code_id.in_(ids))
            result = await session.execute(query)
            return result.scalars().all()
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
    async def get_by_code(code: str):
        async with db as session:
            query = select(ReferalCode).filter(ReferalCode.code==code)
            result = await session.execute(query)
            return result.scalars().first()


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
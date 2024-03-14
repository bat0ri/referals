from referal.models import ReferalCode, Referalship
from referal.repository import CodeRepository, ReferalshipRepository
from referal.schemas import CreateReferalCodeSchema, ReferalshipSchema
from uuid import UUID
from fastapi import Depends, HTTPException
from auth.model import User
from auth.repository import UserRepository
import random
import string
from datetime import datetime


def generate_referral_code(length=6):
    """Генерирует реферальный код заданной длины."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


async def create_code(data: CreateReferalCodeSchema):
    """Создает новый реферальный код."""
    new_code = ReferalCode(
        code=generate_referral_code(),
        parent_id=data.parent_id,
        exp_date=data.exp_date,
        is_active=data.is_active
    )
    return await CodeRepository.insert(new_code)


async def update_code(user: User):
    """Обновляет статус активности реферального кода."""
    await CodeRepository.update_active_code(user.id)
    data = CreateReferalCodeSchema(parent_id=user.id, is_active=True)
    return await create_code(data)


async def get_code(code: str) -> UUID:
    """Получает идентификатор реферального кода по его значению."""
    res = await CodeRepository.get_by_code(code)
    if res.exp_date < datetime.now():
        raise HTTPException(status_code=400, detail='Срок годности истек')
    return res.id


async def get_code_by_email(email: str):
    """Получает реферальный код по адресу электронной почты пользователя."""
    user = await UserRepository.get_by_email(email=email)
    return await CodeRepository.get_by_parent_id(user.id)


async def create_referalship(data: ReferalshipSchema):
    """Создает связь между реферальным кодом и пользователем."""
    new_ship = Referalship(
        code_id=data.code_id,
        user_id=data.user_id
    )
    return await ReferalshipRepository.insert(new_ship)


async def get_all_referals(referer_id: str):
    """Получает всех рефералов по идентификатору реферера."""
    ref_codes = await CodeRepository.get_all_by_parent_id(referer_id)
    codes_id = [ref.id for ref in ref_codes]
    referalships = await ReferalshipRepository.get_by_some_ids(codes_id)
    return referalships

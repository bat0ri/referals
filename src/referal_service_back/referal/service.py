from referal.models import ReferalCode, Referalship
from referal.repository import CodeRepository, ReferalshipRepository
from referal.schemas import CreateReferalCodeSchema, ReferalshipSchema
from uuid import UUID

async def create_code(data: CreateReferalCodeSchema):
    new_code = ReferalCode(
        code=data.code,
        parent_id=data.parent_id,
        exp_date=data.exp_date,
        is_active=data.is_active
    )
    return await CodeRepository.insert(new_code)


async def validate_code(code: str) -> bool:
    return True if await CodeRepository.get_by_code(code) else False


async def get_code(code: str) -> UUID:
    res = await CodeRepository.get_by_code(code)
    return res.id


async def create_referalship(data: ReferalshipSchema):
    new_ship = Referalship(
        code_id=data.code_id,
        user_id=data.user_id
    )
    return await ReferalshipRepository.insert(new_ship)
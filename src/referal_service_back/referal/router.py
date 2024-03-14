from fastapi import APIRouter, Depends
from referal.service import update_code, get_code_by_email, get_all_referals
from auth.security import get_current_user

router = APIRouter(prefix='/referalcodes', tags=['Codes endpoints'])


@router.post('/update')
async def update_code_for_user(user=Depends(get_current_user)):
    """
    Обновляет реферальный код для пользователя.

    Args:
        user: Аутентифицированный пользователь.

    Returns:
        dict: Результат обновления реферального кода.
    """
    return await update_code(user)


@router.get('/get_code')
async def get_code_by_user_email(email: str):
    """
    Получает реферальный код по адресу электронной почты реферера.

    Args:
        email: Адрес электронной почты реферера.

    Returns:
        dict: Реферальный код.
    """
    return await get_code_by_email(email=email)


@router.get('/get_all_codes')
async def get_all_codes_by_user_email(referer_id: str):
    """
    Получает информацию о рефералах по идентификатору реферера.

    Args:
        referer_id: Идентификатор реферера.

    Returns:
        list: Информация о рефералах.
    """
    return await get_all_referals(referer_id)

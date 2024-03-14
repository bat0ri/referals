from fastapi import APIRouter
from auth.schemas import UserInputSchema, TokenInput, UserRegisterSchema
from auth import service, security

router = APIRouter()

@router.post("/create", status_code=200)
async def registration(user: UserRegisterSchema):
    """
    Регистрация нового пользователя.

    Args:
        user (UserRegisterSchema): Данные нового пользователя.

    Returns:
        JSON: Информация о пользователе.
    """
    return await service.create_user(user)

@router.post('/login', status_code=200)
async def login(user: UserInputSchema):
    """
    Аутентификация пользователя.

    Args:
        user (UserInputSchema): Данные пользователя для входа.

    Returns:
        JSON: Токен доступа.
    """
    return await service.login_user(user)

@router.post('/validate', status_code=200)
async def protected(token: TokenInput):
    """
    Проверка токена доступа.

    Args:
        token (TokenInput): Токен доступа для проверки.

    Returns:
        JSON: Информация о пользователе, закодированная в токене.
    """
    return security.decode_jwt(token.token)

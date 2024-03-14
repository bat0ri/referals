from pydantic import BaseModel, UUID4
from typing import Optional

class UserInputSchema(BaseModel):
    """
    Схема для входных данных пользователя.
    """
    email: str
    password: str

class UserRegisterSchema(UserInputSchema):
    """
    Схема для регистрации нового пользователя.
    """
    code: Optional[str] = None

class TokenInput(BaseModel):
    """
    Схема для входных данных токена.
    """
    token: str

class UserOutput(BaseModel):
    """
    Модель вывода пользователя.
    """
    id: UUID4
    email: str

class AuthResponse(BaseModel):
    """
    Ответ аутентификации.
    """
    token: str
    user: UserOutput

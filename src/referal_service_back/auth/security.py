import jwt
from fastapi import HTTPException, Request, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from auth.repository import UserRepository


def encode_jwt(user, expire_minutes: int = 5000):
    """
    Кодирует JWT токен для пользователя.

    Args:
        user: Пользователь, для которого будет создан токен.
        expire_minutes (int): Срок действия токена в минутах. По умолчанию 5000 минут.

    Returns:
        str: JWT токен.
    """
    now = datetime.utcnow()
    expiration_time = now + timedelta(minutes=expire_minutes)

    payload = {
        'sub': user.email,
        'exp': expiration_time,
        'iat': now,
        'token_type': "access"
    }

    return jwt.encode(payload, "secret", algorithm="HS256")


def decode_jwt(token: str, secret_key="secret"):
    """
    Декодирует JWT токен.

    Args:
        token (str): JWT токен для декодирования.
        secret_key (str): Секретный ключ для декодирования токена. По умолчанию "secret".

    Returns:
        dict: Раскодированный токен.
        
    Raises:
        HTTPException: Если произошла ошибка при декодировании токена.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=400, detail=f'{e}')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=400, detail=f'{e}')


class JWTBearer(HTTPBearer):
    """
    Проверка JWT токена пользователя.
    """

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Неверная схема аутентификации.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Неверный токен или истек срок его действия.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Неверный код авторизации.")

    def verify_jwt(self, jwt_token: str):
        """
        Проверяет действительность JWT токена.

        Args:
            jwt_token (str): JWT токен для проверки.

        Returns:
            bool: True, если токен действителен, иначе False.
        """
        is_token_valid = False
        try:
            payload = decode_jwt(jwt_token)
            is_token_valid = True
        except jwt.ExpiredSignatureError:
            is_token_valid = False
        except jwt.InvalidTokenError:
            is_token_valid = False
        return is_token_valid


async def get_current_user(token: str = Depends(JWTBearer())):
    """
    Получает текущего пользователя по JWT токену.

    Args:
        token (str): JWT токен пользователя.

    Returns:
        User: Текущий пользователь.
        
    Raises:
        HTTPException: Если токен недействителен или не удалось получить пользователя.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception

    payload = decode_jwt(token)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    return await UserRepository.get_by_email(email=email)

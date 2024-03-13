import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException


def encode_jwt(user, expire_minutes: int = 5000):

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
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=400, detail=f'{e}')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=400, detail=f'{e}')
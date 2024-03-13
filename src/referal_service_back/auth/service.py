from auth.repository import UserRepository
from auth.schemas import UserInputSchema, AuthResponse, UserOutput
from auth.model import User
from auth import security
from auth.hashing import BcryptHasher
from fastapi import HTTPException, status


async def create_user(user: UserInputSchema):
    new_user = await UserRepository.get_by_email(user.email)

    if new_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    new_user = User(email=user.email, hash_password=BcryptHasher.get_password_hash(user.password))
    await UserRepository.insert(new_user)
    return new_user


async def login_user(user: UserInputSchema):
    new_user = await UserRepository.get_by_email(user.email)

    if new_user is None:
        raise HTTPException(status_code=400, detail="Пользователь не зареган")

    if not BcryptHasher.verify_password(user.password, new_user.hash_password):
        raise HTTPException(status_code=400, detail="Неправильный пароль")
    else:
        response = AuthResponse(
            token=security.encode_jwt(user),
            user=UserOutput(id=new_user.id, email=new_user.email)
        )
        return response

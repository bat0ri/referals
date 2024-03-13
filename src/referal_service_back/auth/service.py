from auth.repository import UserRepository
from auth.schemas import UserInputSchema, AuthResponse, UserOutput, UserRegisterSchema
from auth.model import User
from auth import security
from auth.hashing import BcryptHasher
from fastapi import HTTPException, status
from referal.service import create_code, validate_code, create_referalship, get_code
from referal.schemas import CreateReferalCodeSchema, ReferalshipSchema
from referal.models import ReferalCode, generate_referral_code


async def create_user(user: UserRegisterSchema):
    new_user = await UserRepository.get_by_email(user.email)

    if new_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    if user.code and await validate_code(user.code):
        print("пришел реферал c правильным реф кодом")
        code_id = await get_code(user.code)
    else:
        raise HTTPException(status_code=400, detail="Неправильный реф код")



    new_user = User(email=user.email, hash_password=BcryptHasher.get_password_hash(user.password))

    await UserRepository.insert(new_user)
    await create_code(CreateReferalCodeSchema(
        code=generate_referral_code(),
        parent_id=new_user.id,
        is_active=True
    ))

    if code_id:
        ref = ReferalshipSchema(code_id=code_id, user_id=new_user.id)
        await create_referalship(ref)

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

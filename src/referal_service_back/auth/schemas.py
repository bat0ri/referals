from pydantic import BaseModel, UUID4, Field
import uuid
from datetime import datetime
from typing import Optional


class UserInputSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(UserInputSchema):
    code: Optional[str] = None


class TokenInput(BaseModel):
    token: str


class UserOutput(BaseModel):
    id: UUID4
    email: str


class AuthResponse(BaseModel):
    token: str
    user: UserOutput
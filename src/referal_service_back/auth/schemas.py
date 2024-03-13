from pydantic import BaseModel, UUID4
import uuid
from datetime import datetime


class UserInputSchema(BaseModel):
    email: str
    password: str


class TokenInput(BaseModel):
    token: str


class UserOutput(BaseModel):
    id: UUID4
    email: str


class AuthResponse(BaseModel):
    token: str
    user: UserOutput
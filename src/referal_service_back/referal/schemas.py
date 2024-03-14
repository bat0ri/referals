from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class CreateReferalCodeSchema(BaseModel):
    """
    Схема данных для создания реферального кода.
    """
    parent_id: UUID
    exp_date: Optional[datetime] = None
    is_active: bool


class ReferalshipSchema(BaseModel):
    """
    Схема данных для связи между реферальным кодом и пользователем.
    """
    code_id: UUID
    user_id: UUID

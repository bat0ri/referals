from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID



class CreateReferalCodeSchema(BaseModel):
    code: str
    parent_id: UUID
    exp_date: Optional[datetime] = None
    is_active: bool



class ReferalshipSchema(BaseModel):
    code_id: UUID
    user_id: UUID

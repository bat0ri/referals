from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
import uuid
from auth.model import User
import random
import string


def generate_referral_code(length=6):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

Base = declarative_base()


class ReferalCode(Base):

    __tablename__ = 'referal_codes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    
    # чей реф-код
    parent_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)

    # срок годности
    exp_date = Column(DateTime, default=datetime.now()+timedelta(days=30), nullable=True)
    is_active = Column(Boolean, nullable=False)


class Referalship(Base):

    __tablename__ = 'referalship'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # внешний ключ к рефкоду
    code_id = Column(UUID(as_uuid=True), ForeignKey(ReferalCode.id), nullable=False)
    # внешний ключ к рефералу
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)

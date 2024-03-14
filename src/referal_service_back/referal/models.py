from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
import uuid
from auth.model import User

Base = declarative_base()

class ReferalCode(Base):
    """Модель для реферального кода."""
    __tablename__ = 'referal_codes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    
    # Чей реферальный код
    parent_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    
    # Срок годности
    exp_date = Column(DateTime, default=datetime.now() + timedelta(minutes=2), nullable=True)
    is_active = Column(Boolean, nullable=False)

class Referalship(Base):
    """Модель для связи реферального кода с рефералом."""
    __tablename__ = 'referalship'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Внешний ключ к реферальному коду
    code_id = Column(UUID(as_uuid=True), ForeignKey(ReferalCode.id), nullable=False)
    
    # Внешний ключ к рефералу
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)

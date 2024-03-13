from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import datetime
import uuid



Base = declarative_base()


class User(Base):

    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    email = Column(String, nullable= False)
    hash_password = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.now(), nullable= True)


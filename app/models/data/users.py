import string
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.configurations.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import UUID

class Users(Base):
    _tablename_ = 'users'

    id = Column(UUID, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    type = Column(String, nullable=False)  # 'particular' or 'professional'

    _mapper_args_ = {
        'polymorphic_identity': 'base_user',
        'polymorphic_on': type
    }
import string
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.configurations.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import UUID

class ParticularUser(Users):
    _tablename_ = 'particular'

    id = Column(UUID, ForeignKey('base_users.id'), primary_key=True)
    birth_day = Column(Date)

    _mapper_args_ = {
        'polymorphic_identity': 'particular_user',
    }
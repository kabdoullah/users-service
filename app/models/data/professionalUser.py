import string
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.configurations.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import UUID

class ProfessionalUser(Users):
    _tablename_ = 'professional'

    id = Column(UUID, ForeignKey('base_users.id'), primary_key=True)
    phone_2 = Column(String, nullable=True)  # Numéro fixe
    company = Column(String)
    country = Column(String)
    company_type = Column(String)
    professional_category = Column(String)
    sub_category = Column(String, nullable=True)
    website = Column(String, nullable=True)

    _mapper_args_ = {
        'polymorphic_identity': 'professional_user',
    }

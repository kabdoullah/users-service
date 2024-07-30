import uuid
from sqlalchemy import Column, DateTime, String, Boolean, Integer, func
from app.configuration.database import Base
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    type = Column(String, nullable=False)  
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    login_attempts = Column(Integer, default=0)
    last_login_attempt = Column(DateTime, default=None)
    last_login = Column(DateTime, default=None)
    

    sessions = relationship("Session", back_populates="user")

    __mapper_args__ = {
        'polymorphic_identity': 'base_user',
        'polymorphic_on': type
    }
